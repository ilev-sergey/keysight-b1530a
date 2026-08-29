from pathlib import Path

import keysight_b1530a


def test_lib_files_included():
    """wgfmu.dll and wgfmu.h should be included in the installed package."""
    package_dir = Path(keysight_b1530a.__file__).parent
    assert (package_dir / "lib" / "wgfmu.dll").exists()
    assert (package_dir / "lib" / "wgfmu.h").exists()
