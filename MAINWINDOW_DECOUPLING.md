# MainWindow Decoupling Analysis

## The Actual Coupling in MainWindow Today

### Current Problems

```python
# MainWindow.__init__
self.plugin_widget_factory = PluginWidgetFactory(controller, self)   # ← MainWindow creates the plugin system

# MainWindow.create_folders_page()
for plugin_name in self.plugin_widget_factory.plugin_manager.get_loaded_plugin_names():  # ← drills into plugin internals
    json_metadata = getattr(plugin, '_json_metadata', {})

# MainWindow.close_all_apps()
for name in self.plugin_widget_factory._widget_cache.items():   # ← accesses private cache

# MainWindow imports
from core.application.ApplicationContext import get_application_required_plugins  # ← knows about app context
from modules.shared.GlueWorkpieceField import GlueWorkpieceField                 # ← glue-specific in GUI shell!
```

**MainWindow currently does three jobs:**
1. Qt shell
2. Plugin orchestrator
3. App-specific wiring

**That's the overlap causing tight coupling.**

---

## The Clean Separation

MainWindow should only receive **two things** from outside:

1. `list[AppDescriptor]` — what icons to show in which folder
2. `Callable[[str], QWidget]` — how to create a widget given an app name

It never needs to know **HOW** those come from plugins, or **WHICH** application is running.

### Architecture Flow

```
┌─────────────────────────────────────────────────────────┐
│  main.py                                                │
│    1. creates RobotApplication                          │
│    2. PluginManager loads its plugins                   │
│    3. builds AppDescriptor list from loaded plugins     │
│    4. builds factory fn: app_name → plugin.create_widget│
│    5. passes both into PlGui / MainWindow               │
└──────────────┬──────────────────────────────────────────┘
               │  injects: descriptors + factory
┌──────────────▼──────────────────────────────────────────┐
│  MainWindow (PL_GUI)                                    │
│    - renders folders from AppDescriptor list            │
│    - calls factory(app_name) when user taps an icon     │
│    - puts the returned QWidget into QStackedWidget      │
│    - ZERO import of Plugin, PluginManager, AppContext   │
└─────────────────────────────────────────────────────────┘
```

---

## The New Interface

### AppDescriptor Dataclass

```python
# A plain dataclass — no plugin imports
@dataclass
class AppDescriptor:
    name: str        # "Dashboard", "Settings"
    icon: QIcon      # already resolved
    folder_id: int   # 1 = Work, 2 = Service, 3 = Admin
```

### MainWindow Constructor

```python
# MainWindow receives these — knows nothing else
class MainWindow(TranslatableWidget):
    def __init__(
        self,
        controller,
        app_descriptors: list[AppDescriptor],
        widget_factory: Callable[[str], QWidget],
    ):
        self._app_descriptors = app_descriptors
        self._widget_factory = widget_factory
        ...

    def create_app(self, app_name: str) -> QWidget:
        return self._widget_factory(app_name)   # one line, no plugin knowledge

    def create_folders_page(self):
        for desc in self._app_descriptors:      # no plugin_manager loop
            ...
```

---

## Where the Wiring Actually Lives

### New AppBinder / PlGui Integration

```python
# PlGui.start() — or a new AppBinder class
def _build_app_registry(plugin_manager, icon_map) -> tuple[list[AppDescriptor], Callable]:
    """Build app descriptors and factory from loaded plugins."""
    descriptors = []
    
    for name in plugin_manager.get_loaded_plugin_names():
        plugin = plugin_manager.get_plugin(name)
        meta = plugin._json_metadata
        descriptors.append(AppDescriptor(
            name=name,
            icon=icon_map.get(meta.get('icon_name')),
            folder_id=meta.get('folder_id', 1),
        ))

    def factory(app_name: str) -> QWidget:
        """Create widget for given app name."""
        plugin = plugin_manager.get_plugin(app_name)
        if plugin:
            return plugin.create_widget()
        return AppWidget(app_name=f"Unknown: {app_name}")

    return descriptors, factory
```

**PlGui.start()** calls this, then passes both into MainWindow.  
The plugin system **never leaks** into the shell.

---

## What This Buys You

| Concern | Lives in | MainWindow sees |
|---------|----------|-----------------|
| Which plugins exist | PluginManager | nothing |
| Which app type is running | ApplicationContext | nothing |
| Icon paths | PlGui / AppBinder | resolved QIcon |
| Widget construction | IPlugin.create_widget() | opaque Callable |
| Folder structure | AppDescriptor.folder_id | plain int |

**PL_GUI becomes a completely standalone Qt shell.**

You could run it with:
- Hardcoded list of `AppDescriptor`
- Mock callables in tests
- **No plugins, no robot application, no broker**

---

## The One Remaining Issue

### Signal Wiring in MainWindow

```python
# MainWindow._connect_widget_signals() still does app-specific wiring:
if hasattr(app_widget, 'start_requested'):
    app_widget.start_requested.connect(...)
    app_widget.clean_requested.connect(...)    # glue-specific
    app_widget.reset_errors_requested.connect(...)
```

### The Right Fix

The factory callable passed to MainWindow returns an **already-wired widget**.

The plugin's `create_widget()` connects its own signals to the controller internally.

MainWindow only needs to connect the **generic `app_closed`** signal.

---

## Summary of Changes Needed

| File | Change |
|------|--------|
| `MainWindow.__init__` | Accept `app_descriptors` + `widget_factory` instead of creating `PluginWidgetFactory` |
| `MainWindow.create_folders_page` | Iterate `self._app_descriptors`, no plugin loop |
| `MainWindow.create_app` | Call `self._widget_factory(name)`, 1 line |
| `MainWindow.close_all_apps` | Don't touch `plugin_widget_factory._widget_cache` |
| `PlGui.start()` | Build descriptors + factory, inject into MainWindow |
| Each `plugin.create_widget()` | Connect its own signals to controller_service internally |

---

## Benefits After Refactoring

### Before (Tightly Coupled)

```python
MainWindow
  ├─ imports PluginWidgetFactory ❌
  ├─ imports ApplicationContext ❌
  ├─ imports GlueWorkpieceField ❌
  ├─ creates plugin_widget_factory ❌
  ├─ accesses plugin_manager internals ❌
  └─ knows about specific signals (clean_requested) ❌
```

### After (Properly Decoupled)

```python
MainWindow
  ├─ receives list[AppDescriptor] ✅
  ├─ receives Callable[[str], QWidget] ✅
  ├─ renders folders from descriptors ✅
  ├─ calls factory to create widgets ✅
  └─ NO knowledge of plugins/apps/signals ✅
```

---

## Testing Benefits

### Unit Testing MainWindow (After Refactoring)

```python
def test_main_window_renders_folders():
    # No need for real plugins!
    descriptors = [
        AppDescriptor("Test App", QIcon(), folder_id=1),
        AppDescriptor("Another App", QIcon(), folder_id=2),
    ]
    
    def mock_factory(name: str) -> QWidget:
        return QLabel(f"Mock widget: {name}")
    
    window = MainWindow(
        controller=None,
        app_descriptors=descriptors,
        widget_factory=mock_factory
    )
    
    # Test folder creation, icon placement, etc.
    # No PluginManager, no ApplicationContext, no real plugins!
```

---

## Implementation Priority

### Phase 1: Core Decoupling
1. ✅ Create `AppDescriptor` dataclass
2. ✅ Create `_build_app_registry()` function in PlGui
3. ✅ Refactor `MainWindow.__init__` to accept descriptors + factory
4. ✅ Update `MainWindow.create_app()` to use factory

### Phase 2: Remove Dependencies
5. ✅ Remove `PluginWidgetFactory` from MainWindow imports
6. ✅ Remove `ApplicationContext` import from MainWindow
7. ✅ Remove `GlueWorkpieceField` import from MainWindow
8. ✅ Update `create_folders_page()` to use descriptors

### Phase 3: Signal Cleanup
9. ✅ Move signal wiring into each plugin's `create_widget()`
10. ✅ Simplify `MainWindow._connect_widget_signals()`
11. ✅ Only connect generic signals in MainWindow

---

## Related Documents

- See [`ARCHITECTURE_ANALYSIS.md`](./ARCHITECTURE_ANALYSIS.md) for application/plugin/widget layer analysis
- This document focuses specifically on the **MainWindow decoupling** strategy

---

## Date

Generated: February 20, 2026

