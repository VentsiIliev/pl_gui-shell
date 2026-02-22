import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon


@pytest.fixture(scope="session")
def qapp():
    """Provide a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def mock_qicon():
    """Return a non-null QIcon mock."""
    icon = MagicMock(spec=QIcon)
    icon.isNull.return_value = False
    return icon


@pytest.fixture
def tmp_icon_file(tmp_path):
    """Create a temporary valid PNG file for file-path tests."""
    # Minimal valid 1x1 PNG
    import struct, zlib

    def _minimal_png():
        signature = b"\x89PNG\r\n\x1a\n"
        ihdr_data = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data) & 0xFFFFFFFF
        ihdr = struct.pack(">I", 13) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc)
        raw = b"\x00\x00\x00\x00"  # filter byte + 1 RGB pixel
        deflated = zlib.compress(raw)
        idat_crc = zlib.crc32(b"IDAT" + deflated) & 0xFFFFFFFF
        idat = struct.pack(">I", len(deflated)) + b"IDAT" + deflated + struct.pack(">I", idat_crc)
        iend_crc = zlib.crc32(b"IEND") & 0xFFFFFFFF
        iend = struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc)
        return signature + ihdr + idat + iend

    icon_file = tmp_path / "test_icon.png"
    icon_file.write_bytes(_minimal_png())
    return str(icon_file)
