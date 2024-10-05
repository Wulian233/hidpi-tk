__version__: str
__all__: tuple[str, ...]

from tkinter import Tk

class DPIAwareTk(Tk):
    def __init__(self, *args: object, **kwargs: object) -> None: ...

def fix_HiDPI(root: Tk) -> None: ...
