"""Midea local DC device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice
from midealocal.exceptions import ValueWrongType

from .message import MessageDCResponse, MessagePower, MessageQuery, MessageStart

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea DC device attributes."""

    power = "power"
    start = "start"
    status = "status"
    program = "program"
    intensity = "intensity"
    dryness_level = "dryness_level"
    dry_temperature = "dry_temperature"
    error_code = "error_code"
    door_warn = "door_warn"
    ai_switch = "ai_switch"
    material = "material"
    water_box = "water_box"
    washing_data = "washing_data"
    progress = "progress"
    time_remaining = "time_remaining"


class MideaDCDevice(MideaDevice):
    """Midea DC device."""

    _status: ClassVar[dict[int, str]] = {
        1: "standby",
        2: "start",
        3: "pause",
        4: "end",
        5: "prevent_wrinkle_end",
        6: "delay_choosing",
        7: "fault",
        8: "delay",
        9: "delay_pause",
    }

    _program: ClassVar[dict[int, str]] = {
        0: "cotton",
        1: "fiber",
        2: "mixed_wash",
        3: "jean",
        4: "bedsheet",
        5: "outdoor",
        6: "down_jacket",
        7: "plush",
        8: "wool",
        9: "dehumidify",
        10: "cold_air_fresh_air",
        11: "hot_air_dry",
        12: "sport_clothes",
        13: "underwear",
        14: "baby_clothes",
        15: "shirt",
        16: "standard",
        17: "quick_dry",
        18: "fresh_air",
        19: "low_temp_dry",
        20: "eco_dry",
        21: "quick_dry_30",
        22: "towel",
        23: "intelligent_dry",
        24: "steam_care",
        25: "big",
        26: "fixed_time_dry",
        27: "night_dry",
        28: "bracket_dry",
        29: "western_trouser",
        30: "dehumidification",
        31: "smart_dry",
        32: "four_piece_suit",
        33: "warm_clothes",
        34: "quick_dry_20",
        35: "steam_sterilize",
        36: "enzyme",
        37: "big_60",
        38: "steam_no_iron",
        39: "air_wash",
        40: "bed_clothes",
        41: "little_fast_dry",
        42: "small_piece_dry",
        43: "big_dry",
        44: "wool_nurse",
        45: "sun_quilt",
        46: "fresh_remove_smell",
        47: "bucket_self_clean",
        48: "silk",
        49: "sterilize",
    }

    def __init__(
        self,
        name: str,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        device_protocol: ProtocolVersion,
        model: str,
        subtype: int,
        customize: str,  # noqa: ARG002
    ) -> None:
        """Initialize Midea DC device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.DC,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.start: False,
                DeviceAttributes.status: "Unknown",
                DeviceAttributes.program: "None",
                DeviceAttributes.intensity: None,
                DeviceAttributes.dryness_level: None,
                DeviceAttributes.dry_temperature: None,
                DeviceAttributes.error_code: None,
                DeviceAttributes.door_warn: None,
                DeviceAttributes.ai_switch: None,
                DeviceAttributes.material: None,
                DeviceAttributes.water_box: None,
                DeviceAttributes.washing_data: bytearray([]),
                DeviceAttributes.progress: "Unknown",
                DeviceAttributes.time_remaining: None,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea DC device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea DC device process message."""
        message = MessageDCResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        progress = [
            "Prog0",
            "Prog1",
            "Prog2",
            "Prog3",
            "Prog4",
            "Prog5",
            "Prog6",
            "Prog7",
        ]
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                # parse progress
                if status == DeviceAttributes.progress:
                    self._attributes[status] = progress[value]
                # parse status
                elif status == DeviceAttributes.status:
                    if value in MideaDCDevice._status:
                        self._attributes[DeviceAttributes.status] = (
                            MideaDCDevice._status.get(value)
                        )
                    else:
                        self._attributes[DeviceAttributes.status] = None
                # parse program
                elif status == DeviceAttributes.program:
                    if value in MideaDCDevice._program:
                        self._attributes[DeviceAttributes.program] = (
                            MideaDCDevice._program.get(value)
                        )
                    else:
                        self._attributes[DeviceAttributes.program] = None
                else:
                    self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea DC device set attribute."""
        if not isinstance(value, bool):
            raise ValueWrongType("[dc] Expected bool")
        message: MessagePower | MessageStart | None = None
        if attr == DeviceAttributes.power:
            message = MessagePower(self._message_protocol_version)
            message.power = value
            self.build_send(message)
        elif attr == DeviceAttributes.start:
            message = MessageStart(self._message_protocol_version)
            message.start = value
            message.washing_data = self._attributes[DeviceAttributes.washing_data]
            self.build_send(message)


class MideaAppliance(MideaDCDevice):
    """Midea DC appliance."""
