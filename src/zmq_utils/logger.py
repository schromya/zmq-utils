from zmq_utils.utils import encode_frame, encode_frames

from enum import Enum
import time
import json
import signal
import sys
import threading


import zmq


class SocketPattern(Enum):
    PUSH_PULL = "push_pull"
    PUB_SUB = "pub_sub"
    # REQ_REP = "req_rep"
    # DEALER_ROUTER = "dealer_router"
    # XPUB_XSUB = "xpub_xsub"
    # PAIR = "pair"
    # STREAM = "stream"


class Logger():
    def __init__(self, log_host: str, log_port: int, socket_pattern:str, 
                 storage_path:str=None):
        """
        Logger class for subscribing to and either printing or 
        storing messages from a ZeroMQ socket.

        Args:
            log_host (str): Host/IP to connect the SUB socket for logging.
            log_port (int): Port to connect the SUB socket for logging.
            socket_pattern (str): Pattern of ZMQ socket. (Options: "push_pull",
                "pub_sub")
            storage_path (str): Path to store data. If None, then only prints
                the data instead of storing it. (Default: None)
        """
    
        self.log_endpoint = f"tcp://{log_host}:{log_port}"
        self.socket_pattern = SocketPattern(socket_pattern)
        self.storage_path = storage_path
        self.file = None
        self.sub = None


    def shutdown(self, *_args, exit_on_shutdown=False):
        """
        Safely stops logging. Should not be called from log_thread.
        """

        # Causes rec_multipart in while loop to stop safely
        try:
            if self.sub:
                self.sub.close(0)
                
        finally:
            self.sub = None
        try:
            if self.file:
                self.file.close()
            
        finally:
            if exit_on_shutdown:
                sys.exit(0)
            elif self.log_thread and threading.current_thread() != self.log_thread:
                self.log_thread.join()


    def log_listener(self):
        """
        Connect to capture PUB and write records (manifest + JSONL messages).
        Each record includes: socket_pattern, ts, optional topic, frames.
        """
        ctx = zmq.Context.instance()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect(self.log_endpoint)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "")
        self.sub.setsockopt(zmq.RCVTIMEO, 50)  # Non blocking
        time.sleep(0.2)  # slow-joiner guard to avoid missing initial msgs

        # open file (if any) and write manifest/header
        manifest = {
            "version": "1.0",
            "created_at": time.time(),
            "schema": "socket_pattern|ts|topic?|frames",
            "socket_pattern": self.socket_pattern.value,
        }
        manifest_dump = json.dumps(manifest,)
        if self.storage_path:
            self.file = open(self.storage_path, "w", encoding="utf-8")
            self.file.write(manifest_dump + "\n")
            self.file.flush()
        else:
            print(manifest_dump)
        
        # Only shutdown when interrupted if not threaded
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, lambda *a: self.shutdown(exit_on_shutdown=True))
            signal.signal(signal.SIGTERM, lambda *a: self.shutdown(exit_on_shutdown=True))

        while self.sub:
            try:
                frames = self.sub.recv_multipart()   # may raise zmq.Again on timeout
            except zmq.Again:
                continue  

            ts = time.time()

            if self.socket_pattern == SocketPattern.PUB_SUB and frames:
                topic = encode_frame(frames[0])
                enc_frames = encode_frames(frames[1:])
            else:
                # Default behavior for PUSH/PULL: no topic; keep all frames as payload.
                topic = ""
                enc_frames = encode_frames(frames)

            record = {
                "socket_pattern": self.socket_pattern.value,
                "ts": ts,
                "frames": enc_frames,
                "topic": topic
            }
            record_dump = json.dumps(record, ensure_ascii=False)

            if self.storage_path:
                self.file.write(record_dump + "\n")
                self.file.flush()
            else:
                print(record_dump)
            
    
    def run_threaded_logging(self):
        """
        Starts the logger in its own thread.
        """

        self.log_thread = threading.Thread(target=self.log_listener, 
                                      daemon=True)
        self.log_thread.start()
        
