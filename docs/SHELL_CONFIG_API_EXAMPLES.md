# Shell Configuration API Examples

This document demonstrates how to use the public API for managing folder definitions in the App Shell.

## Basic Usage

### Getting Current Folders

```python
from src.shell.shell_config import ShellConfig

# Get all folders
folders = ShellConfig.get_folders()
for folder in folders:
    print(f"ID {folder.id}: {folder.display_name}")

# Get specific folder
work_folder = ShellConfig.get_folder_by_id(1)
if work_folder:
    print(f"Found: {work_folder.name}")

# Check if folder exists
if ShellConfig.folder_exists(4):
    print("Folder 4 is configured")

# Get all folder IDs
ids = ShellConfig.get_all_folder_ids()
print(f"Configured folder IDs: {ids}")
```

## Adding Custom Folders

### Method 1: Add to Default Folders

```python
from src.shell.shell_config import ShellConfig, FolderDefinition

# Create and add a maintenance folder (defaults will be initialized first)
maintenance = FolderDefinition(
    id=4,
    name="MAINTENANCE",
    translation_key="folder.maintenance",
    display_name="MAINTENANCE"
)

# This adds to the 3 default folders (WORK, SERVICE, ADMINISTRATION)
ShellConfig.add_folder(maintenance)  # override_defaults=False (default)

# Result: 4 folders total (3 defaults + 1 custom)
```

### Method 2: Override Defaults (Custom-Only Configuration)

```python
from src.shell.shell_config import ShellConfig, create_custom_folder

# Clear defaults first
ShellConfig.clear_folders()

# Add custom folders WITHOUT initializing defaults
custom_folders = [
    create_custom_folder(1, "PRODUCTION", "Production"),
    create_custom_folder(2, "QUALITY", "Quality Control"),
    create_custom_folder(3, "MAINTENANCE", "Maintenance"),
]

for folder in custom_folders:
    ShellConfig.add_folder(folder, override_defaults=True)

# Result: Only 3 custom folders (no defaults)
```

### Method 3: Using Helper Function

```python
from src.shell.shell_config import ShellConfig, create_custom_folder

# Simpler way to create and add custom folders to defaults
maintenance = create_custom_folder(
    folder_id=4,
    name="MAINTENANCE",
    display_name="Maintenance"  # Optional, defaults to name
)

ShellConfig.add_folder(maintenance)  # Adds to defaults
```

## Updating Folders

```python
from src.shell.shell_config import ShellConfig

# Update display name
ShellConfig.update_folder(1, display_name="WORK AREA")

# Update multiple fields
ShellConfig.update_folder(
    folder_id=2,
    display_name="Service & Support",
    translation_key="folder.service_support"
)

# Check if update succeeded
if ShellConfig.update_folder(99, display_name="Invalid"):
    print("Updated successfully")
else:
    print("Folder not found")
```

## Removing Folders

```python
from src.shell.shell_config import ShellConfig

# Remove a folder
if ShellConfig.remove_folder(4):
    print("Maintenance folder removed")
else:
    print("Folder not found")
```

## Resetting Configuration

```python
from src.shell.shell_config import ShellConfig

# Reset to default 3 folders (WORK, SERVICE, ADMINISTRATION)
ShellConfig.reset_to_defaults()

# Clear all folders (use with caution!)
ShellConfig.clear_folders()

# Then add custom configuration
ShellConfig.add_folder(create_custom_folder(1, "CUSTOM"))
```

## Complete Example: Custom Configuration

```python
from src.shell.shell_config import ShellConfig, create_custom_folder

def setup_custom_folders():
    """Setup a completely custom folder structure."""
    
    # Clear default folders
    ShellConfig.clear_folders()
    
    # Add custom folders for a specific application
    folders = [
        create_custom_folder(1, "PRODUCTION", "Production"),
        create_custom_folder(2, "QUALITY_CONTROL", "Quality Control"),
        create_custom_folder(3, "MAINTENANCE", "Maintenance"),
        create_custom_folder(4, "ADMINISTRATION", "Admin"),
    ]
    
    for folder in folders:
        ShellConfig.add_folder(folder)
    
    print(f"Configured {len(ShellConfig.get_folders())} custom folders")

# Use in your application startup
if __name__ == "__main__":
    setup_custom_folders()
```

## Integration with AppShell

The folder configuration is automatically picked up by AppShell:

```python
from src.shell.shell_config import ShellConfig, create_custom_folder
from src.shell.AppShell import AppShell
from src.core.app_registry import build_app_registry

# Configure custom folders BEFORE creating AppShell
maintenance_folder = create_custom_folder(4, "MAINTENANCE", "Maintenance")
ShellConfig.add_folder(maintenance_folder)

# Create descriptors with apps in the new folder
app_descriptors = [
    AppDescriptor("Diagnostics", "fa5s.stethoscope", folder_id=4),
    AppDescriptor("Logs Viewer", "fa5s.file-alt", folder_id=4),
]

# AppShell will automatically render the MAINTENANCE folder
shell = AppShell(app_descriptors, widget_factory)
```

## Runtime Folder Management

```python
from src.shell.shell_config import ShellConfig, create_custom_folder

class FolderManager:
    """Example manager for runtime folder configuration."""
    
    @staticmethod
    def add_maintenance_folder_if_needed(has_maintenance_permission: bool):
        """Conditionally add maintenance folder based on user permissions."""
        if has_maintenance_permission and not ShellConfig.folder_exists(4):
            maintenance = create_custom_folder(4, "MAINTENANCE")
            ShellConfig.add_folder(maintenance)
            return True
        return False
    
    @staticmethod
    def configure_for_user_role(role: str):
        """Configure folders based on user role."""
        ShellConfig.reset_to_defaults()
        
        if role == "admin":
            # Admins see all folders
            pass
        elif role == "operator":
            # Operators only see work folder
            ShellConfig.remove_folder(2)  # Remove SERVICE
            ShellConfig.remove_folder(3)  # Remove ADMINISTRATION
        elif role == "technician":
            # Technicians see work + service
            ShellConfig.remove_folder(3)  # Remove ADMINISTRATION

# Usage
manager = FolderManager()
manager.configure_for_user_role("operator")
```

## Error Handling

```python
from src.shell.shell_config import ShellConfig, create_custom_folder

# Handle duplicate IDs
try:
    folder = create_custom_folder(1, "DUPLICATE")
    ShellConfig.add_folder(folder)
except ValueError as e:
    print(f"Error: {e}")
    # ID 1 already exists, use different ID
    folder = create_custom_folder(10, "DUPLICATE")
    ShellConfig.add_folder(folder)

# Safe removal
removed = ShellConfig.remove_folder(999)
if not removed:
    print("Folder 999 doesn't exist, nothing to remove")

# Safe update
updated = ShellConfig.update_folder(999, display_name="New Name")
if not updated:
    print("Folder 999 doesn't exist, cannot update")
```

## Best Practices

1. **Configure before creating AppShell**: Modify folder configuration before instantiating the shell
2. **Use unique IDs**: Folder IDs should be unique across your application
3. **Use ID constants**: Define constants for folder IDs instead of magic numbers
4. **Validate permissions**: Check user permissions before adding privileged folders
5. **Document folder purpose**: Use clear, descriptive names for custom folders

```python
# Good: Use constants
from src.shell.shell_config import FOLDER_WORK, FOLDER_SERVICE

app = AppDescriptor("My App", "fa5s.home", folder_id=FOLDER_WORK)

# Better: Define your own constants
FOLDER_MAINTENANCE = 4
FOLDER_DIAGNOSTICS = 5

app = AppDescriptor("Diagnostics", "fa5s.chart-line", folder_id=FOLDER_DIAGNOSTICS)
```

## API Reference Quick Summary

| Method | Purpose |
|--------|---------|
| `ShellConfig.add_folder(folder)` | Add new folder definition |
| `ShellConfig.remove_folder(folder_id)` | Remove folder by ID |
| `ShellConfig.update_folder(folder_id, **updates)` | Update folder properties |
| `ShellConfig.get_folders()` | Get all folders |
| `ShellConfig.get_folder_by_id(folder_id)` | Get specific folder |
| `ShellConfig.folder_exists(folder_id)` | Check if folder exists |
| `ShellConfig.get_all_folder_ids()` | Get list of all folder IDs |
| `ShellConfig.reset_to_defaults()` | Reset to default 3 folders |
| `ShellConfig.clear_folders()` | Remove all folders |
| `create_custom_folder(id, name, ...)` | Helper to create FolderDefinition |

