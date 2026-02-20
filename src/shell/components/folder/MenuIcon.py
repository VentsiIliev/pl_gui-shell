import os
import sys

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QGridLayout, QPushButton, QGraphicsDropShadowEffect)

from .managers.AnimationManager import AnimationManager

class MenuIcon(QPushButton):
    """Material Design 3 app icon with proper touch targets and visual feedback"""

    button_clicked = pyqtSignal(str)

    def __init__(self, icon_label, icon_path, icon_text="", callback=None, parent=None):
        super().__init__(parent)
        self.icon_label = icon_label
        self.icon_path = icon_path
        self.icon_text = icon_text
        self.callback = callback

        # Material Design touch target size (minimum 48dp)
        self.setFixedSize(112, 112)  # 112dp for comfortable touch interaction
        self.setup_ui()
        # self.setup_animations()
        self.animation_manager = AnimationManager(self)

        # Connect callback if provided
        if self.callback is not None:
            self.button_clicked.connect(self.callback)

    def setup_ui(self):
        """Setup Material Design 3 styling with proper tokens"""

        # Material Design 3 filled button styling
        self.setStyleSheet("""
            QPushButton {
                background: #6750A4;
                color: #FFFFFF;
                border: none;
                border-radius: 28px;
                font-size: 12px;
                font-weight: 500;
                font-family: 'Roboto', 'Segoe UI', sans-serif;
                text-align: center;
                padding: 8px;
            }
            QPushButton:hover {
                background: #7965AF;
            }
            QPushButton:pressed {
                background: #5A3D99;
            }
            QPushButton:disabled {
                background: #E8DEF8;
                color: #79747E;
            }
        """)

        # Material Design elevation shadow (level 1)
        try:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(12)
            shadow.setColor(QColor(103, 80, 164, 40))  # Primary color shadow
            shadow.setOffset(0, 2)
            self.setGraphicsEffect(shadow)
        except:
            pass

        # Setup icon and text with Material Design principles
        self.setup_icon_content()

        # Material Design tooltip
        self.setToolTip(self.icon_label)

    def setup_icon_content(self):
        """Setup icon content following Material Design icon guidelines"""

        # Handle QIcon object directly
        if isinstance(self.icon_path, QIcon):
            if not self.icon_path.isNull():
                self.setIcon(self.icon_path)
                icon_size = int(self.width() * 0.5)
                self.setIconSize(QSize(icon_size, icon_size))
                self.setText("")
                return
        # Try to load actual icon from path
        elif self.icon_path and isinstance(self.icon_path, str) and os.path.exists(self.icon_path):
            try:
                icon = QIcon(self.icon_path)
                if not icon.isNull():
                    self.setIcon(icon)
                    icon_size = int(self.width() * 0.5)
                    self.setIconSize(QSize(icon_size, icon_size))
                    self.setText("")
                    return
            except Exception as e:
                print(f"Error loading icon: {e}")

        # Fallback to Material Design text representation
        self.setup_fallback_text()

    def setup_fallback_text(self):
        """Setup fallback text with Material Design typography"""

        # Use emoji or abbreviation for better visual representation
        if self.icon_text and self.icon_text != " No text and icon provided":
            display_text = self.icon_text
        else:
            # Create abbreviation from app name (Material Design pattern)
            words = self.icon_label.split()
            if len(words) >= 2:
                display_text = ''.join(word[0].upper() for word in words[:2])
            else:
                display_text = self.icon_label[:2].upper()

        self.setText(display_text)

        # Adjust font size based on text length for optimal readability
        if len(display_text) <= 2:
            font_size = 18  # Larger for abbreviations
        else:
            font_size = 14  # Smaller for longer text

        # Update stylesheet for text-only display
        self.setStyleSheet(self.styleSheet() + f"""
            QPushButton {{
                font-size: {font_size}px;
                font-weight: 500;
                letter-spacing: 0.5px;
            }}
        """)

    def enterEvent(self, event):
        """Material Design hover state"""
        super().enterEvent(event)

        # Update shadow for hover state (Material Design elevation change)
        try:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(16)
            shadow.setColor(QColor(103, 80, 164, 60))  # Deeper shadow on hover
            shadow.setOffset(0, 4)
            self.setGraphicsEffect(shadow)
        except:
            pass

    def leaveEvent(self, event):
        """Material Design normal state restoration"""
        super().leaveEvent(event)

        # Restore normal shadow
        try:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(12)
            shadow.setColor(QColor(103, 80, 164, 40))
            shadow.setOffset(0, 2)
            self.setGraphicsEffect(shadow)
        except:
            pass

    def mousePressEvent(self, event):
        """Material Design press interaction"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._original_rect = self.geometry()
            self.animation_manager.create_button_press_animation()
            self.button_clicked.emit(self.icon_label)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Material Design release interaction"""
        if event.button() == Qt.MouseButton.LeftButton and self._original_rect:
            self.animation_manager.create_button_release_animation(self._original_rect)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        """Custom paint event for Material Design visual consistency"""
        super().paintEvent(event)

        # Additional Material Design visual enhancements can be added here
        # For now, we rely on stylesheet and shadow effects

    def sizeHint(self):
        """Material Design size hint"""
        return QSize(112, 112)  # Consistent Material Design touch target

    def minimumSizeHint(self):
        """Minimum size following Material Design guidelines"""
        return QSize(48, 48)  # Material Design minimum touch target

    def set_icon_from_path(self, icon_path):
        """Update icon from new path with Material Design handling"""
        self.icon_path = icon_path
        self.setup_icon_content()

    def set_material_style(self, style_variant="primary"):
        """Apply different Material Design style variants"""

        style_variants = {
            "primary": {
                "background": "#6750A4",
                "hover": "#7965AF",
                "pressed": "#5A3D99",
                "text_color": "#FFFFFF"
            },
            "secondary": {
                "background": "#E8DEF8",
                "hover": "#DDD2EA",
                "pressed": "#D1C6DD",
                "text_color": "#6750A4"
            },
            "tertiary": {
                "background": "#F7F2FA",
                "hover": "#F0EBEF",
                "pressed": "#E9E3E4",
                "text_color": "#7D5260"
            }
        }

        if style_variant in style_variants:
            colors = style_variants[style_variant]

            self.setStyleSheet(f"""
                QPushButton {{
                    background: {colors['background']};
                    color: {colors['text_color']};
                    border: none;
                    border-radius: 28px;
                    font-size: 12px;
                    font-weight: 500;
                    font-family: 'Roboto', 'Segoe UI', sans-serif;
                    text-align: center;
                    padding: 8px;
                }}
                QPushButton:hover {{
                    background: {colors['hover']};
                }}
                QPushButton:pressed {{
                    background: {colors['pressed']};
                }}
                QPushButton:disabled {{
                    background: #E8DEF8;
                    color: #79747E;
                }}
            """)

    def set_material_size(self, size_variant="standard"):
        """Apply different Material Design size variants"""

        size_variants = {
            "compact": QSize(80, 80),
            "standard": QSize(112, 112),
            "large": QSize(144, 144)
        }

        if size_variant in size_variants:
            new_size = size_variants[size_variant]
            self.setFixedSize(new_size)

            # Update border radius proportionally
            radius = min(new_size.width(), new_size.height()) // 4

            current_style = self.styleSheet()
            # Update border-radius in stylesheet
            import re
            updated_style = re.sub(
                r'border-radius:\s*\d+px',
                f'border-radius: {radius}px',
                current_style
            )
            self.setStyleSheet(updated_style)

            # Update icon size proportionally
            if hasattr(self, 'icon') and not self.icon().isNull():
                icon_size = min(new_size.width(), new_size.height()) // 2
                self.setIconSize(QSize(icon_size, icon_size))

