from zmq_utils.socket_pattern import SocketPattern

import base64
from typing import List, Union, Iterable, Tuple


def encode_frame(frame_bytes: bytes) -> Union[str, dict]:
    """
    Convert a single frame of bytes into a JSON-safe value.

    Args:
        frame_bytes (bytes): The frame data as bytes.

    Returns:
        (str) or (dict): UTF-8 string if possible, 
        else {"b64": "<base64>"} dict.
    """
    try:
        return frame_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return {"b64": base64.b64encode(frame_bytes).decode("ascii")}


def encode_frames(frames_bytes: List[bytes]) -> List[Union[str, dict]]:
    """
    Convert a list of byte frames into a list of JSON-safe values.

    Args:
        frames_bytes (List[bytes]): List of frame data as bytes.

    Returns:
        List[Union[str, dict]]: List of UTF-8 strings if possible, else list
        of {"b64": "<base64>"} dicts.
    """
    return [encode_frame(b) for b in frames_bytes]


def process_frames(socket_pattern: SocketPattern, frames: Iterable[bytes]) -> Tuple[str, list]:
    """
    Processes a sequence of message frames according to the socket pattern.
    Args:
        socket_pattern (SocketPattern): The type of ZeroMQ socket pattern.
        frames (Iterable[bytes]): The message frames as bytes.

    Returns:
        (str, list): 
            - The topic as a string (empty if not PUB_SUB).
            - A list of encoded frames (JSON-safe).
    """
    
    frames = list(frames)
    if socket_pattern == SocketPattern.PUB_SUB and frames:
        topic = encode_frame(frames[0])
        enc_frames = encode_frames(frames[1:])
    else:
        # Default behavior for PUSH/PULL: no topic; keep all frames as payload.
        topic = ""
        enc_frames = encode_frames(frames)
    return topic, enc_frames