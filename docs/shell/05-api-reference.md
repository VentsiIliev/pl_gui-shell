# API Reference

Organized by module path. Each class lists its constructor signature, signals, and public methods.

---

## `src.shell.app_descriptor`

### `AppDescriptor`

```python
@dataclass
class AppDescriptor:
    name: str       # App display name
    icon_str: str   # QtAwesome string, e.g. "fa5s.cog"
    folder_id: int  # Maps to FolderDefinition.id
```

---

## `src.shell.app_registry`

### `build_app_registry(plugin_manager, widget_factory_instance)`

```python
def build_app_registry(
    plugin_manager,            # has get_loaded_plugin_names(), get_plugin(name)
    widget_factory_instance    # has create_widget(app_name)
) -> Tuple[List[AppDescriptor], Callable[[str], QWidget]]
```

Returns `(descriptors, factory)`. Reads `_json_metadata` dict from each plugin for `folder_id` (default `1`) and `icon_str` (default `"fa5s.users-cog"`).

---

## `src.shell.base_app_widget.AppWidget`

### `AppWidget(QWidget)`

```python
def __init__(self, app_name: str, parent=None)
```

| Signal | Type |
|--------|------|
| `app_closed` | `pyqtSignal()` |

| Method | Signature | Returns |
|--------|-----------|---------|
| `close_app` | `() -> None` | Emits `app_closed` |
| `clean_up` | `() -> None` | Override for cleanup |

---

## `src.shell.ui.LanguageSelectorWidget`

### `LanguageSelectorWidget(QComboBox)`

```python
def __init__(self, languages: Optional[List[Tuple[str, str]]] = None, parent=None)
```

| Parameter | Type | Default |
|-----------|------|---------|
| `languages` | `list[tuple[str, str]]` or `None` | `None` — selector hidden; pass a list to show it |

| Signal | Type |
|--------|------|
| `languageChanged` | `pyqtSignal(str)` — emits language code (e.g. `"en"`) |

| Method | Signature | Description |
|--------|-----------|-------------|
| `updateSelectedLang` | `() -> None` | Sync dropdown to `current_language` |

---

## `src.shell.ui.Header`

### `Header(QFrame)`

```python
def __init__(
    self,
    screen_width: int,
    screen_height: int,
    toggle_menu_callback: Optional[Callable[[], None]],
    dashboard_button_callback: Optional[Callable[[], None]],
    languages: Optional[list] = None
)
```

| Signal | Type |
|--------|------|
| `user_account_clicked` | `pyqtSignal()` |
| `fps_updated` | `pyqtSignal(float)` |

| Method | Signature | Description |
|--------|-----------|-------------|
| `toggle_power` | `() -> None` | Toggle power state |
| `update_fps_label` | `(fps: float) -> None` | Update FPS display |
| `handle_language_change` | `(language_code: str) -> None` | Log language change |
| `on_user_account_clicked` | `() -> None` | Emit `user_account_clicked` |

---

## `src.shell.shell_config`

### `FolderDefinition`

```python
@dataclass
class FolderDefinition:
    id: int
    name: str
    translation_key: str
    display_name: str
```

| Method | Signature | Returns |
|--------|-----------|---------|
| `get_translate_fn` | `() -> Callable[[str], str]` | Translation function |

### `ShellConfig`

All methods are `@classmethod`.

| Method | Signature | Returns |
|--------|-----------|---------|
| `initialize_defaults` | `()` | `None` |
| `add_folder` | `(folder: FolderDefinition, override_defaults: bool = False)` | `None` |
| `remove_folder` | `(folder_id: int)` | `bool` |
| `update_folder` | `(folder_id: int, **updates)` | `bool` |
| `clear_folders` | `()` | `None` |
| `reset_to_defaults` | `()` | `None` |
| `get_folders` | `()` | `list[FolderDefinition]` |
| `get_folder_by_id` | `(folder_id: int)` | `Optional[FolderDefinition]` |
| `get_all_folder_ids` | `()` | `list[int]` |
| `folder_exists` | `(folder_id: int)` | `bool` |
| `get_folders_with_apps` | `(filtered_apps: dict[int, list])` | `list[FolderDefinition]` |

### `create_custom_folder`

```python
def create_custom_folder(
    folder_id: int,
    name: str,
    display_name: Optional[str] = None,
    translation_key: Optional[str] = None
) -> FolderDefinition
```

### Constants

```python
FOLDER_WORK = 1
FOLDER_SERVICE = 2
FOLDER_ADMINISTRATION = 3
```

---

## `src.shell.interfaces`

Ten `@runtime_checkable` protocols. See [Architecture — Protocols](./02-architecture.md#protocols-srcshellinterfacespy) for full signatures.

| Protocol | Key Methods |
|----------|-------------|
| `IAppWidget` | Attributes: `app_name`; Methods: `close_app()`, `on_language_changed()`, `clean_up()` |
| `IMenuIcon` | Attributes: `icon_label`, `icon_path`, `icon_text`, `callback` |
| `IFolderWidget` | `add_app()`, `set_grayed_out()`, `update_title_label()`, `update_folder_preview()` |
| `IExpandedView` | `add_app_icon()`, `fade_in()`, `fade_out()`, `show_close_app_button()`, `hide_close_app_button()` |
| `IOverlay` | `fade_in()`, `fade_out()`, `setStyleSheet()`, `resize()` |
| `IFloatingIcon` | `show_with_animation()`, `hide_with_animation()`, `move()` |
| `IExpandedViewManager` | `show_expanded_view()`, `populate_apps()`, `fade_in()`, `fade_out()`, `show_close_button()`, `hide_close_button()` |
| `IFloatingIconManager` | `show_floating_icon()`, `hide_floating_icon()` |
| `IOverlayManager` | `show_overlay()`, `hide_overlay()`, `set_style()` |
| `UIFactory` | `create_folder_widget()`, `create_expanded_view_manager()`, `create_floating_icon_manager()`, `create_overlay_manager()` |

---

## `src.shell.AppShell`

### `AppShell(QWidget)`

```python
def __init__(
    self,
    app_descriptors: List[AppDescriptor],
    widget_factory: Callable[[str], QWidget],
    ui_factory=None,   # Optional[UIFactory], defaults to MaterialUIFactory
    languages: list = None  # Optional list of (code, display_name) tuples; None hides the selector
)
```

| Signal | Type |
|--------|------|
| `start_requested` | `pyqtSignal()` |
| `stop_requested` | `pyqtSignal()` |
| `pause_requested` | `pyqtSignal()` |

| Method | Signature | Returns | Description |
|--------|-----------|---------|-------------|
| `show_app` | `(app_name: str)` | `QWidget` | Create or reuse app widget, show in stacked widget |
| `create_app` | `(app_name: str)` | `QWidget` | Delegate to `widget_factory` |
| `close_current_app` | `()` | `None` | Close all apps, return to folders |
| `close_all_apps` | `()` | `None` | Clean up all cached widgets |
| `retranslate` | `()` | `None` | Update folder titles on language change |
| `lock` | `()` | `None` | Disable the entire GUI |
| `unlock` | `()` | `None` | Re-enable the GUI |
| `cleanup` | `()` | `None` | Clean up on close |

---

## `src.shell.FolderLauncher`

### `FolderConfig`

```python
@dataclass
class FolderConfig:
    ID: int
    name: str
    apps: list                   # [[app_name, icon_str], ...]
    translate_fn: Callable = None
```

### `FolderLauncher(QWidget)`

```python
def __init__(self, parent=None, folder_config_list=None,
             main_window=None, ui_factory=None)
```

| Signal | Type | Description |
|--------|------|-------------|
| `folder_opened` | `pyqtSignal(object)` | FolderController that opened |
| `folder_closed` | `pyqtSignal()` | Any folder closed |
| `app_selected` | `pyqtSignal(str)` | App name selected |
| `close_current_app_requested` | `pyqtSignal()` | Close app request |

| Method | Signature | Returns |
|--------|-----------|---------|
| `get_folders` | `()` | `list[FolderController]` |
| `get_folder_controllers` | `()` | `list[FolderController]` |
| `get_folder_widgets` | `()` | `list[FolderWidget]` |
| `enable_folder_by_id` | `(ID: int)` | `None` |
| `disable_folder_by_id` | `(ID: int)` | `None` |

---

## `src.shell.folder_controller`

### `FolderState`

```python
@dataclass
class FolderState:
    is_open: bool = False
    is_grayed_out: bool = False
    app_running: bool = False
    current_app_name: Optional[str] = None
```

### `FolderController(QObject)`

```python
def __init__(self, folder_widget, main_window=None,
             ui_factory=None, parent=None)
```

| Signal | Type |
|--------|------|
| `folder_opened` | `pyqtSignal()` |
| `folder_closed` | `pyqtSignal()` |
| `app_selected` | `pyqtSignal(str)` |
| `close_current_app_signal` | `pyqtSignal()` |

| Method | Signature | Description |
|--------|-----------|-------------|
| `handle_folder_click` | `()` | Toggle folder open/close |
| `open_folder` | `()` | Show overlay + expanded view |
| `close_folder` | `()` | Hide all, reset state |
| `handle_app_selected` | `(app_name: str)` | Set running state, emit signal, minimize |
| `handle_close_app` | `()` | Reset state, emit close signal |
| `minimize_to_floating_icon` | `()` | Hide overlay/view, show FAB |
| `restore_from_floating_icon` | `()` | Show overlay/view, hide FAB |
| `handle_outside_click` | `()` | Minimize or close based on state |
| `set_disabled` | `(disabled: bool)` | Update grayed out state |
| `set_main_window` | `(main_window)` | Set parent reference |

---

## `src.shell.ui.icon_loader`

### `load_icon`

```python
def load_icon(source, color=None, size=None) -> QIcon
```

See [UI Components — Icon Loading](./04-ui-components.md#icon-loading-srcshelluiicon_loaderpy).

---

## `src.shell.ui.styles`

Module-level constants. See [UI Components — Design Tokens](./04-ui-components.md#design-tokens-srcshellui-stylespy) for the full table.

---

## `src.shell.ui.material.MaterialUIFactory`

### `MaterialUIFactory`

```python
class MaterialUIFactory:
    def create_folder_widget(self, ID: int, folder_name: str) -> FolderWidget
    def create_expanded_view_manager(self, folder_widget) -> ExpandedViewManager
    def create_floating_icon_manager(self, folder_widget) -> FloatingIconManager
    def create_overlay_manager(self, folder_widget, overlay_parent, overlay_callback) -> OverlayManager
```

---

## `src.shell.ui.material.folder_widget`

### `LayoutManager`

```python
def __init__(self, folder_widget: FolderWidget)
```

| Method | Description |
|--------|-------------|
| `setup_responsive_sizing()` | Set min/max size and size policy |
| `update_main_layout_margins()` | Dynamic margin based on width |
| `update_header_layout_spacing()` | Set header spacing to 16px |
| `update_preview_layout_margins()` | Dynamic preview margins |
| `calculate_icon_size()` | Compute icon size from preview dimensions |
| `update_typography()` | Scale font size based on width |
| `handle_resize_event()` | Recalculate layout on resize (debounced) |

### `FolderWidget(QFrame)`

See [UI Components — FolderWidget](./04-ui-components.md#folderwidget-srcshellui-materialfolder_widgetpy).

---

## `src.shell.ui.material.menu_icon`

### `MenuIcon(QPushButton)`

See [UI Components — MenuIcon](./04-ui-components.md#menuicon-srcshellui-materialmenu_iconpy).

---

## `src.shell.ui.material.expanded_view`

### `ExpandedFolderView(QFrame)`

See [UI Components — ExpandedFolderView](./04-ui-components.md#expandedfolderview-srcshellui-materialexpanded_viewpy).

---

## `src.shell.ui.material.overlay`

### `FolderOverlay(QWidget)`

See [UI Components — FolderOverlay](./04-ui-components.md#folderoverlay-srcshellui-materialoverlaypy).

---

## `src.shell.ui.material.floating_icon`

### `FloatingFolderIcon(QPushButton)`

See [UI Components — FloatingFolderIcon](./04-ui-components.md#floatingfoldericon-srcshellui-materialfloating_iconpy).

---

## `src.shell.ui.material.animation`

### `MaterialDesignTiming`

| Constant | ms |
|----------|----|
| `FAST` | 100 |
| `SHORT` | 150 |
| `MEDIUM` | 300 |
| `LONG` | 500 |
| `EXTRA_LONG` | 700 |

### `MaterialDesignEasing`

| Constant | Curve |
|----------|-------|
| `STANDARD` | `OutCubic` |
| `EMPHASIZED` | `OutQuart` |
| `DECELERATED` | `OutCubic` |
| `ACCELERATED` | `InCubic` |
| `LINEAR` | `Linear` |

### `AnimationManager(QObject)`

See [UI Components — AnimationManager](./04-ui-components.md#animationmanager-srcshellui-materialanimationpy).

### `AnimationPatterns`

| Static Method | Signature |
|---------------|-----------|
| `folder_open_animation` | `(expanded_view_widget, center_pos) -> AnimationManager` |
| `folder_close_animation` | `(expanded_view_widget) -> AnimationManager` |
| `floating_icon_transition` | `(floating_icon_widget, show: bool) -> AnimationManager` |

### Utility Functions

| Function | Signature |
|----------|-----------|
| `create_material_entrance_animation` | `(widget, center_pos, duration?, callback?) -> AnimationManager` |
| `create_material_exit_animation` | `(widget, duration?, callback?) -> AnimationManager` |
| `create_fab_animation` | `(widget, show=True, callback?) -> AnimationManager` |

---

## `src.shell.ui.material.managers.expanded_view_manager`

### `ExpandedViewManager`

```python
def __init__(self, parent_widget)
```

| Method | Signature |
|--------|-----------|
| `show_expanded_view` | `(folder_name, overlay_parent, on_close, on_app_selected, on_minimize, on_close_app) -> ExpandedFolderView` |
| `populate_apps` | `(buttons: list) -> None` |
| `fade_in` | `(center_pos) -> None` |
| `fade_out` | `() -> None` |
| `show_close_button` | `() -> None` |
| `hide_close_button` | `() -> None` |

---

## `src.shell.ui.material.managers.floating_icon_manager`

### `FloatingIconManager`

```python
def __init__(self, parent_widget)
```

| Method | Signature |
|--------|-----------|
| `show_floating_icon` | `(folder_name: str, on_click_callback: Callable) -> None` |
| `hide_floating_icon` | `() -> None` |

---

## `src.shell.ui.material.managers.overlay_manager`

### `OverlayManager`

```python
def __init__(self, parent_widget, overlay_parent, overlay_callback)
```

| Method | Signature |
|--------|-----------|
| `show_overlay` | `() -> Optional[FolderOverlay]` |
| `hide_overlay` | `() -> None` |
| `set_style` | `(style: str) -> None` |

---

Previous: [UI Components](./04-ui-components.md)
