# PL_GUI Shell

A decoupled, modular Qt-based application shell for launching and managing applications through a folder-based interface.

## 🏗️ Architecture

This project implements a **clean separation** between the GUI shell and the application/plugin system following the principles outlined in [MAINWINDOW_DECOUPLING.md](./MAINWINDOW_DECOUPLING.md).

### Core Layers

```
┌─────────────────────────────────────────────────────────┐
│  main.py / Runner                                       │
│    1. Creates plugin manager                            │
│    2. Builds AppDescriptor list from plugins            │
│    3. Creates factory: app_name → widget                │
│    4. Injects both into AppShell                        │
└──────────────┬──────────────────────────────────────────┘
               │  injects: descriptors + factory
┌──────────────▼──────────────────────────────────────────┐
│  AppShell (Pure Qt GUI)                                 │
│    - Renders folders from AppDescriptor list            │
│    - Calls factory(app_name) when user clicks icon      │
│    - Puts returned QWidget into QStackedWidget          │
│    - ZERO knowledge of plugins or business logic        │
└─────────────────────────────────────────────────────────┘
```

- **Shell Layer** (`src/shell/`) - Pure Qt launcher with folder-based UI
- **Base App** (`src/shell/base_app_widget/`) - Base application widget
- **Core** (`src/shell/app_descriptor.py`, `src/shell/app_registry.py`) - Integration abstractions
- **Components** (`src/components/`) - Shared UI components
- **Factory Layer** (`src/factory/`) - Mock plugin system

## 📁 Project Structure

```
PL_GUI/
├── src/
│   ├── shell/                    # App Shell - folder launcher
│   │   ├── AppShell.py          # Main window (formerly MainWindow)
│   │   ├── FolderLauncher.py    # Folder grid manager
│   │   ├── shell_config.py      # Centralized folder configuration
│   │   └── components/
│   │       └── folder/          # Folder UI components
│   │           ├── Folder.py
│   │           ├── MenuIcon.py
│   │           ├── FloatingFolderIcon.py
│   │           ├── ExpandedFolderView.py
│   │           └── managers/
│   │
│   ├── apps/                     # Individual applications
│   │   ├── base/
│   │   │   └── AppWidget.py     # Base class for all apps
│   │   └── dashboard/           # Example app (if exists)
│   │
│   ├── core/                     # Core abstractions
│   │   ├── app_descriptor.py    # AppDescriptor dataclass
│   │   └── app_registry.py      # Integration seam
│   │
│   ├── components/               # Shared UI components
│   │   ├── Header.py
│   │   └── LanguageSelectorWidget.py
│   │
│   ├── factory/                  # Mock plugin system
│   │   ├── WidgetFactory.py
│   │   ├── MockPluginManager.py
│   │   └── MockPluginWidgetFactory.py
│   │
│   └── utils_widgets/            # Utility widgets
│       └── MaterialButton.py
│
├── run_mainwindow.py             # Main runner with plugin system
├── run_barebone.py               # Barebone runner (no plugins)
├── tests/                        # Test suite
├── MAINWINDOW_DECOUPLING.md      # Architecture documentation
└── README.md                     # This file
```

## 🌟 Key Features

### Complete Decoupling
- **AppShell** has ZERO imports of Plugin, PluginManager, or AppContext
- Shell only receives `List[AppDescriptor]` and `Callable[[str], QWidget]`
- Clean dependency injection pattern

### AppDescriptor Pattern
```python
@dataclass
class AppDescriptor:
    name: str        # "Dashboard", "Settings"
    icon_str: str    # "fa5s.tachometer-alt" (QtAwesome string)
    folder_id: int   # 1=WORK, 2=SERVICE, 3=ADMINISTRATION
```

### Integration Seam
The `app_registry.py` module is the **only place** that knows about plugins:
```python
def build_app_registry(plugin_manager, widget_factory):
    # Converts plugin system → (descriptors, factory)
    # THIS IS THE SEAM between shell and plugins
```

### Centralized Configuration
Folder structure defined in `shell_config.py`:
```python
class ShellConfig:
    FOLDERS = [
        FolderDefinition(id=1, name="WORK", ...),
        FolderDefinition(id=2, name="SERVICE", ...),
        FolderDefinition(id=3, name="ADMINISTRATION", ...),
    ]
```

### Testable Architecture
```python
# Run with mock data - no plugins needed!
descriptors = [AppDescriptor("Test", "fa5s.home", 1)]
factory = lambda name: QLabel(f"Mock: {name}")
shell = AppShell(descriptors, factory)
```

## 🚀 Running the Application

### With Plugin System
```bash
python run_mainwindow.py
```

### Barebone Mode (No Plugins)
```bash
python run_barebone.py
```

The barebone runner demonstrates the shell working with hardcoded `AppDescriptor` data and a simple factory that returns placeholder widgets.

## 📦 Requirements

- Python 3.10+
- PyQt6
- qtawesome (for Font Awesome icons)

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/VentsiIliev/pl_gui-shell.git
cd pl_gui-shell

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install PyQt6 qtawesome
```

## 🎯 Development Principles

### Layer Separation

1. **Shell Layer** - Only knows about `AppDescriptor` and widget factory callable
2. **Integration Layer** - `app_registry.py` converts plugin system to shell interface  
3. **Apps Layer** - Independent application widgets
4. **Plugin Layer** - Plugin management and loading

### What Lives Where

| Concern | Lives in | AppShell sees |
|---------|----------|---------------|
| Which plugins exist | PluginManager | nothing |
| Icon paths | app_registry.py | resolved icon strings |
| Widget construction | Plugin.create_widget() | opaque Callable |
| Folder structure | shell_config.py | FolderDefinition |

### Signal Wiring

- **Generic signals** (like `app_closed`) connected by AppShell
- **App-specific signals** connected inside the app's `create_widget()` method
- AppShell never knows about app-specific signals

## 🧪 Testing

The decoupled architecture enables easy testing:

```python
# Test AppShell without any plugins
def test_app_shell():
    descriptors = [
        AppDescriptor("App1", "fa5s.home", 1),
        AppDescriptor("App2", "fa5s.cog", 2),
    ]
    factory = lambda name: QLabel(f"Mock: {name}")
    
    shell = AppShell(descriptors, factory)
    # Test folder rendering, icon clicks, etc.
```

## 📚 Documentation

- **[MAINWINDOW_DECOUPLING.md](./MAINWINDOW_DECOUPLING.md)** - Detailed architecture analysis and refactoring strategy
- **[ARCHITECTURE_CONCEPTS.md](./ARCHITECTURE_CONCEPTS.md)** - Conceptual framework and naming conventions (if exists)

## 🎨 UI Features

- **Material Design** folder widgets with animations
- **QtAwesome** font icons for apps
- **Responsive layout** with 3-column grid
- **Folder expansion** with overlay and floating icons
- **Language selector** with Qt LanguageChange events
- **Header** with machine indicators

## 🔄 Adding New Apps

### Option 1: Via Plugin System
1. Create plugin with metadata (name, icon_str, folder_id)
2. Implement `create_widget()` method
3. Registry automatically picks it up

### Option 2: Via Barebone Runner
1. Add `AppDescriptor` to the list
2. Update factory to create widget for that name
3. Add to `WidgetType` enum (temporary requirement)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the layer separation principles
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

[Specify your license here]

## 👥 Authors

- Ventsi Iliev - [@VentsiIliev](https://github.com/VentsiIliev)

## 🙏 Acknowledgments

- Architecture inspired by clean architecture and dependency inversion principles
- UI design follows Material Design guidelines
- Built with PyQt6 and QtAwesome

---

**Note:** This is a refactored architecture demonstrating complete decoupling between GUI shell and application/plugin systems. The shell is a standalone Qt component that can work with any app system through dependency injection.

