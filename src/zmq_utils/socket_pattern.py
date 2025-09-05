from enum import Enum

class SocketPattern(Enum):
    PUSH_PULL = "push_pull"
    PUB_SUB = "pub_sub"
    # REQ_REP = "req_rep"
    # DEALER_ROUTER = "dealer_router"
    # XPUB_XSUB = "xpub_xsub"
    # PAIR = "pair"
    # STREAM = "stream"