from zmq_utils.socket_pattern import SocketPattern

from zmq_utils.utils_frames import process_frames
from zmq_utils.utils_writer import make_writer
from zmq_utils.utils_signal import install_signal_handlers

import time
import json
import threading

import zmq


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
        self.log_thread = None
        self.stop_event = threading.Event()


    def shutdown(self, *_args):
        """
        Safely stops logging. Should NOT be called from log_thread.
        """

        self.stop_event.set()

        # Wait for thread to finish if its running
        if self.log_thread and threading.current_thread() is not self.log_thread:
            self.log_thread.join()


    def run_logger(self):
        """
        Connect to capture PUB and write records (manifest + JSONL messages).
        Each record includes: socket_pattern, ts, optional topic, frames.
        """
        ctx = zmq.Context.instance()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect(self.log_endpoint)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "")
        self.sub.setsockopt(zmq.RCVTIMEO, 50)  # Non blocking
        time.sleep(0.2)

        writer, self.file = make_writer(self.storage_path)

        manifest = {
            "version": "1.0",
            "created_at": time.time(),
            "schema": "socket_pattern|ts|topic?|frames",
            "socket_pattern": self.socket_pattern.value,
        }

        writer(json.dumps(manifest))
        
        install_signal_handlers(self.shutdown)

        try:
            while not self.stop_event.is_set():
                try:
                    frames = self.sub.recv_multipart() 
                except zmq.Again:
                    continue  

                ts = time.time()

                topic, enc_frames = process_frames(self.socket_pattern, frames)

                record = {
                    "socket_pattern": self.socket_pattern.value,
                    "ts": ts,
                    "frames": enc_frames,
                    "topic": topic
                }

                writer(json.dumps(record, ensure_ascii=False))

        finally:
            # Shutdown sequence 
            if self.sub:
                self.sub.close(0)
            if self.file:
                self.file.close()


    def run_threaded_logger(self):
        """
        Starts the logger in its own thread.
        """

        self.log_thread = threading.Thread(target=self.run_logger, 
                                      daemon=False)
        self.log_thread.start()
        
