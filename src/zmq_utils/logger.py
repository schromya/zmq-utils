import zmq

def sub_logger(log_host: str, log_port: int):
    """
    Subscribes to the given socket to log all messages.

    Args:
        log_host (str): Host/IP to connect the SUB socket for logging.
        log_port (int): Port to connect the SUB socket for logging.
    """
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect(f"tcp://{log_host}:{log_port}")
    sub.setsockopt_string(zmq.SUBSCRIBE, "")  

    while True:
        print("LOG:", sub.recv())