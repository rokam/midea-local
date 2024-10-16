"""Midea local B8 device const."""

from enum import IntEnum, StrEnum


class B8DeviceAttributes(StrEnum):
    """Midea B8 device attributes."""

    WORK_STATUS = "work_status"
    FUNCTION_TYPE = "function_type"
    CONTROL_TYPE = "control_type"
    MOVE_DIRECTION = "move_direction"
    CLEAN_MODE = "clean_mode"
    FAN_LEVEL = "fan_level"
    AREA = "area"
    WATER_LEVEL = "water_level"
    VOICE_VOLUME = "voice_volume"
    MOP = "mop"
    CARPET_SWITCH = "carpet_switch"
    SPEED = "speed"
    HAVE_RESERVE_TASK = "have_reserve_task"
    BATTERY_PERCENT = "battery_percent"
    WORK_TIME = "work_time"
    UV_SWITCH = "uv_switch"
    WIFI_SWITCH = "wifi_switch"
    VOICE_SWITCH = "voice_switch"
    COMMAND_SOURCE = "command_source"
    ERROR_TYPE = "error_type"
    ERROR_DESC = "error_desc"
    DEVICE_ERROR = "device_error"
    BOARD_COMMUNICATION_ERROR = "board_communication_error"
    LASER_SENSOR_SHELTER = "laser_sensor_shelter"
    LASER_SENSOR_ERROR = "laser_sensor_error"


class B8WorkMode(IntEnum):
    """Midea B8 work mode."""

    CHARGE = 0x01
    WORK = 0x02
    STOP = 0x03
    PAUSE = 0x1B


class B8WorkStatus(IntEnum):
    """Midea B8 work status."""

    NONE = 0x00
    CHARGE = 0x01
    WORK = 0x02
    STOP = 0x03
    CHARGING_ON_DOCK = 0x04
    RESERVE_TASK_FINISHED = 0x05
    CHARGE_FINISH = 0x06
    CHARGING_WITH_WIRE = 0x07
    PAUSE = 0x08
    UPDATING = 0x09
    SAVING_MAP = 0x0A
    ERROR = 0x0B
    SLEEP = 0x0C
    CHARGE_PAUSE = 0x0D
    RELOCATE = 0x0E
    ELECTROLYSED_WATER_MAKING = 0x0F
    DUST_COLLECTING = 0x10
    BACK_DUST_COLLECTING = 0x11
    SLEEP_IN_STATION = 0x12


class B8FunctionType(IntEnum):
    """Midea B8 function type."""

    NONE = 0x00
    DUST_BOX_CLEANING = 0x01
    WATER_TANK_CLEANING = 0x02


class B8ControlType(IntEnum):
    """Midea B8 control type."""

    NONE = 0x0
    MANUAL = 0x1
    AUTO = 0x2


class B8Moviment(IntEnum):
    """Midea B8 movement."""

    NONE = 0x0
    FORWARD = 0x1
    BACK = 0x2
    LEFT = 0x3
    RIGHT = 0x4


class B8CleanMode(IntEnum):
    """Midea B8 clean mode."""

    NONE = 0x00
    RANDOM = 0x01
    ARC = 0x02
    EDGE = 0x03
    EMPHASES = 0x04
    SCREW = 0x05
    BED = 0x06
    WIDE_SCREW = 0x07
    AUTO = 0x08
    AREA = 0x09
    ZONE_INDEX = 0x0A
    ZONE_RECT = 0x0B
    PATH = 0x0C


class B8FanLevel(IntEnum):
    """Midea B8 fan level."""

    OFF = 0x0
    SOFT = 0x1
    NORMAL = 0x2
    HIGH = 0x3
    LOW = 0x4


class B8WaterLevel(IntEnum):
    """Midea B8 water level."""

    OFF = 0x0
    LOW = 0x1
    NORMAL = 0x2
    HIGH = 0x3


class B8MopState(IntEnum):
    """Midea B8 mop state."""

    OFF = 0x0
    ON = 0x1
    LACK_WATER = 0x2


class B8Speed(IntEnum):
    """Midea B8 speed."""

    LOW = 0x1
    HIGH = 0x0


class B8ErrorType(IntEnum):
    """Midea B8 error type."""

    NO = 0x00
    CAN_FIX = 0x01
    REBOOT = 0x02
    WARNING = 0x03


class B8ErrorCanFixDescription(IntEnum):
    """Midea B8 error can fix description."""

    NO = 0x0
    FIX_DUST = 0x01
    FIX_WHEEL_HANG = 0x02
    FIX_WHEEL_OVERLOAD = 0x03
    FIX_SIDE_BRUSH_OVERLOAD = 0x04
    FIX_ROLL_BRUSH_OVERLOAD = 0x05
    FIX_DUST_ENGINE = 0x06
    FIX_FRONT_PANEL = 0x07
    FIX_RADAR_MASK = 0x08
    FIX_DROP_SENSOR = 0x09
    FIX_LOW_BATTERY = 0x0A
    FIX_ABNORMAL_POSTURE = 0x0B
    FIX_LASER_SENSOR = 0x0C
    FIX_EDGE_SENSOR = 0x0D
    FIX_START_IN_FORBID_AREA = 0x0E
    FIX_START_IN_STRONG_MAGNETIC = 0x0F
    FIX_LASER_SENSOR_BLOCKED = 0x10


class B8ErrorRebootDescription(IntEnum):
    """Midea B8 error reboot description."""

    NO = 0x00
    REBOOT_LASER_COMM_FAIL = 0x01
    REBOOT_ROBOT_COMM_FAIL = 0x02
    REBOOT_INNER_FAIL = 0x03


class B8ErrorWarningDescription(IntEnum):
    """Midea B8 error warning description."""

    NO = 0x00
    WARN_LOCATION_FAIL = 0x01
    WARN_LOW_BATTERY = 0x02
    WARN_FULL_DUST = 0x03
    WARN_LOW_WATER = 0x04


class B8StatusType(IntEnum):
    """B8 Status Type."""

    X01 = 0x01
