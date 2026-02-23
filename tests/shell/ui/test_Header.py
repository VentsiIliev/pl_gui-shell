"""Tests for src.shell.ui.Header — Header icon loading with load_icon."""

import pytest
from unittest.mock import patch, MagicMock

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget


class FakeLanguageSelector(QWidget):
    """Minimal stand-in for LanguageSelectorWidget that satisfies addWidget()."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.languageChanged = MagicMock()
        self.languageChanged.connect = MagicMock()


@patch("src.shell.ui.Header.LanguageSelectorWidget", FakeLanguageSelector)
@patch("src.shell.ui.Header.load_icon", return_value=QIcon())
class TestHeaderIconLoading:
    def test_header_dashboard_icon_uses_load_icon(self, mock_load_icon, qapp):
        """Dashboard button icon set via load_icon."""
        from src.shell.ui.Header import Header
        header = Header(800, 600, lambda: None, lambda: None)

        call_args_list = [str(c[0][0]) for c in mock_load_icon.call_args_list]
        assert any("DASHBOARD_BUTTON_SQUARE" in arg for arg in call_args_list)

    def test_header_menu_icon_uses_load_icon(self, mock_load_icon, qapp):
        """Menu button icon set via load_icon."""
        from src.shell.ui.Header import Header
        header = Header(800, 600, lambda: None, lambda: None)

        call_args_list = [str(c[0][0]) for c in mock_load_icon.call_args_list]
        assert any("SANDWICH_MENU" in arg for arg in call_args_list)

    def test_header_power_toggle(self, mock_load_icon, qapp):
        """Toggle switches between ON/OFF icons."""
        from src.shell.ui.Header import Header
        header = Header(800, 600, lambda: None, lambda: None)

        assert header.power_on is False

        mock_load_icon.reset_mock()
        header.toggle_power()

        assert header.power_on is True
        call_args_list = [str(c[0][0]) for c in mock_load_icon.call_args_list]
        assert any("POWER_ON_BUTTON" in arg for arg in call_args_list)

        mock_load_icon.reset_mock()
        header.toggle_power()

        assert header.power_on is False
        call_args_list = [str(c[0][0]) for c in mock_load_icon.call_args_list]
        assert any("POWER_OFF_BUTTON" in arg for arg in call_args_list)

    def test_header_user_account_icon(self, mock_load_icon, qapp):
        """User button uses qtawesome 'fa5s.user'."""
        from src.shell.ui.Header import Header
        header = Header(800, 600, lambda: None, lambda: None)

        call_args_list = [str(c[0][0]) for c in mock_load_icon.call_args_list]
        assert "fa5s.user" in call_args_list
