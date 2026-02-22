"""Tests for src.shell.ui.icon_loader — load_icon(), _tint_icon(), and cache."""

import pytest
from unittest.mock import patch, MagicMock

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize

from src.shell.ui import icon_loader
from src.shell.ui.icon_loader import load_icon, _tint_icon, _icon_cache


@pytest.fixture(autouse=True)
def clear_icon_cache():
    """Reset the icon cache before every test."""
    _icon_cache.clear()
    yield
    _icon_cache.clear()


# ── load_icon: QIcon input ────────────────────────────────────────────

class TestLoadIconQIconInput:
    def test_load_icon_returns_qicon_passthrough(self, qapp):
        """QIcon input returned as-is when no color/size."""
        icon = QIcon()
        result = load_icon(icon)
        assert result is icon

    @patch("src.shell.ui.icon_loader._tint_icon")
    def test_load_icon_tints_qicon_when_color_and_size(self, mock_tint, qapp):
        """QIcon + color + size → calls _tint_icon."""
        icon = QIcon()
        size = QSize(24, 24)
        tinted = QIcon()
        mock_tint.return_value = tinted

        result = load_icon(icon, color="#FF0000", size=size)

        mock_tint.assert_called_once_with(icon, "#FF0000", size)
        assert result is tinted

    def test_load_icon_qicon_no_tint_without_size(self, qapp):
        """QIcon + color but no size → returns the original icon untinted."""
        icon = QIcon()
        result = load_icon(icon, color="#FF0000")
        assert result is icon


# ── load_icon: invalid input ─────────────────────────────────────────

class TestLoadIconInvalidInput:
    def test_load_icon_none_input(self, qapp):
        """None → empty QIcon."""
        result = load_icon(None)
        assert isinstance(result, QIcon)
        assert result.isNull()

    def test_load_icon_empty_string(self, qapp):
        """Empty string → empty QIcon."""
        result = load_icon("")
        assert isinstance(result, QIcon)
        assert result.isNull()

    def test_load_icon_non_string_non_qicon(self, qapp):
        """Non-string, non-QIcon (e.g. int) → empty QIcon."""
        result = load_icon(123)
        assert isinstance(result, QIcon)
        assert result.isNull()


# ── load_icon: file path ─────────────────────────────────────────────

class TestLoadIconFilePath:
    def test_load_icon_file_path(self, qapp, tmp_icon_file):
        """Existing file path → returns a QIcon."""
        result = load_icon(tmp_icon_file)

        assert isinstance(result, QIcon)
        # The file exists and is a valid PNG, so the icon should load
        assert not result.isNull()


# ── load_icon: qtawesome string ───────────────────────────────────────

class TestLoadIconQtaString:
    @patch("src.shell.ui.icon_loader.os.path.exists", return_value=False)
    @patch("src.shell.ui.icon_loader.qta")
    def test_load_icon_qta_string(self, mock_qta, mock_exists, qapp):
        """qtawesome string → qta.icon(...) called."""
        fake_icon = MagicMock(spec=QIcon)
        fake_icon.isNull.return_value = False
        mock_qta.icon.return_value = fake_icon

        result = load_icon("fa5s.cog")

        mock_qta.icon.assert_called_once_with("fa5s.cog")
        assert result is fake_icon

    @patch("src.shell.ui.icon_loader.os.path.exists", return_value=False)
    @patch("src.shell.ui.icon_loader.qta")
    def test_load_icon_qta_string_with_color(self, mock_qta, mock_exists, qapp):
        """qtawesome + color → qta.icon(source, color=color)."""
        fake_icon = MagicMock(spec=QIcon)
        fake_icon.isNull.return_value = False
        mock_qta.icon.return_value = fake_icon

        result = load_icon("fa5s.cog", color="#FFFFFF")

        mock_qta.icon.assert_called_once_with("fa5s.cog", color="#FFFFFF")
        assert result is fake_icon

    @patch("src.shell.ui.icon_loader.os.path.exists", return_value=False)
    @patch("src.shell.ui.icon_loader.qta")
    def test_load_icon_qta_failure(self, mock_qta, mock_exists, qapp):
        """Invalid qta string → empty QIcon."""
        mock_qta.icon.side_effect = Exception("not found")

        result = load_icon("fa5s.nonexistent")

        assert isinstance(result, QIcon)
        assert result.isNull()


# ── load_icon: cache ──────────────────────────────────────────────────

class TestLoadIconCache:
    @patch("src.shell.ui.icon_loader.os.path.exists", return_value=False)
    @patch("src.shell.ui.icon_loader.qta")
    def test_load_icon_cache_hit(self, mock_qta, mock_exists, qapp):
        """Second call with same args returns cached icon."""
        fake_icon = MagicMock(spec=QIcon)
        fake_icon.isNull.return_value = False
        mock_qta.icon.return_value = fake_icon

        result1 = load_icon("fa5s.cog")
        result2 = load_icon("fa5s.cog")

        assert result1 is result2
        # qta.icon called only once — second call served from cache
        mock_qta.icon.assert_called_once()

    @patch("src.shell.ui.icon_loader.os.path.exists", return_value=False)
    @patch("src.shell.ui.icon_loader.qta")
    def test_load_icon_cache_miss_different_color(self, mock_qta, mock_exists, qapp):
        """Different color → separate cache entry."""
        icon_a = MagicMock(spec=QIcon)
        icon_a.isNull.return_value = False
        icon_b = MagicMock(spec=QIcon)
        icon_b.isNull.return_value = False
        mock_qta.icon.side_effect = [icon_a, icon_b]

        result1 = load_icon("fa5s.cog", color="#FFFFFF")
        result2 = load_icon("fa5s.cog", color="#000000")

        assert result1 is not result2
        assert mock_qta.icon.call_count == 2


# ── _tint_icon ────────────────────────────────────────────────────────

class TestTintIcon:
    def test_tint_icon_applies_color(self, qapp):
        """_tint_icon creates a tinted icon (non-null result)."""
        # Create a real 16x16 pixmap so painting succeeds
        pixmap = QPixmap(16, 16)
        pixmap.fill()
        source_icon = QIcon(pixmap)
        size = QSize(16, 16)

        result = _tint_icon(source_icon, "#FF0000", size)

        assert isinstance(result, QIcon)
        assert not result.isNull()

    def test_tint_icon_null_pixmap(self, qapp):
        """Null pixmap → returns original icon."""
        icon = QIcon()  # empty icon → null pixmap
        size = QSize(16, 16)

        result = _tint_icon(icon, "#FF0000", size)

        # Should return the original icon unchanged
        assert result is icon

    @patch("src.shell.ui.icon_loader.QPainter")
    def test_tint_icon_exception(self, MockPainter, qapp):
        """Painting failure → returns original icon."""
        MockPainter.side_effect = Exception("paint error")

        pixmap = QPixmap(16, 16)
        pixmap.fill()
        icon = QIcon(pixmap)
        size = QSize(16, 16)

        result = _tint_icon(icon, "#FF0000", size)

        assert result is icon
