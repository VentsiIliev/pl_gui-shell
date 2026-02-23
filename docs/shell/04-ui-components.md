# UI Components

All visual components live under `src/shell/ui/` and use Material Design 3 styling.

## Design Tokens (`src/shell/ui/styles.py`)

### Colors

| Constant | Value | Usage |
|----------|-------|-------|
| `PRIMARY` | `#7A5AF8` | Primary brand color |
| `PRIMARY_DARK` | `#6D4ED6` | Pressed state |
| `PRIMARY_HOVER` | `#8B6FF9` | Hover state |
| `SURFACE` | `#FFFFFF` | Card / surface background |
| `BORDER` | `#E4E6F0` | Default border color |
| `ICON_COLOR` | `#905BA9` | Icon tint |
| `QTA_ICON_COLOR` | `#FFFFFF` | QtAwesome mini-preview icon color |
| `BG_COLOR` | `#F6F7FB` | Page background |
| `TEXT_PRIMARY` | `#1D1B20` | Body text |
| `TEXT_DISABLED` | `#9C9A9E` | Disabled text |
| `TEXT_ON_PRIMARY` | `#FFFFFF` | Text on primary surfaces |

### Secondary / Tertiary Variants

| Constant | Value |
|----------|-------|
| `SECONDARY_BG` | `#EDE7F6` |
| `SECONDARY_HOVER` | `#E0D6F0` |
| `SECONDARY_PRESSED` | `#D4CAE4` |
| `TERTIARY_BG` | `#F6F7FB` |
| `TERTIARY_HOVER` | `#EDEEF2` |
| `TERTIARY_PRESSED` | `#E5E6EA` |
| `TERTIARY_TEXT` | `#7D5260` |

### Disabled States

| Constant | Value |
|----------|-------|
| `DISABLED_BG` | `#EDE7F6` |
| `DISABLED_BORDER` | `#B0A7BC` |
| `DISABLED_PREVIEW_BG` | `#F3EDF7` |
| `DISABLED_PREVIEW_BORDER` | `#C4C0CA` |

### Overlay Colors

| Constant | Value |
|----------|-------|
| `OVERLAY_BG` | `rgba(0, 0, 0, 0.5)` |
| `OVERLAY_LIGHT` | `rgba(0, 0, 0, 0.32)` |
| `OVERLAY_SUBTLE` | `rgba(0, 0, 0, 0.16)` |
| `OVERLAY_FAINT` | `rgba(0, 0, 0, 0.05)` |

### Shadows (RGBA tuples for `QColor`)

| Constant | Value | Usage |
|----------|-------|-------|
| `SHADOW_LIGHT` | `(0, 0, 0, 20)` | Default card shadow |
| `SHADOW_MEDIUM` | `(0, 0, 0, 30)` | Expanded view |
| `SHADOW_DARK` | `(0, 0, 0, 40)` | Close button |
| `SHADOW_FAB` | `(0, 0, 0, 60)` | Floating action button |
| `SHADOW_PRIMARY_LIGHT` | `(122, 90, 248, 30)` | Preview frame |
| `SHADOW_PRIMARY` | `(122, 90, 248, 40)` | Icon default |
| `SHADOW_PRIMARY_HOVER` | `(122, 90, 248, 60)` | Icon hover |

### Size Constants

| Constant | Value |
|----------|-------|
| `BUTTON_SIZE` | `60` |
| `ICON_SIZE` | `26` |

### Stylesheet Constants

`NORMAL_STYLE`, `PRIMARY_STYLE`, `ACTIVE_STYLE` — QPushButton stylesheets.
`DIALOG_BUTTON_STYLE`, `TAB_WIDGET_STYLE` — Dialog and tab widget stylesheets.

---

## Icon Loading (`src/shell/ui/icon_loader.py`)

### `load_icon(source, color=None, size=None) -> QIcon`

Unified icon loader with built-in cache.

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | `QIcon`, `str`, or any | QIcon passthrough, file path, or qtawesome string (e.g. `"fa5s.cog"`) |
| `color` | `str` or `None` | Optional tint color (e.g. `"#FFFFFF"`) |
| `size` | `QSize` or `None` | Required when tinting a `QIcon` object |

**Resolution order:**
1. If `source` is a `QIcon` — return it (optionally tinted).
2. If `source` is a file path that exists — load as `QIcon` from file.
3. Otherwise — try `qtawesome.icon(source, color=color)`.
4. On failure — return empty `QIcon()`.

Results are cached by `(source, color)` key in the module-level `_icon_cache` dict.

### `_tint_icon(icon, color, size) -> QIcon`

Internal helper. Extracts a pixmap from `icon`, fills a blank pixmap with `color`, composites using `DestinationIn` mode, and returns a new `QIcon`.

---

## FolderWidget (`src/shell/ui/material/folder_widget.py`)

Material Design 3 folder card. Extends `QFrame`.

### Constructor

```python
FolderWidget(ID: int, folder_name: str = "Apps", parent=None)
```

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `clicked` | `pyqtSignal()` | Emitted when the folder preview is clicked |
| `outside_clicked` | `pyqtSignal()` | Emitted on outside click |

### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `ID` | `int` | Folder identifier |
| `folder_name` | `str` | Display name |
| `buttons` | `list[MenuIcon]` | Stored app icons |
| `is_grayed_out` | `bool` | Current disabled state |
| `translate_fn` | `Callable` or `None` | Translation callback |
| `layout_manager` | `LayoutManager` | Handles responsive sizing |

### Methods

| Method | Description |
|--------|-------------|
| `add_app(app_name, icon_path="", callback=None)` | Create a `MenuIcon` and append to `buttons` |
| `set_grayed_out(grayed_out: bool)` | Toggle disabled visual state |
| `update_title_label(message=None)` | Re-translate folder title via `translate_fn` |
| `update_folder_preview()` | Rebuild the 2x2 preview grid with first 4 app icons |

### LayoutManager

Internal responsive layout helper. Manages sizes (min 300x340, max 480x520), margins, spacing, typography scaling, and a debounced resize timer.

---

## MenuIcon (`src/shell/ui/material/menu_icon.py`)

Material Design 3 app icon button. Extends `QPushButton`.

### Constructor

```python
MenuIcon(icon_label: str, icon_path, icon_text: str = "",
         callback=None, parent=None, qta_color=None)
```

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `button_clicked` | `pyqtSignal(str)` | Emits `icon_label` on click |

### Key Methods

| Method | Description |
|--------|-------------|
| `setup_icon_content()` | Load icon via `load_icon()`, fallback to text |
| `setup_fallback_text()` | Show 2-letter abbreviation from app name |
| `set_icon_from_path(icon_path)` | Update icon dynamically |
| `set_material_style(variant)` | Apply `"primary"`, `"secondary"`, or `"tertiary"` style |
| `set_material_size(variant)` | Apply `"compact"` (80px), `"standard"` (112px), or `"large"` (144px) |

### Style Variants

| Variant | Background | Text Color |
|---------|-----------|------------|
| `primary` | `#7A5AF8` | white |
| `secondary` | `#EDE7F6` | `#7A5AF8` |
| `tertiary` | `#F6F7FB` | `#7D5260` |

### Size Variants

| Variant | Size | Min Touch Target |
|---------|------|-----------------|
| `compact` | 80x80 | 48x48 |
| `standard` | 112x112 | 48x48 |
| `large` | 144x144 | 48x48 |

---

## ExpandedFolderView (`src/shell/ui/material/expanded_view.py`)

Full-size folder popup showing all app icons. Extends `QFrame`. Fixed size 580x680.

### Constructor

```python
ExpandedFolderView(folder_name: str, parent=None)
```

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `close_requested` | `pyqtSignal()` | Close button or outside click |
| `app_selected` | `pyqtSignal(str)` | App icon clicked |
| `close_current_app_requested` | `pyqtSignal()` | "BACK" button clicked |
| `minimize_requested` | `pyqtSignal()` | Minimize to floating icon |

### Key Methods

| Method | Description |
|--------|-------------|
| `add_app_icon(widget, row, col)` | Add widget to the 4-column grid |
| `fade_in(center_pos)` | Combined fade + scale-in animation |
| `fade_out()` | Combined fade + scale-out animation |
| `show_close_app_button()` | Show "BACK" button with fade animation |
| `hide_close_app_button()` | Hide "BACK" button |
| `on_app_clicked(app_name)` | Handle app selection, emit signals |

---

## FolderOverlay (`src/shell/ui/material/overlay.py`)

Translucent background overlay. Extends `QWidget`.

### Constructor

```python
FolderOverlay(parent=None)
```

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `mouse_pressed_outside` | `pyqtSignal()` | Any click on the overlay |

### Methods

| Method | Description |
|--------|-------------|
| `fade_in()` | Animate from 0 to 1 opacity |
| `fade_out()` | Animate from 1 to 0 opacity, then hide |

---

## FloatingFolderIcon (`src/shell/ui/material/floating_icon.py`)

Floating action button (FAB) shown when a folder is minimized. Extends `QPushButton`. Fixed size 80x80.

### Constructor

```python
FloatingFolderIcon(folder_name: str, parent=None)
```

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `clicked_signal` | `pyqtSignal()` | FAB clicked |

### Methods

| Method | Description |
|--------|-------------|
| `show_with_animation()` | Scale-in + fade-in via `AnimationManager` |
| `hide_with_animation()` | Fade-out via `AnimationManager` |

---

## AnimationManager (`src/shell/ui/material/animation.py`)

Centralized animation system. Extends `QObject`.

### Timing Constants (`MaterialDesignTiming`)

| Constant | Value (ms) |
|----------|-----------|
| `FAST` | 100 |
| `SHORT` | 150 |
| `MEDIUM` | 300 |
| `LONG` | 500 |
| `EXTRA_LONG` | 700 |

### Easing Presets (`MaterialDesignEasing`)

| Constant | QEasingCurve |
|----------|-------------|
| `STANDARD` | `OutCubic` |
| `EMPHASIZED` | `OutQuart` |
| `DECELERATED` | `OutCubic` |
| `ACCELERATED` | `InCubic` |
| `LINEAR` | `Linear` |

### Constructor

```python
AnimationManager(target_widget: QWidget, parent=None)
```

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `animation_finished` | `pyqtSignal(str)` | Single animation completed |
| `all_animations_finished` | `pyqtSignal()` | All active animations done |

### Animation Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `fade_in(start, end, duration, callback)` | `QPropertyAnimation` | Opacity 0→1 |
| `fade_out(start, end, duration, hide, callback)` | `QPropertyAnimation` | Opacity 1→0 |
| `scale_in_from_center(center, scale, duration, callback)` | `QPropertyAnimation` | Geometry animation |
| `scale_out_to_center(center, scale, duration, hide, callback)` | `QPropertyAnimation` | Geometry animation |
| `combined_fade_and_scale_in(center, scale, ...)` | `QParallelAnimationGroup` | Parallel fade + scale entrance |
| `combined_fade_and_scale_out(center, scale, ...)` | `QParallelAnimationGroup` | Parallel fade + scale exit |
| `create_floating_icon_show_animation(offset, duration)` | `QParallelAnimationGroup` | FAB appear |
| `create_floating_icon_hide_animation(duration, callback)` | `QPropertyAnimation` | FAB disappear |
| `create_button_press_animation(scale, duration)` | `QPropertyAnimation` | Scale down 95% |
| `create_button_release_animation(original_rect, duration)` | `QPropertyAnimation` | Restore size |

### Control Methods

| Method | Description |
|--------|-------------|
| `stop_animation(animation_id)` | Stop a specific animation by ID |
| `stop_all_animations()` | Stop all active animations |
| `is_animation_active(animation_id)` | Check if running |
| `has_active_animations()` | Any running? |
| `cleanup()` | Stop all and delete |

### Utility Functions

```python
create_material_entrance_animation(widget, center_pos, duration, callback)
create_material_exit_animation(widget, duration, callback)
create_fab_animation(widget, show=True, callback=None)
```

### AnimationPatterns (Static Methods)

```python
AnimationPatterns.folder_open_animation(widget, center_pos)
AnimationPatterns.folder_close_animation(widget)
AnimationPatterns.floating_icon_transition(widget, show)
```

---

## Manager Classes

### ExpandedViewManager (`src/shell/ui/material/managers/expanded_view_manager.py`)

Manages the lifecycle of `ExpandedFolderView`.

| Method | Description |
|--------|-------------|
| `show_expanded_view(folder_name, overlay_parent, on_close, on_app_selected, on_minimize, on_close_app)` | Create and wire up the view |
| `populate_apps(buttons)` | Copy `MenuIcon` objects into a 4-column grid |
| `fade_in(center_pos)` | Delegate to expanded view |
| `fade_out()` | Delegate to expanded view |
| `show_close_button()` | Show "BACK" button |
| `hide_close_button()` | Hide "BACK" button |

### FloatingIconManager (`src/shell/ui/material/managers/floating_icon_manager.py`)

Manages `FloatingFolderIcon` lifecycle.

| Method | Description |
|--------|-------------|
| `show_floating_icon(folder_name, on_click_callback)` | Create FAB at position (10, 10) on main window |
| `hide_floating_icon()` | Hide with animation, schedule cleanup after 300ms |

### OverlayManager (`src/shell/ui/material/managers/overlay_manager.py`)

Manages `FolderOverlay` instance.

| Method | Description |
|--------|-------------|
| `show_overlay()` | Resize to parent, set light style, fade in |
| `hide_overlay()` | Fade out |
| `set_style(style: str)` | Update overlay stylesheet |

---

## Header (`src/shell/ui/Header.py`)

Top toolbar bar. Extends `QFrame`.

### Constructor

```python
Header(screen_width: int, screen_height: int,
       toggle_menu_callback: Optional[Callable],
       dashboard_button_callback: Optional[Callable],
       languages: Optional[list] = None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `languages` | `list[tuple[str, str]]` or `None` | Language `(code, display_name)` tuples passed to `LanguageSelectorWidget`. When `None` (default), the language selector is hidden. |

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `user_account_clicked` | `pyqtSignal()` | User icon clicked |
| `fps_updated` | `pyqtSignal(float)` | FPS value updated |

### Key Widgets

| Attribute | Type | Description |
|-----------|------|-------------|
| `dashboardButton` | `QPushButton` | Dashboard icon button |
| `menu_button` | `QPushButton` | Hamburger menu button |
| `language_selector` | `LanguageSelectorWidget` | Language dropdown |
| `power_toggle_button` | `QPushButton` | Power on/off toggle |
| `userAccountButton` | `QPushButton` | User account (hidden by default) |
| `fps_label` | `QLabel` | FPS display |

### Methods

| Method | Description |
|--------|-------------|
| `toggle_power()` | Toggle power state, update icon and tooltip |
| `update_fps_label(fps: float)` | Update FPS display text |
| `handle_language_change(language_code)` | Log language change |

Height: responsive between `screen_height * 0.08` and `100px`.

---

## LanguageSelectorWidget (`src/shell/ui/LanguageSelectorWidget.py`)

Language dropdown. Extends `QComboBox`.

### Constructor

```python
LanguageSelectorWidget(languages: Optional[list[tuple[str, str]]] = None, parent=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `languages` | `list[tuple[str, str]]` or `None` | List of `(code, display_name)` tuples. Defaults to `[("en", "English"), ("bg", "Bulgarian")]` internally, but the widget is hidden when `Header` receives `None`. |

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `languageChanged` | `pyqtSignal(str)` | Emits the language code string (e.g. `"en"`) on selection change |

### Behavior

On selection change:
1. Updates `current_language` attribute (language code string).
2. Emits `languageChanged` signal with the code string.
3. Posts `QEvent.Type.LanguageChange` to all top-level widgets via `QApplication.postEvent()`.

---

## AppWidget (`src/shell/base_app_widget/AppWidget.py`)

Base class for application content. Extends `QWidget`. Implements `IAppWidget` protocol.

### Constructor

```python
AppWidget(app_name: str, parent=None)
```

### Signals

| Signal | Type | Description |
|--------|------|-------------|
| `app_closed` | `pyqtSignal()` | App wants to close |

### Methods

| Method | Description |
|--------|-------------|
| `close_app()` | Emit `app_closed` signal |
| `on_language_changed()` | Called on `LanguageChange` event. Override in subclasses for translation logic. Base implementation prints. |
| `clean_up()` | Override for resource cleanup (no-op by default) |

---

Previous: [Configuration](./03-configuration.md) | Next: [API Reference](./05-api-reference.md)
