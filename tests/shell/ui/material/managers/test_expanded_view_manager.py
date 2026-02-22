"""Tests for src.shell.ui.material.managers.expanded_view_manager — ExpandedViewManager."""

import pytest
from unittest.mock import patch, MagicMock, call

from src.shell.ui.material.managers.expanded_view_manager import ExpandedViewManager


def _make_mock_button(label="App", path="fa5s.cog", text="", callback=None):
    """Create a mock button with the attributes MenuIcon expects."""
    btn = MagicMock()
    btn.icon_label = label
    btn.icon_path = path
    btn.icon_text = text
    btn.callback = callback
    return btn


class TestPopulateApps:
    def test_populate_apps_no_expanded_view(self):
        """Returns early if no expanded view."""
        mgr = ExpandedViewManager(parent_widget=MagicMock())
        # expanded_view is None by default
        mgr.populate_apps([_make_mock_button()])
        # No error, just returns

    @patch("src.shell.ui.material.managers.expanded_view_manager.MenuIcon")
    def test_populate_apps_empty_buttons(self, MockMenuIcon):
        """Empty list → no icons added."""
        mgr = ExpandedViewManager(parent_widget=MagicMock())
        mgr.expanded_view = MagicMock()

        mgr.populate_apps([])

        MockMenuIcon.assert_not_called()
        mgr.expanded_view.add_app_icon.assert_not_called()

    @patch("src.shell.ui.material.managers.expanded_view_manager.MenuIcon")
    def test_populate_apps_grid_positions(self, MockMenuIcon):
        """4-column layout: divmod positions are correct."""
        mgr = ExpandedViewManager(parent_widget=MagicMock())
        mgr.expanded_view = MagicMock()

        mock_icons = [MagicMock() for _ in range(5)]
        MockMenuIcon.side_effect = mock_icons

        buttons = [_make_mock_button(f"App{i}") for i in range(5)]
        mgr.populate_apps(buttons)

        # Verify grid positions: (0,0), (0,1), (0,2), (0,3), (1,0)
        expected_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)]
        for icon, (row, col) in zip(mock_icons, expected_positions):
            mgr.expanded_view.add_app_icon.assert_any_call(icon, row, col)

    @patch("src.shell.ui.material.managers.expanded_view_manager.MenuIcon")
    def test_populate_apps_passes_qta_color(self, MockMenuIcon):
        """Created MenuIcons get QTA_ICON_COLOR."""
        mgr = ExpandedViewManager(parent_widget=MagicMock())
        mgr.expanded_view = MagicMock()

        mock_icon = MagicMock()
        MockMenuIcon.return_value = mock_icon

        btn = _make_mock_button("Test", "fa5s.star", "TS", None)
        mgr.populate_apps([btn])

        # Verify QTA_ICON_COLOR ("#FFFFFF") was passed
        MockMenuIcon.assert_called_once_with(
            "Test", "fa5s.star", "TS", None, qta_color="#FFFFFF"
        )

    @patch("src.shell.ui.material.managers.expanded_view_manager.MenuIcon")
    def test_populate_apps_connects_signals(self, MockMenuIcon):
        """button_clicked connected to on_app_clicked."""
        mgr = ExpandedViewManager(parent_widget=MagicMock())
        mgr.expanded_view = MagicMock()

        mock_icon = MagicMock()
        MockMenuIcon.return_value = mock_icon

        mgr.populate_apps([_make_mock_button()])

        mock_icon.button_clicked.connect.assert_called_once_with(
            mgr.expanded_view.on_app_clicked
        )
