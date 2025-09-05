from typing import Callable, Tuple, TextIO

def make_writer(storage_path: str | None) -> Tuple[Callable[[str], None], TextIO | None]:
    """
    Creates a writer function that writes strings either to a 
    file or to stdout.

    Args:
        storage_path (str | None): Path to the file to write to. 
        If None, output is printed to stdout.

    Returns:
        (Callable[[str]], TextIO | None): 
            - A callable that takes a string and writes it to the file or stdout.
            - The file object if writing to a file, otherwise None.
    """
    if storage_path:
        f = open(storage_path, "w", encoding="utf-8")

        def write(line: str) -> None:
            f.write(line)
            f.write("\n")
            f.flush()

        return write, f
    
    else:
        return (lambda s: print(s)), None