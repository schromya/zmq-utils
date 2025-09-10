import threading
import signal
from typing import Callable

def install_signal_handlers(shutdown_func: Callable):
    """
    Installs signal handlers for SIGINT and (if available) SIGTERM
    to call the provided shutdown_func. Only installs handlers if
    running in the main thread.
    
    Args:
        shutdown_func (Callable): Function to call on signal.
    """
    if threading.current_thread() is threading.main_thread():
        signal.signal(signal.SIGINT, shutdown_func)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, shutdown_func)