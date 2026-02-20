"""
Shell configuration module.

Defines the folder structure and layout for the App Shell launcher.
"""
from dataclasses import dataclass
from typing import Callable


@dataclass
class FolderDefinition:
    """Definition of a folder in the shell launcher."""
    id: int
    name: str
    translation_key: str
    display_name: str  # Default English name

    def get_translate_fn(self) -> Callable[[str], str]:
        """Return a translate function for this folder."""
        return lambda key: self.display_name


class ShellConfig:
    """Configuration for the App Shell launcher."""

    # Folder definitions - centralized configuration
    FOLDERS = [
        FolderDefinition(
            id=1,
            name="WORK",
            translation_key="folder.work",
            display_name="WORK"
        ),
        FolderDefinition(
            id=2,
            name="SERVICE",
            translation_key="folder.service",
            display_name="SERVICE"
        ),
        FolderDefinition(
            id=3,
            name="ADMINISTRATION",
            translation_key="folder.administration",
            display_name="ADMINISTRATION"
        ),
    ]

    @classmethod
    def get_folder_by_id(cls, folder_id: int) -> FolderDefinition:
        """Get folder definition by ID."""
        for folder in cls.FOLDERS:
            if folder.id == folder_id:
                return folder
        raise ValueError(f"No folder defined with ID {folder_id}")

    @classmethod
    def get_all_folder_ids(cls) -> list[int]:
        """Get all defined folder IDs."""
        return [f.id for f in cls.FOLDERS]

    @classmethod
    def folder_exists(cls, folder_id: int) -> bool:
        """Check if folder ID exists in configuration."""
        return folder_id in cls.get_all_folder_ids()

    @classmethod
    def get_folders_with_apps(cls, filtered_apps: dict[int, list]) -> list['FolderDefinition']:
        """Get only folders that have apps assigned."""
        return [f for f in cls.FOLDERS if f.id in filtered_apps and filtered_apps[f.id]]


# Convenience constants for folder IDs
FOLDER_WORK = 1
FOLDER_SERVICE = 2
FOLDER_ADMINISTRATION = 3
