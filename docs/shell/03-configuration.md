# Configuration

All configuration lives in `src/shell/shell_config.py`.

## FolderDefinition

```python
@dataclass
class FolderDefinition:
    id: int               # Unique folder identifier
    name: str             # Internal name (uppercase recommended)
    translation_key: str  # i18n key, e.g. "folder.work"
    display_name: str     # Default English display name
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_translate_fn()` | `Callable[[str], str]` | Returns a translation function (currently returns `display_name`) |

## ShellConfig

`ShellConfig` is a classmethod-based singleton. All methods are `@classmethod` — no instantiation required.

### Default Folders

On first access the config auto-initializes with three folders:

| ID | Name             | Translation Key          | Display Name      |
|----|------------------|--------------------------|--------------------|
| 1  | WORK             | `folder.work`            | WORK               |
| 2  | SERVICE          | `folder.service`         | SERVICE            |
| 3  | ADMINISTRATION   | `folder.administration`  | ADMINISTRATION     |

### Folder Management

#### `add_folder(folder, override_defaults=False)`

Add a new folder definition.

```python
from src.shell.shell_config import ShellConfig, FolderDefinition

# Add to defaults (auto-initializes if needed)
new_folder = FolderDefinition(id=4, name="MAINTENANCE",
                              translation_key="folder.maintenance",
                              display_name="Maintenance")
ShellConfig.add_folder(new_folder)

# Override defaults — for custom-only configurations
ShellConfig.clear_folders()
ShellConfig.add_folder(custom_folder, override_defaults=True)
```

Raises `ValueError` if the folder ID already exists.

#### `remove_folder(folder_id) -> bool`

Remove a folder by ID. Returns `True` if removed, `False` if not found.

```python
ShellConfig.remove_folder(4)  # True
```

#### `update_folder(folder_id, **updates) -> bool`

Update fields on an existing folder. Returns `True` if found and updated.

```python
ShellConfig.update_folder(1, display_name="WORK AREA", name="WORK_AREA")
```

#### `clear_folders()`

Remove all folder definitions. Prevents auto-initialization of defaults.

```python
ShellConfig.clear_folders()
```

#### `reset_to_defaults()`

Restore the three default folders.

```python
ShellConfig.reset_to_defaults()
```

### Folder Queries

#### `get_folders() -> list[FolderDefinition]`

Returns a copy of all folder definitions.

```python
for folder in ShellConfig.get_folders():
    print(f"{folder.id}: {folder.display_name}")
```

#### `get_folder_by_id(folder_id) -> Optional[FolderDefinition]`

Look up a single folder by ID.

```python
folder = ShellConfig.get_folder_by_id(1)
if folder:
    print(folder.name)  # "WORK"
```

#### `get_all_folder_ids() -> list[int]`

Returns all folder IDs as a list.

```python
ids = ShellConfig.get_all_folder_ids()  # [1, 2, 3]
```

#### `folder_exists(folder_id) -> bool`

Check whether a folder ID is defined.

```python
ShellConfig.folder_exists(4)  # False
```

#### `get_folders_with_apps(filtered_apps) -> list[FolderDefinition]`

Returns only folders that have at least one app. `filtered_apps` is a `dict[int, list]` mapping folder IDs to app lists.

```python
app_map = {1: [["Dashboard", "fa5s.tachometer-alt"]], 2: []}
folders = ShellConfig.get_folders_with_apps(app_map)
# Returns only folder 1 (folder 2 has an empty list)
```

## Helper Function

### `create_custom_folder(folder_id, name, display_name=None, translation_key=None)`

Convenience function for creating `FolderDefinition` objects with sensible defaults.

```python
from src.shell.shell_config import create_custom_folder, ShellConfig

folder = create_custom_folder(4, "MAINTENANCE", "Maintenance")
# FolderDefinition(id=4, name="MAINTENANCE",
#                  translation_key="folder.maintenance",
#                  display_name="Maintenance")

ShellConfig.add_folder(folder)
```

- `display_name` defaults to `name`
- `translation_key` defaults to `folder.{name.lower()}`

## Constants

```python
from src.shell.shell_config import FOLDER_WORK, FOLDER_SERVICE, FOLDER_ADMINISTRATION

FOLDER_WORK = 1
FOLDER_SERVICE = 2
FOLDER_ADMINISTRATION = 3
```

Use these when assigning `folder_id` on `AppDescriptor` for clarity.

## AppDescriptor

Defined in `src/shell/app_descriptor.py`:

```python
@dataclass
class AppDescriptor:
    name: str       # Display name shown under the icon
    icon_str: str   # QtAwesome icon string, e.g. "fa5s.cog"
    folder_id: int  # Must match a FolderDefinition.id
```

The `folder_id` maps each app to a folder. Apps whose `folder_id` has no matching `FolderDefinition` are silently excluded.

## Recipes

### Add a Folder to Defaults

```python
from src.shell.shell_config import ShellConfig, create_custom_folder

# Defaults (WORK, SERVICE, ADMINISTRATION) are auto-initialized
ShellConfig.add_folder(create_custom_folder(4, "DIAGNOSTICS", "Diagnostics"))
# Now 4 folders: 1, 2, 3, 4
```

### Fully Custom Folder Set

```python
from src.shell.shell_config import ShellConfig, create_custom_folder

ShellConfig.clear_folders()
for folder_id, name, display in [
    (1, "PRODUCTION", "Production"),
    (2, "QUALITY", "Quality Control"),
    (3, "MAINTENANCE", "Maintenance"),
]:
    ShellConfig.add_folder(
        create_custom_folder(folder_id, name, display),
        override_defaults=True
    )
```

### Modify an Existing Folder

```python
ShellConfig.update_folder(2, display_name="SERVICE & SUPPORT")
```

## Internationalization (i18n)

### How It Works

1. `LanguageSelectorWidget` (in the header) shows a dropdown built from a configurable list of `(code, display_name)` tuples.
2. When the user selects a new language, the widget posts `QEvent.Type.LanguageChange` to **all top-level widgets** via `QApplication.postEvent()`.
3. `AppShell.changeEvent()` detects `LanguageChange` and calls `retranslate()`.
4. `retranslate()` iterates folder widgets and calls `update_title_label()` on each.
5. Each `FolderWidget` calls its `translate_fn(folder_name)` to get the localized title.

### Configuring Languages

Pass a `languages` list to `AppShell`. Each entry is a `(code, display_name)` tuple:

```python
shell = AppShell(
    app_descriptors=descriptors,
    widget_factory=factory,
    languages=[("en", "English"), ("de", "German"), ("fr", "French")]
)
```

When omitted (`None`), the language selector is **hidden** and no dropdown is shown in the header. The `languages` list is forwarded through `Header` to `LanguageSelectorWidget`.

### LanguageSelectorWidget Signals

| Signal            | Type              | Description                            |
|-------------------|-------------------|----------------------------------------|
| `languageChanged` | `pyqtSignal(str)` | Emits the language **code** (e.g. `"en"`) when user selects a language |

### Connecting to Language Changes

```python
# In your widget's changeEvent:
def changeEvent(self, event):
    if event.type() == event.Type.LanguageChange:
        self.retranslate()
    super().changeEvent(event)
```

---

Previous: [Architecture](./02-architecture.md) | Next: [UI Components](./04-ui-components.md)
