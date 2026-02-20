import enum

from PyQt6.QtWidgets import QComboBox, QApplication
from PyQt6.QtCore import pyqtSignal, QEvent


# crea Language Mock
class Language(enum.Enum):
    ENGLISH = "English"
    BULGARIAN = "Bulgarian"

    @property
    def display_name(self):
        return self.value


class LanguageSelectorWidget(QComboBox):
    """
    Language selector that emits Qt LanguageChange events.

    When language changes:
    1. Emits custom languageChanged signal (for backward compatibility)
    2. Posts QEvent.LanguageChange to all top-level widgets
    3. Widgets handle it in changeEvent() and call retranslateUi()
    """
    languageChanged = pyqtSignal(Language)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_language = Language.ENGLISH

        self.languages = list(Language)
        self.language_name_to_enum = {lang.display_name: lang for lang in self.languages}

        # Populate dropdown
        self.addItems([lang.display_name for lang in self.languages])

        # Set current language
        self.updateSelectedLang()

        self.currentIndexChanged.connect(self._on_language_change)

    def _on_language_change(self, index):
        """Handle language change and emit Qt LanguageChange events"""
        selected_text = self.currentText()
        selected_enum = self.language_name_to_enum[selected_text]

        # Update current language
        self.current_language = selected_enum

        # Emit custom signal for backward compatibility
        self.languageChanged.emit(selected_enum)

        # Post LanguageChange event to all top-level widgets (Qt standard way)
        self._post_language_change_events()

    def _post_language_change_events(self):
        """Post LanguageChange event to all top-level widgets in the application"""
        app = QApplication.instance()
        if app and isinstance(app, QApplication):
            # Send to all top-level widgets
            for widget in app.topLevelWidgets():
                event = QEvent(QEvent.Type.LanguageChange)
                app.postEvent(widget, event)
            print(f"[LanguageSelector] Posted LanguageChange events to {len(app.topLevelWidgets())} top-level widgets")

    def updateSelectedLang(self):
        """Update the selected language in the dropdown"""
        self.setCurrentIndex(self.findText(self.current_language.display_name))


