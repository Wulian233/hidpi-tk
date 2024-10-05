import os
from unittest.mock import MagicMock, patch

import pytest

from hidpi_tk import DPIAwareTk, fix_HiDPI


def test_dpiaware_tk_initialization():
    tk = DPIAwareTk()
    assert isinstance(tk, DPIAwareTk)

@pytest.mark.skipif(os.name != "nt", reason="Test only applicable to Windows systems")
@patch("hidpi_tk.windll.shcore.SetProcessDpiAwareness")
@patch("hidpi_tk.windll.shcore.GetScaleFactorForDevice", return_value=150)
@patch("hidpi_tk.windll.user32.MonitorFromWindow", return_value=0)
@patch("hidpi_tk.windll.shcore.GetDpiForMonitor")
def test_fix_hidpi_windows(mock_get_dpi_for_monitor, mock_monitor_from_window, mock_get_scale_factor, mock_set_dpi_awareness):
    root = MagicMock()
    root.winfo_id.return_value = 1
    
    fix_HiDPI(root)

    # Check if SetProcessDpiAwareness was called with expected arguments
    mock_set_dpi_awareness.assert_called_once_with(2)
    
    # Check if GetScaleFactorForDevice was called to get scale factor for monitor
    mock_get_scale_factor.assert_called_once_with(0)
    
    # Check if GetDpiForMonitor was called to retrieve monitor DPI
    mock_get_dpi_for_monitor.assert_called_once()

@pytest.mark.skipif(os.name != "nt", reason="Test only applicable to Windows systems")
@patch("hidpi_tk.windll.user32.SetProcessDPIAware")
def test_fix_hidpi_windows_legacy(mock_set_dpi_aware):
    root = MagicMock()
    root.winfo_id.return_value = 1
    
    with patch("hidpi_tk.windll.shcore.SetProcessDpiAwareness", side_effect=Exception):
        fix_HiDPI(root)
    
    mock_set_dpi_aware.assert_called_once()

@pytest.mark.skipif(os.name != "nt", reason="Test only applicable to Windows systems")
@patch("hidpi_tk.windll.shcore.SetProcessDpiAwareness", side_effect=OSError)
def test_fix_hidpi_windows_with_oserror(mock_set_dpi_awareness):
    root = MagicMock()
    root.winfo_id.return_value = 1
    
    fix_HiDPI(root)
    
    mock_set_dpi_awareness.assert_called_once()
