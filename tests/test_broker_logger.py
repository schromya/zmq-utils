import threading
import time
import zmq
from zmq_utils.broker import pull_push_broker
from zmq_utils.logger import sub_logger

HOST = '127.0.0.1'
PUSH_PORT = 5557
PULL_PORT = 5558
LOG_PORT = 5559

def run_broker():
    """
    Start the broker
    """
    pull_push_broker(HOST, PUSH_PORT, HOST, PULL_PORT, HOST, LOG_PORT)


def run_logger():
    """
    Start the logger
    """
    sub_logger(HOST, LOG_PORT)


def run_puller():
    """
    Connects to the broker's PUSH socket and prints all received messages.
    """
    ctx = zmq.Context()
    pull = ctx.socket(zmq.PULL)
    pull.connect(f"tcp://{HOST}:{PULL_PORT}")
    while True:
        msg = pull.recv()
        print("WORKER RECEIVED:", msg)


def test_broker_logger():
    """
    Thread broker and logger.
    """
    print("/nSTARTING TEST")
    broker_thread = threading.Thread(target=run_broker, daemon=True)
    broker_thread.start()
    time.sleep(1)  # Allow broker to start

    logger_thread = threading.Thread(target=run_logger, daemon=True)
    logger_thread.start()
    time.sleep(1)  # Allow logger to connect

    puller_thread = threading.Thread(target=run_puller, daemon=True)
    puller_thread.start()
    time.sleep(1)  # Allow puller to connect

    # Start Pusher
    ctx = zmq.Context()
    push = ctx.socket(zmq.PUSH)
    push.connect(f'tcp://{HOST}:{PUSH_PORT}')
    time.sleep(1)
    push.send(b"msg1")
    push.send(b"msg2")
    
    time.sleep(1)

    # TODO: assert

