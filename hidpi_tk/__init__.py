import os
import re
from ctypes import pointer, windll, wintypes
from tkinter import Tk

__version__ = "1.1.0"

__all__ = ("DPIAwareTk", "fix_HiDPI")


def Get_HWND_DPI(window_handle):
    """Get DPI information for a window handle."""
    if os.name == "nt":
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass  # this will fail on Windows Server and maybe early Windows

        DPI100pc = 96  # DPI 96 is 100% scaling
        DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
        winH = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(
            winH, wintypes.DWORD(2)
        )  # MONITOR_DEFAULTTONEAREST = 2

        X = wintypes.UINT()
        Y = wintypes.UINT()
        try:
            windll.shcore.GetDpiForMonitor(
                monitorhandle, DPI_type, pointer(X), pointer(Y)
            )
            return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
        except Exception:
            return 96, 96, 1  # Assume standard Windows DPI & scaling
    else:
        return None, None, 1


def TkGeometryScale(s, cvtfunc):
    """Scale geometry string based on DPI scaling."""
    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
    R = re.compile(patt).search(s)
    G = str(cvtfunc(R.group("W"))) + "x"
    G += str(cvtfunc(R.group("H"))) + "+"
    G += str(cvtfunc(R.group("X"))) + "+"
    G += str(cvtfunc(R.group("Y")))
    return G


def fix_scaling(root):
    """Scale fonts on HiDPI displays."""
    import tkinter.font

    scaling = float(root.tk.call("tk", "scaling"))
    if scaling > 1.4:
        for name in tkinter.font.names(root):
            font = tkinter.font.Font(root=root, name=name, exists=True)
            size = int(font["size"])
            if size < 0:
                font["size"] = round(-0.75 * size)


class DPIAwareTk(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fix_HiDPI(self)

        # Add scaling functions to the root window
        self.TkScale = lambda v: int(float(v) * self.DPI_scaling)
        self.geometry = lambda s: self.wm_geometry(TkGeometryScale(s, self.TkScale))


def fix_HiDPI(root):
    """Adjust scaling for HiDPI displays on Windows."""
    if os.name == "nt":
        try:
            # For Windows 8.1 and later
            windll.shcore.SetProcessDpiAwareness(2)
            scale_factor = windll.shcore.GetScaleFactorForDevice(0)
            shcore = True
        except Exception:
            # For Windows older than 8.1
            try:
                windll.user32.SetProcessDPIAware()
                shcore = False
            except Exception:
                return

        if shcore:
            # Set Tk scaling based on Windows DPI settings
            root.tk.call("tk", "scaling", 96 * scale_factor / 100 / 72)

            # Get DPI for the monitor
            win_handle = wintypes.HWND(root.winfo_id())
            monitor_handle = windll.user32.MonitorFromWindow(
                win_handle, 2
            )  # MONITOR_DEFAULTTONEAREST = 2

            x_dpi = wintypes.UINT()
            y_dpi = wintypes.UINT()
            windll.shcore.GetDpiForMonitor(
                monitor_handle, 0, pointer(x_dpi), pointer(y_dpi)
            )  # MDT_EFFECTIVE_DPI = 0

            # Store DPI information in the root window
            root.DPI_X = x_dpi.value
            root.DPI_Y = y_dpi.value
            root.DPI_scaling = (x_dpi.value + y_dpi.value) / (2 * 96)
        else:
            root.DPI_X, root.DPI_Y, root.DPI_scaling = Get_HWND_DPI(root.winfo_id())
    else:
        # Non-Windows systems
        root.DPI_X, root.DPI_Y, root.DPI_scaling = Get_HWND_DPI(root.winfo_id())

    fix_scaling(root)
