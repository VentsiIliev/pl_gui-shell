# Getting Started

## Prerequisites

- **Python 3.10+**
- **PyQt6** — Qt 6 bindings for Python
- **qtawesome** — FontAwesome icons for Qt

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-org>/pl_gui-shell.git
cd pl_gui-shell

# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
pl_gui-shell/
├── run_mainwindow.py              # Default demo (3 folders, 6 apps)
├── run_custom_folders.py          # Custom folders demo (5 folders, 15 apps)
├── src/
│   └── shell/
│       ├── app_descriptor.py      # AppDescriptor dataclass
│       ├── app_registry.py        # Plugin integration helper
│       ├── base_app_widget/
│       │   └── AppWidget.py       # Base application widget
│       ├── AppShell.py            # Main window (QWidget)
│       ├── FolderLauncher.py      # Folder grid page + FolderConfig
│       ├── folder_controller.py   # Business logic per folder
│       ├── interfaces.py          # 10 Protocol interfaces + UIFactory
│       ├── shell_config.py        # ShellConfig API + FolderDefinition
│       └── ui/
│           ├── Header.py              # Top toolbar with power, language, FPS
│           ├── LanguageSelectorWidget.py  # Language dropdown + i18n events
│           ├── icon_loader.py     # Unified icon loading with cache
│           ├── styles.py          # Design tokens (colors, shadows, stylesheets)
│           └── material/
│               ├── __init__.py    # Exports MaterialUIFactory
│               ├── factory.py     # MaterialUIFactory implementation
│               ├── animation.py   # AnimationManager + Material timing
│               ├── expanded_view.py   # ExpandedFolderView
│               ├── floating_icon.py   # FloatingFolderIcon (FAB)
│               ├── folder_widget.py   # FolderWidget + LayoutManager
│               ├── menu_icon.py       # MenuIcon (app icon button)
│               ├── overlay.py         # FolderOverlay
│               └── managers/
│                   ├── expanded_view_manager.py
│                   ├── floating_icon_manager.py
│                   └── overlay_manager.py
└── tests/
    ├── conftest.py
    └── ...
```

## Running the Default Demo

```bash
python run_mainwindow.py
```

This launches the shell with **3 default folders** (WORK, SERVICE, ADMINISTRATION) and **6 example apps** distributed across them:

| Folder          | Apps                              |
|-----------------|-----------------------------------|
| WORK (1)        | Dashboard, Management, Settings   |
| SERVICE (2)     | GALLERY, CALIBRATION              |
| ADMINISTRATION (3) | ANALYTICS                      |

Click a folder to expand it, then click an app icon to launch it. Press **ESC** to close the running app and return to the folder view.

## Running the Custom Folders Demo

```bash
python run_custom_folders.py
```

This demo shows how to configure **5 custom folders** with **15 apps** using the `ShellConfig` API. See [03-configuration.md](./03-configuration.md) for details.

## Minimal Hello-World Example

Create a file `hello_shell.py` at the project root:

```python
import sys
from PyQt6.QtWidgets import QApplication
from src.shell.AppShell import AppShell
from src.shell.app_descriptor import AppDescriptor
from src.shell.base_app_widget.AppWidget import AppWidget


def main():
    app = QApplication(sys.argv)

    # 1. Define apps as data
    descriptors = [
        AppDescriptor(name="Hello App", icon_str="fa5s.star", folder_id=1),
        AppDescriptor(name="World App", icon_str="fa5s.globe", folder_id=1),
    ]

    # 2. Create a widget factory
    def factory(app_name: str):
        return AppWidget(app_name=app_name)

    # 3. Launch the shell
    shell = AppShell(app_descriptors=descriptors, widget_factory=factory)
    shell.resize(1280, 1024)
    shell.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

Run it:

```bash
python hello_shell.py
```

You will see a single WORK folder containing two app icons. Click the folder to expand, click an icon to launch the placeholder app.

---

Next: [Architecture](./02-architecture.md)
