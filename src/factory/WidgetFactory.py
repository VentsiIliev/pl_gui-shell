from enum import Enum


class WidgetType(Enum):
    # Core plugins - MUST match the "name" field in plugin.json files (same as PluginType)
    USER_MANAGEMENT = "User Management"  # Matches plugin.json
    SETTINGS = "Settings"  # Matches plugin.json
    DASHBOARD = "Dashboard"  # Matches plugin.json
    GALLERY = "Gallery"  # Matches plugin.json
    CALIBRATION = "Calibration"  # Matches plugin.json
    CONTOUR_EDITOR = "Contour Editor"  # Matches plugin.json - FIXED!
    GLUE_CELL_SETTINGS = "Glue Cell Settings"  # Matches plugin.json - FIXED!
    MODBUS_SETTINGS = "Modbus Settings"  # Matches plugin.json

    # Legacy/non-plugin widgets
    CREATE_WORKPIECE_OPTIONS = "Create Workpiece Options"
    DXF_BROWSER = "DXF Browser"
    SERVICE = "service"
    ANALYTICS = "analytics"
    REPORTS = "reports"
    METRICS = "metrics"

    @classmethod
    def get_from_value(cls, value):
        try:
            return cls(value)  # Enum constructor
        except ValueError:
            return None

