# Architecture

## Layer Diagram

```
Runner (run_mainwindow.py / run_custom_folders.py)
  │
  │  Creates: app_descriptors, widget_factory
  │
  ▼
AppShell (src/shell/AppShell.py)
  │  QWidget — main window, stacked widget, header
  │  DI: app_descriptors, widget_factory, optional ui_factory
  │
  ▼
FolderLauncher (src/shell/FolderLauncher.py)
  │  QWidget — grid layout of folder widgets
  │  Reads ShellConfig for folder definitions
  │
  ▼
FolderController (src/shell/folder_controller.py)
  │  QObject — business logic per folder
  │  Owns: ExpandedViewManager, FloatingIconManager, OverlayManager
  │
  ▼
Manager Layer
  ├── ExpandedViewManager  → ExpandedFolderView
  ├── FloatingIconManager  → FloatingFolderIcon
  └── OverlayManager       → FolderOverlay
```

## Dependency Injection Contract

`AppShell.__init__` accepts three arguments:

| Parameter          | Type                            | Required | Description                                      |
|--------------------|---------------------------------|----------|--------------------------------------------------|
| `app_descriptors`  | `List[AppDescriptor]`           | Yes      | List of apps with name, icon, and folder_id      |
| `widget_factory`   | `Callable[[str], QWidget]`      | Yes      | Given an app name, returns the app widget         |
| `ui_factory`       | `UIFactory` (protocol)          | No       | Swappable UI component factory (defaults to `MaterialUIFactory`) |

The shell never imports or references any plugin system, business logic, or application code. It only knows about `AppDescriptor` data and the factory callable.

## Protocols (`src/shell/interfaces.py`)

The project defines 10 protocols using `typing.Protocol` with `@runtime_checkable`:

### UI Component Protocols

```python
class IMenuIcon(Protocol):
    icon_label: str
    icon_path: object
    icon_text: str
    callback: Optional[Callable]

class IFolderWidget(Protocol):
    ID: int
    folder_name: str
    buttons: list
    translate_fn: Optional[Callable]

    def add_app(self, app_name: str, icon_path, callback=None) -> None: ...
    def set_grayed_out(self, grayed_out: bool) -> None: ...
    def update_title_label(self, message=None) -> None: ...
    def update_folder_preview(self) -> None: ...

class IExpandedView(Protocol):
    def add_app_icon(self, widget, row: int, col: int) -> None: ...
    def fade_in(self, center_pos) -> None: ...
    def fade_out(self) -> None: ...
    def show_close_app_button(self) -> None: ...
    def hide_close_app_button(self) -> None: ...

class IOverlay(Protocol):
    def fade_in(self) -> None: ...
    def fade_out(self) -> None: ...
    def setStyleSheet(self, style: str) -> None: ...
    def resize(self, *args) -> None: ...

class IFloatingIcon(Protocol):
    def show_with_animation(self) -> None: ...
    def hide_with_animation(self) -> None: ...
    def move(self, x: int, y: int) -> None: ...
```

### Manager Protocols

```python
class IExpandedViewManager(Protocol):
    def show_expanded_view(self, folder_name, overlay_parent,
                           on_close, on_app_selected,
                           on_minimize, on_close_app): ...
    def populate_apps(self, buttons: list) -> None: ...
    def fade_in(self, center_pos) -> None: ...
    def fade_out(self) -> None: ...
    def show_close_button(self) -> None: ...
    def hide_close_button(self) -> None: ...

class IFloatingIconManager(Protocol):
    def show_floating_icon(self, folder_name: str,
                           on_click_callback: Callable) -> None: ...
    def hide_floating_icon(self) -> None: ...

class IOverlayManager(Protocol):
    def show_overlay(self): ...
    def hide_overlay(self) -> None: ...
    def set_style(self, style: str) -> None: ...
```

### UIFactory Protocol

```python
class UIFactory(Protocol):
    def create_folder_widget(self, ID: int, folder_name: str) -> IFolderWidget: ...
    def create_expanded_view_manager(self, folder_widget) -> IExpandedViewManager: ...
    def create_floating_icon_manager(self, folder_widget) -> IFloatingIconManager: ...
    def create_overlay_manager(self, folder_widget, overlay_parent,
                               overlay_callback) -> IOverlayManager: ...
```

## UIFactory Pattern

The default implementation is `MaterialUIFactory` (`src/shell/ui/material/factory.py`). To implement a custom UI factory:

```python
from src.shell.ui.material.managers.expanded_view_manager import ExpandedViewManager
from src.shell.ui.material.managers.floating_icon_manager import FloatingIconManager
from src.shell.ui.material.managers.overlay_manager import OverlayManager


class MyCustomUIFactory:
    """Custom UI factory — must implement 4 methods."""

    def create_folder_widget(self, ID, folder_name):
        # Return any widget satisfying IFolderWidget protocol
        return MyCustomFolderWidget(ID, folder_name)

    def create_expanded_view_manager(self, folder_widget):
        # Return object satisfying IExpandedViewManager
        return ExpandedViewManager(folder_widget)  # or custom

    def create_floating_icon_manager(self, folder_widget):
        return FloatingIconManager(folder_widget)  # or custom

    def create_overlay_manager(self, folder_widget, overlay_parent, overlay_callback):
        return OverlayManager(folder_widget, overlay_parent, overlay_callback)
```

Pass it to the shell:

```python
shell = AppShell(
    app_descriptors=descriptors,
    widget_factory=factory,
    ui_factory=MyCustomUIFactory()
)
```

## Signal Flow

### Folder Click → App Launch

```
User clicks folder preview
  │
  ▼
FolderWidget.clicked signal
  │
  ▼
FolderController.handle_folder_click()
  ├── OverlayManager.show_overlay()        → FolderOverlay.fade_in()
  ├── ExpandedViewManager.show_expanded_view()  → creates ExpandedFolderView
  ├── ExpandedViewManager.populate_apps()  → creates MenuIcon copies in 4-col grid
  └── ExpandedViewManager.fade_in()        → combined fade + scale animation
  │
  ▼
User clicks app icon (MenuIcon.button_clicked)
  │
  ▼
ExpandedFolderView.on_app_clicked(app_name)
  ├── Emits app_selected signal
  ├── Shows close_app_button
  └── Emits minimize_requested signal
  │
  ▼
FolderController.handle_app_selected(app_name)
  ├── Updates FolderState (app_running=True)
  ├── Emits app_selected signal → FolderLauncher → AppShell
  ├── ExpandedViewManager.show_close_button()
  ├── OverlayManager.hide_overlay()
  └── QTimer.singleShot(300, minimize_to_floating_icon)
  │
  ▼
AppShell.on_app_selected(app_name)
  └── AppShell.show_app(app_name)
      ├── Creates widget via widget_factory(app_name) (or reuses cached)
      ├── Connects app_closed signal
      └── stacked_widget.setCurrentIndex(1)
```

### Close App → Return to Folders

```
User presses ESC  or  FloatingFolderIcon clicked → expanded view → "BACK" button
  │
  ▼
AppShell.close_current_app() → close_all_apps()
  ├── Calls clean_up() on each cached widget
  ├── Removes from stacked widget
  ├── Clears running_widgets cache
  └── stacked_widget.setCurrentIndex(0)  → shows folders page
```

## Plugin Integration Seam

For projects with a plugin system, `build_app_registry()` in `src/shell/app_registry.py` bridges the gap:

```python
from src.shell.app_registry import build_app_registry

# plugin_manager: has get_loaded_plugin_names() and get_plugin(name)
# widget_factory_instance: has create_widget(app_name)
descriptors, factory = build_app_registry(plugin_manager, widget_factory_instance)

shell = AppShell(app_descriptors=descriptors, widget_factory=factory)
```

This function reads `_json_metadata` from each plugin (expecting `folder_id` and `icon_str` keys) and wraps the widget factory into a simple callable. The shell remains plugin-agnostic.

---

Previous: [Getting Started](./01-getting-started.md) | Next: [Configuration](./03-configuration.md)
