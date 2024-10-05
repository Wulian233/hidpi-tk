import os
from ctypes import pointer, windll, wintypes
from idlelib.run import fix_scaling
from tkinter import Tk

__version__ = "1.0.0"

__all__ = (
    "DPIAwareTk",
    "fix_HiDPI",
)

class DPIAwareTk(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fix_HiDPI(self)

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
            root.tk.call('tk', 'scaling', 96 * scale_factor / 100 / 72)
            
            # Get DPI for the monitor
            win_handle = wintypes.HWND(root.winfo_id())
            monitor_handle = windll.user32.MonitorFromWindow(win_handle, 2)  # MONITOR_DEFAULTTONEAREST = 2

            x_dpi = wintypes.UINT()
            y_dpi = wintypes.UINT()
            windll.shcore.GetDpiForMonitor(monitor_handle, 0, pointer(x_dpi), pointer(y_dpi))  # MDT_EFFECTIVE_DPI = 0

    # Adjust font sizes for HiDPI displays
    fix_scaling(root)
