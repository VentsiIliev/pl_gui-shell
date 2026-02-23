"""
Example: Custom Folder Configuration

Demonstrates programmatically adding custom folders to the shell.
"""
import sys
from PyQt6.QtWidgets import QApplication

from src.shell.AppShell import AppShell
from src.shell.app_descriptor import AppDescriptor
from src.shell.shell_config import ShellConfig, create_custom_folder
from src.shell.base_app_widget.AppWidget import AppWidget


def create_simple_factory():
    """Simple factory that returns placeholder widgets."""
    def factory(app_name: str):
        print(f"[Factory] Creating widget for '{app_name}'")
        return AppWidget(app_name=app_name)
    return factory


def setup_custom_folders():
    """
    Configure a custom folder structure with 5 folders.

    This demonstrates the public API for folder management.
    """
    print("=" * 60)
    print("CONFIGURING CUSTOM FOLDER STRUCTURE")
    print("=" * 60)

    # Start fresh - clear defaults
    ShellConfig.clear_folders()

    # Add custom folders using the public API with override_defaults=True
    custom_folders = [
        create_custom_folder(1, "PRODUCTION", "Production"),
        create_custom_folder(2, "QUALITY", "Quality Control"),
        create_custom_folder(3, "MAINTENANCE", "Maintenance"),
        create_custom_folder(4, "DIAGNOSTICS", "Diagnostics"),
        create_custom_folder(5, "ADMIN", "Administration"),
    ]

    for folder in custom_folders:
        ShellConfig.add_folder(folder, override_defaults=True)
        print(f"  ✓ Added: {folder.display_name} (ID: {folder.id})")

    print(f"\nTotal folders configured: {len(ShellConfig.get_folders())}")
    print("=" * 60)


def create_apps_for_custom_folders():
    """Create app descriptors for the custom folders."""
    return [
        # Production folder (ID=1)
        AppDescriptor("Production Monitor", "fa5s.industry", 1),
        AppDescriptor("Batch Control", "fa5s.tasks", 1),
        AppDescriptor("Process View", "fa5s.project-diagram", 1),

        # Quality folder (ID=2)
        AppDescriptor("QC Dashboard", "fa5s.check-circle", 2),
        AppDescriptor("Inspection Log", "fa5s.clipboard-check", 2),

        # Maintenance folder (ID=3)
        AppDescriptor("Equipment Status", "fa5s.wrench", 3),
        AppDescriptor("Maintenance Log", "fa5s.tools", 3),
        AppDescriptor("Spare Parts", "fa5s.boxes", 3),

        # Diagnostics folder (ID=4)
        AppDescriptor("System Health", "fa5s.heartbeat", 4),
        AppDescriptor("Error Logs", "fa5s.exclamation-triangle", 4),
        AppDescriptor("Performance", "fa5s.chart-line", 4),

        # Admin folder (ID=5)
        AppDescriptor("User Management", "fa5s.users-cog", 5),
        AppDescriptor("Settings", "fa5s.cog", 5),
        AppDescriptor("Reports", "fa5s.file-alt", 5),
    ]


def main():
    """Run the app shell with custom folder configuration."""
    app = QApplication(sys.argv)

    # Step 1: Configure custom folders using public API
    setup_custom_folders()

    # Step 2: Create app descriptors for custom folders
    app_descriptors = create_apps_for_custom_folders()

    # Step 3: Create widget factory
    widget_factory = create_simple_factory()

    # Step 4: Create shell - it will automatically use the custom folders
    shell = AppShell(
        app_descriptors=app_descriptors,
        widget_factory=widget_factory
    )

    shell.resize(1280, 1024)
    shell.show()

    print("\n" + "=" * 60)
    print("CUSTOM FOLDER SHELL RUNNING")
    print("=" * 60)
    print(f"✓ {len(ShellConfig.get_folders())} custom folders rendered")
    print(f"✓ {len(app_descriptors)} apps distributed across folders")
    print("\nClick any app icon to see placeholder widget")
    print("ESC to close app and return to folders")
    print("=" * 60)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

