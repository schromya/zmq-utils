from zmq_utils.broker import push_pull_broker

import sys
import argparse


def main():
    """
    Command-line entry point for running a ZeroMQ broker.
    Currently it supports a `push_pull` broker, which:
        * Accepts tasks from producer(s) over a PUSH socket.
        * Forwards tasks to worker(s) over a PULL socket.
        * Publishes all forwarded messages to a PUB socket for logging/monitoring.

    Args are provided via command-line flags; see `-h` for details.
    """
    parser = argparse.ArgumentParser(description="ZeroMQ Broker")
    subparsers = parser.add_subparsers(dest="broker", required=True, help="Broker type")

    # Pull-Push broker subcommand
    pp_parser = subparsers.add_parser("push_pull", help="Run a pull-push broker")
    pp_parser.add_argument("--push_host", type=str, help="Host for producer PUSH connections")
    pp_parser.add_argument("--push_port", type=int, help="Port for producer PUSH connections")
    pp_parser.add_argument("--pull_host", type=str, help="Host for worker PULL connections")
    pp_parser.add_argument("--pull_port", type=int, help="Port for worker PULL connections")
    pp_parser.add_argument("--log_host", type=str, help="Host for PUB logging")
    pp_parser.add_argument("--log_port", type=int, help="Port for PUB logging")



    args = parser.parse_args()

    if args.broker == "push_pull":
        push_pull_broker(
            push_host=args.push_host,
            push_port=args.push_port,
            pull_host=args.pull_host,
            pull_port=args.pull_port,
            log_host=args.log_host,
            log_port=args.log_port,
        )


if __name__ == "__main__":
    main()