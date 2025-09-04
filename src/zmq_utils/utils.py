import base64
from typing import List, Union


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