import zmq

def push_pull_broker(push_host:str, push_port: int, pull_host:str, pull_port: int, 
                     log_host: str, log_port: int):
    """
    Starts a ZeroMQ proxy broker that forwards messages from producers (PUSH) 
    to workers (PULL), and publishes all messages to a PUB socket for 
    logging/monitoring.

    Producer(s) --PUSH--> [BROKER: PULL → PUSH] --PULL--> Worker(s)
                                |
                                +--PUB--> Logger(s)

    Args:
        push_host (str): Host/IP where the broker listens for producer PUSH connections.
        push_port (int): Port where the broker listens for producer PUSH connections.
        pull_host (str): Host/IP where the broker pushes tasks to workers (they PULL).
        pull_port (int): Port where the broker pushes tasks to workers.
        log_host (str): Host/IP to bind the PUB socket (log subscribers connect).
        log_port (int): Port to bind the PUB socket.
    """

    ctx = zmq.Context.instance()

    producer = ctx.socket(zmq.PULL)
    producer.bind(f"tcp://{push_host}:{push_port}")

    logger = ctx.socket(zmq.PUB)
    logger.bind(f"tcp://{log_host}:{log_port}")

    workers = ctx.socket(zmq.PUSH)
    workers.bind(f"tcp://{pull_host}:{pull_port}")

    zmq.proxy(producer, workers, logger) 


