import sys
from typing import List

from PyQt6.QtWidgets import QApplication, QWidget

from src.shell.AppShell import AppShell
from src.shell.app_descriptor import AppDescriptor
from src.shell.base_app_widget.AppWidget import AppWidget

def create_simple_factory():
    """Simple factory that always returns placeholder AppWidgets - no plugins!"""
    def factory(app_name: str) -> QWidget:
        print(f"[SimpleFactory] Creating placeholder widget for '{app_name}'")
        return AppWidget(app_name=app_name)

    return factory

def get_example_app_descriptors() -> List[AppDescriptor]:
     # Step 1: Define apps with pure data - no plugin system!
    app_descriptors = [
        # Work folder (folder_id=1)
        AppDescriptor(
            name="Dashboard",
            icon_str="fa5s.tachometer-alt",
            folder_id=1
        ),
        AppDescriptor(
            name="Management",
            icon_str="fa5s.folder-open",
            folder_id=1
        ),
        AppDescriptor(
            name="Settings",
            icon_str="fa5s.chart-bar",
            folder_id=1
        ),

        # Service folder (folder_id=2)
        AppDescriptor(
            name="GALLERY",
            icon_str="fa5s.cog",
            folder_id=2
        ),
        AppDescriptor(
            name="CALIBRATION",
            icon_str="fa5s.stethoscope",
            folder_id=2
        ),

        # Admin folder (folder_id=3)
        AppDescriptor(
            name="ANALYTICS",
            icon_str="fa5s.users",
            folder_id=3
        ),
    ]

    return app_descriptors

def main():
    app = QApplication(sys.argv)


    # Step 1: Define apps with pure data - no plugin system!
    app_descriptors = get_example_app_descriptors()

    # Step 2: Create factory that creates AppWidgets from descriptors - no plugin system!
    widget_factory = create_simple_factory()

    # Step 3: Create MainWindow with pure data - NO plugin knowledge!
    window = AppShell(
        app_descriptors=app_descriptors,
        widget_factory=widget_factory,
        languages=[("en", "English"), ("de", "German"), ("fr", "French")] # If no language is provided, it will not show the language switcher in the UI

    )

    window.resize(1280, 1024)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

