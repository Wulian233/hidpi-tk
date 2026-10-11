Changes
=======

1.4.1 (2026-10-11)
------------------

- Fixed importing the library on Linux and macOS by loading Windows-specific ctypes APIs only on Windows.

1.4.0 (2026-02-22)
------------------

- Added automatic DPI awareness for `Toplevel` windows, inheriting scaling from the root window.
- Internal refactoring to support negative window positions (`+X+Y` with negative values).

1.3.1 (2025-10-26)
------------------

- Fix geometry "+X+Y" format
(Contributed by ChenDennis2013 in `this PR <https://github.com/Wulian233/hidpi-tk/issues/21>`_)

1.3.0 (2025-08-10)
------------------

- The ``geometry`` function's "WxH" format now scales correctly on high-DPI displays.
(Contributed by ChenDennis2013 in `this PR <https://github.com/Wulian233/hidpi-tk/issues/19>`_)

- The ``place`` layout manager's coordinates are no longer incorrectly scaled, see `this issue <https://github.com/Wulian233/hidpi-tk/issues/20>`_ for more details.


1.2.0 (2025-08-06)
------------------

- Fix window scaling

1.1.0 (2025-07-05)
------------------

- Now does not depend on idlelib
- Added more adaptation optimizations
- Port to pyproject.toml build system

1.0.0 (2024-10-05)
------------------

- Initial release
