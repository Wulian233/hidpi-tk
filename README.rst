===================
hidpi-tk
===================
.. image:: https://github.com/Wulian233/hidpi-tk/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/Wulian233/hidpi-tk/actions/workflows/ci.yml
.. image:: https://img.shields.io/pypi/v/hidpi-tk.svg
    :target: https://pypi.python.org/pypi/hidpi-tk



``hidpi-tk`` is a Python library designed to enhance Tkinter-based GUI applications
by automatically adjusting DPI scaling and font sizes, particularly for high-DPI monitors.

.. image:: ./screenshot.png
    :target: ./screenshot.png

Features
===================

- **Automatic DPI Scaling**

- **Automatic Font Size Adjustment**

- **Without side-effects**

- **Cross-Platform**

Usage
===========================

To use this library, simply replace the standard ``Tk`` class with ``DPIAwareTk``.
The library will handle DPI and font adjustments automatically:

.. code:: python

    from hidpi_tk import DPIAwareTk
    # from tkinter import Tk

    # root = Tk()
    root = DPIAwareTk()
    # After that use like Tk instance
    root.mainloop()

Details
======================

On Windows systems, it provides full support for scaling on high-DPI monitors,
particularly for Windows 8.1 and newer. For older Windows systems (Vista & Win7)
, it still adjusts DPI and font scaling to an extent.

For other systems, such as macOS and Linux, the operating systems themselves
provide excellent high-DPI support, so this library does not include specific
code for DPI adjustments. However, using this library is still beneficial as
it adjusts font scaling, which makes cross-platform development easier and
more consistent.


License
=======

``hidpi-tk`` library is offered under Apache 2 license.

Thanks
======

The library development is based on `high-dpi-tkinter <https://github.com/not-dev/high-dpi-tkinter>`_.

Added: High-DPI font scaling support, legacy Windows support, bug fixes, and modern Python standards.
