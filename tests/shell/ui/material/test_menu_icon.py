"""Tests for src.shell.ui.material.menu_icon — MenuIcon widget."""

import pytest
from unittest.mock import patch, MagicMock

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize


def _make_valid_qicon():
    """Create a real non-null QIcon."""
    pixmap = QPixmap(16, 16)
    pixmap.fill()
    return QIcon(pixmap)


class TestMenuIconSetupContent:
    @patch("src.shell.ui.material.menu_icon.load_icon")
    def test_setup_icon_content_with_valid_icon(self, mock_load_icon, qapp):
        """load_icon returns valid icon → icon set, text cleared."""
        mock_load_icon.return_value = _make_valid_qicon()

        from src.shell.ui.material.menu_icon import MenuIcon
        widget = MenuIcon("Test App", "fa5s.cog")

        assert widget.text() == ""
        mock_load_icon.assert_called()

    @patch("src.shell.ui.material.menu_icon.load_icon")
    def test_setup_icon_content_fallback_text(self, mock_load_icon, qapp):
        """load_icon returns null icon → setup_fallback_text() used."""
        mock_load_icon.return_value = QIcon()  # null icon

        from src.shell.ui.material.menu_icon import MenuIcon
        widget = MenuIcon("My App", "invalid_path")

        assert widget.text() == "MA"


class TestMenuIconFallbackText:
    @patch("src.shell.ui.material.menu_icon.load_icon")
    def test_fallback_text_two_words(self, mock_load_icon, qapp):
        """'My App' → 'MA'."""
        mock_load_icon.return_value = QIcon()

        from src.shell.ui.material.menu_icon import MenuIcon
        widget = MenuIcon("My App", "")

        assert widget.text() == "MA"

    @patch("src.shell.ui.material.menu_icon.load_icon")
    def test_fallback_text_single_word(self, mock_load_icon, qapp):
        """'Settings' → 'SE'."""
        mock_load_icon.return_value = QIcon()

        from src.shell.ui.material.menu_icon import MenuIcon
        widget = MenuIcon("Settings", "")

        assert widget.text() == "SE"

    @patch("src.shell.ui.material.menu_icon.load_icon")
    def test_fallback_text_custom_icon_text(self, mock_load_icon, qapp):
        """Custom icon_text used when provided."""
        mock_load_icon.return_value = QIcon()

        from src.shell.ui.material.menu_icon import MenuIcon
        widget = MenuIcon("My App", "", icon_text="XY")

        assert widget.text() == "XY"


class TestMenuIconSetIconFromPath:
    @patch("src.shell.ui.material.menu_icon.load_icon")
    def test_set_icon_from_path(self, mock_load_icon, qapp):
        """set_icon_from_path updates icon_path and re-calls setup_icon_content."""
        mock_load_icon.return_value = _make_valid_qicon()

        from src.shell.ui.material.menu_icon import MenuIcon
        widget = MenuIcon("Test", "old_path")

        mock_load_icon.reset_mock()
        mock_load_icon.return_value = _make_valid_qicon()
        widget.set_icon_from_path("new_path")

        assert widget.icon_path == "new_path"
        mock_load_icon.assert_called()
