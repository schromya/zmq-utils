from zmq_utils.logger import Logger
from zmq_utils.logger import SocketPattern

import sys
import argparse

def main():
    """
    Command-line entry point for running a ZeroMQ logger.

    This script connects a SUB socket to a broker's PUB capture endpoint 
    and records all observed messages. Records are written either to stdout 
    or to a JSONL file if `--storage_path` is provided.

    Args are provided via command-line flags; see `-h` for details.
    """
    parser = argparse.ArgumentParser(description="ZeroMQ Logger (SUB to PUB, print/store JSONL)")

    # Build choices directly from your enum so help text stays in sync
    socket_pattern_choices = [m.value for m in SocketPattern]

    parser.add_argument("--log_host", type=str, help="Host to connect SUB socket")
    parser.add_argument("--log_port", type=int, help="Port to connect SUB socket")
    parser.add_argument( "--socket_pattern", type=str, choices=socket_pattern_choices,
        help=f"Socket pattern ({', '.join(socket_pattern_choices)})")
    parser.add_argument("--storage_path", type=str, default=None,
        help="Path to write JSONL logs (default: print to stdout)")

    args = parser.parse_args()

    logger = Logger(
        log_host=args.log_host,
        log_port=args.log_port,
        socket_pattern=args.socket_pattern,
        storage_path=args.storage_path,
    )

    logger.run_logger()


if __name__ == "__main__":
    main()