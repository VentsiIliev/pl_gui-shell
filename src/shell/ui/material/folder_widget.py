from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtWidgets import (
    QFrame, QLabel, QGridLayout, QVBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy
)

from .menu_icon import MenuIcon


class LayoutManager:
    """Material Design 3 layout management"""

    def __init__(self, folder_widget):
        self.folder = folder_widget
        self.min_size = QSize(300, 340)
        self.max_size = QSize(480, 520)
        self.preferred_aspect_ratio = 0.88
        self._resize_timer = None

    def setup_responsive_sizing(self):
        self.folder.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.folder.setMinimumSize(self.min_size)
        self.folder.setMaximumSize(self.max_size)

    def update_main_layout_margins(self):
        current_width = self.folder.width() if self.folder.width() > 0 else self.min_size.width()
        margin = max(16, min(24, int(current_width * 0.05)))
        spacing = max(12, min(20, int(current_width * 0.04)))
        self.folder.main_layout.setContentsMargins(margin, margin, margin, margin)
        self.folder.main_layout.setSpacing(spacing)

    def update_header_layout_spacing(self):
        self.folder.header_layout.setSpacing(16)

    def update_preview_layout_margins(self):
        preview_width = self.folder.folder_preview.width() if self.folder.folder_preview.width() > 0 else 200
        margin = max(16, min(28, int(preview_width * 0.08)))
        spacing = max(8, min(16, int(preview_width * 0.04)))
        self.folder.preview_layout.setContentsMargins(margin, margin, margin, margin)
        self.folder.preview_layout.setSpacing(spacing)

    def calculate_icon_size(self):
        preview_width = self.folder.folder_preview.width() if self.folder.folder_preview.width() > 0 else 200
        preview_height = self.folder.folder_preview.height() if self.folder.folder_preview.height() > 0 else 200
        available_size = min(preview_width, preview_height)
        margins = self.folder.preview_layout.contentsMargins()
        total_margin = margins.left() + margins.right()
        spacing = self.folder.preview_layout.spacing()
        icon_size = max(64, min(96, int((available_size - total_margin - spacing) / 2.2)))
        return icon_size

    def update_typography(self):
        current_width = self.folder.width() if self.folder.width() > 0 else self.min_size.width()
        font_size = max(18, min(28, int(current_width * 0.06)))
        font = QFont("Roboto", font_size, QFont.Weight.Medium)
        if not font.exactMatch():
            font = QFont("Segoe UI", font_size, QFont.Weight.Medium)
        self.folder.title_label.setFont(font)

    def handle_resize_event(self):
        if self.folder.parent():
            available_width = self.folder.parent().width()
            target_width = max(self.min_size.width(),
                               min(int(available_width * 0.3), self.max_size.width()))
            target_height = int(target_width / self.preferred_aspect_ratio)
            self.folder.setFixedSize(QSize(target_width, target_height))

        self.update_main_layout_margins()
        self.update_typography()

        if self._resize_timer:
            self._resize_timer.stop()
        else:
            self._resize_timer = QTimer()
            self._resize_timer.setSingleShot(True)
            self._resize_timer.timeout.connect(self.folder.update_folder_preview)
        self._resize_timer.start(150)


class FolderWidget(QFrame):
    """Pure UI component - only handles visual presentation"""

    clicked = pyqtSignal()
    outside_clicked = pyqtSignal()

    def __init__(self, ID, folder_name="Apps", parent=None):
        super().__init__(parent)
        self.ID = ID
        self.folder_name = folder_name
        self.buttons = []
        self.is_grayed_out = False
        self.layout_manager = LayoutManager(self)
        self.setup_ui()
        self.setAcceptDrops(True)
        self.translate_fn = None

    def update_title_label(self, message=None):
        if self.translate_fn:
            title = self.translate_fn(self.folder_name)
        else:
            return

        self.title_label.setText(title)

    def folder_clicked(self, event):
        """Handle folder preview click - just emit signal"""
        if not self.is_grayed_out:
            self.clicked.emit()

    def setup_ui(self):
        """Material Design 3 UI setup - pure presentation"""
        self.layout_manager.setup_responsive_sizing()

        self.setStyleSheet("""
            QFrame {
                background: #FFFBFE;
                border: 1px solid #E7E0EC;
                border-radius: 24px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        self.main_layout = QVBoxLayout(self)
        self.layout_manager.update_main_layout_margins()

        self.header_widget = QFrame()
        self.header_layout = QVBoxLayout(self.header_widget)
        self.layout_manager.update_header_layout_spacing()

        self.folder_preview = QFrame()
        self.folder_preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.folder_preview.setStyleSheet("""
            QFrame {
                background: #FFFBFE;
                border: 1px solid #E7E0EC;
                border-radius: 28px;
            }
        """)

        preview_shadow = QGraphicsDropShadowEffect()
        preview_shadow.setBlurRadius(20)
        preview_shadow.setColor(QColor(103, 80, 164, 30))
        preview_shadow.setOffset(0, 4)
        self.folder_preview.setGraphicsEffect(preview_shadow)
        self.folder_preview.mousePressEvent = self.folder_clicked

        self.preview_layout = QGridLayout(self.folder_preview)
        self.layout_manager.update_preview_layout_margins()

        self.title_label = QLabel(self.folder_name)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.title_label.setWordWrap(True)
        self.layout_manager.update_typography()

        self.title_label.setStyleSheet("""
            QLabel {
                color: #1D1B20;
                background-color: transparent;
                border: none;
                padding: 12px 16px;
                font-weight: 500;
                letter-spacing: 0px;
            }
        """)

        self.header_layout.addWidget(self.folder_preview, 1)
        self.header_layout.addWidget(self.title_label, 0)
        self.main_layout.addWidget(self.header_widget)
        self.update_folder_preview()

    def update_folder_preview(self):
        """Update folder preview icons - pure UI operation"""
        for i in reversed(range(self.preview_layout.count())):
            child = self.preview_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        self.layout_manager.update_preview_layout_margins()
        icon_size = self.layout_manager.calculate_icon_size()
        inner_icon_size = max(48, int(icon_size * 0.7))

        preview_apps = self.buttons[:4]
        for i, app in enumerate(preview_apps):
            row, col = divmod(i, 2)

            mini_icon = QLabel()
            mini_icon.setFixedSize(icon_size, icon_size)
            mini_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            border_radius = max(16, min(28, int(icon_size * 0.25)))
            mini_icon.setStyleSheet(f"""
                QLabel {{
                    background: #6750A4;
                    border: none;
                    border-radius: {border_radius}px;
                    font-size: {max(12, int(icon_size * 0.18))}px;
                    font-weight: 500;
                    color: white;
                    font-family: 'Roboto', 'Segoe UI', sans-serif;
                }}
            """)

            try:
                mini_shadow = QGraphicsDropShadowEffect()
                mini_shadow.setBlurRadius(8)
                mini_shadow.setColor(QColor(103, 80, 164, 40))
                mini_shadow.setOffset(0, 2)
                mini_icon.setGraphicsEffect(mini_shadow)
            except Exception:
                pass

            icon_loaded = False
            try:
                pixmap = QPixmap(app.icon_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        inner_icon_size, inner_icon_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    mini_icon.setPixmap(scaled_pixmap)
                    icon_loaded = True
            except Exception:
                pass

            if not icon_loaded:
                mini_icon.setText("\U0001f4f1")
                placeholder_font_size = max(20, int(icon_size * 0.35))
                mini_icon.setStyleSheet(mini_icon.styleSheet() + f"font-size: {placeholder_font_size}px;")

            self.preview_layout.addWidget(mini_icon, row, col)

    def set_grayed_out(self, grayed_out):
        """Update visual disabled state"""
        self.is_grayed_out = grayed_out

        if grayed_out:
            # Outer frame
            self.setStyleSheet("""
                QFrame {
                    background: #EDE7F6;
                    border: 1px dashed #B0A7BC;
                    border-radius: 24px;
                }
            """)

            # Title text
            self.title_label.setStyleSheet("""
                QLabel {
                    color: #9C9A9E;
                    background-color: transparent;
                    border: none;
                    padding: 12px 16px;
                    font-weight: 500;
                    letter-spacing: 0px;
                }
            """)

            # Folder preview (icons background dimmed)
            self.folder_preview.setStyleSheet("""
                QFrame {
                    background: #F3EDF7;
                    border: 1px solid #C4C0CA;
                    border-radius: 28px;
                }
            """)

            # Dim all child icons
            for i in range(self.preview_layout.count()):
                child = self.preview_layout.itemAt(i).widget()
                if child:
                    child.setGraphicsEffect(None)  # remove shadows
                    child.setStyleSheet(child.styleSheet() + "opacity: 0.4;")

        else:
            # Outer frame
            self.setStyleSheet("""
                QFrame {
                    background: #FFFBFE;
                    border: 1px solid #E7E0EC;
                    border-radius: 24px;
                }
            """)

            # Reset title
            self.title_label.setStyleSheet("""
                QLabel {
                    color: #1D1B20;
                    background-color: transparent;
                    border: none;
                    padding: 12px 16px;
                    font-weight: 500;
                    letter-spacing: 0px;
                }
            """)

            # Reset preview
            self.folder_preview.setStyleSheet("""
                QFrame {
                    background: #FFFBFE;
                    border: 1px solid #E7E0EC;
                    border-radius: 28px;
                }
            """)

            # Reset icons (restore drop shadow + normal look)
            self.update_folder_preview()

    def add_app(self, app_name, icon_path="", callback=None):
        """Add app to UI - no business logic"""
        app_icon = MenuIcon(app_name, icon_path, "", callback)
        self.buttons.append(app_icon)
        self.update_folder_preview()

    def sizeHint(self):
        return QSize(380, 420)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.layout_manager.handle_resize_event()
