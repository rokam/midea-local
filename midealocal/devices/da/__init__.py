"""Midea local DA device."""

import logging
from enum import StrEnum
from typing import Any

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice
from midealocal.exceptions import ValueWrongType

from .message import MessageDAResponse, MessagePower, MessageQuery, MessageStart

_LOGGER = logging.getLogger(__name__)

MIN_TEMP = 15


class DeviceAttributes(StrEnum):
    """Midea DA device attributes."""

    power = "power"
    start = "start"
    washing_data = "washing_data"
    program = "program"
    progress = "progress"
    time_remaining = "time_remaining"
    wash_time = "wash_time"
    soak_time = "soak_time"
    dehydration_time = "dehydration_time"
    dehydration_speed = "dehydration_speed"
    error_code = "error_code"
    rinse_count = "rinse_count"
    rinse_level = "rinse_level"
    wash_level = "wash_level"
    wash_strength = "wash_strength"
    softener = "softener"
    detergent = "detergent"


class MideaDADevice(MideaDevice):
    """Midea DA device."""

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
        """Initialize Midea DA device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.DA,
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
                DeviceAttributes.error_code: None,
                DeviceAttributes.washing_data: bytearray([]),
                DeviceAttributes.program: None,
                DeviceAttributes.progress: "Unknown",
                DeviceAttributes.time_remaining: None,
                DeviceAttributes.wash_time: None,
                DeviceAttributes.soak_time: None,
                DeviceAttributes.dehydration_time: None,
                DeviceAttributes.dehydration_speed: None,
                DeviceAttributes.rinse_count: None,
                DeviceAttributes.rinse_level: None,
                DeviceAttributes.wash_level: None,
                DeviceAttributes.wash_strength: None,
                DeviceAttributes.softener: None,
                DeviceAttributes.detergent: None,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea DA device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea DA device process message."""
        message = MessageDAResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        progress = ["Idle", "Spin", "Rinse", "Wash", "Weight", "Unknown", "Dry", "Soak"]
        program = [
            "Standard",
            "Fast",
            "Blanket",
            "Wool",
            "embathe",
            "Memory",
            "Child",
            "Down Jacket",
            "Stir",
            "Mute",
            "Bucket Self Clean",
            "Air Dry",
        ]
        speed = ["-", "Low", "Medium", "High"]
        strength = ["-", "Week", "Medium", "Strong"]
        detergent = [
            "No",
            "Less",
            "Medium",
            "More",
            "4",
            "5",
            "6",
            "7",
            "8",
            "Insufficient",
        ]
        softener = [
            "No",
            "Intelligent",
            "Programed",  # codespell:ignore
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "Insufficient",
        ]
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.progress:
                    self._attributes[status] = (
                        None if value >= len(progress) else progress[value]
                    )
                elif status == DeviceAttributes.program:
                    self._attributes[status] = (
                        None if value >= len(program) else program[value]
                    )
                elif status == DeviceAttributes.rinse_level:
                    self._attributes[status] = "-" if value == MIN_TEMP else value
                elif status == DeviceAttributes.dehydration_speed:
                    self._attributes[status] = (
                        None if value >= len(speed) else speed[value]
                    )
                elif status == DeviceAttributes.detergent:
                    self._attributes[status] = (
                        None if value >= len(detergent) else detergent[value]
                    )
                elif status == DeviceAttributes.softener:
                    self._attributes[status] = (
                        None if value >= len(softener) else softener[value]
                    )
                elif status == DeviceAttributes.wash_strength:
                    self._attributes[status] = (
                        None if value >= len(strength) else strength[value]
                    )
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea DA device set attribute."""
        if not isinstance(value, bool):
            raise ValueWrongType("[da] Expected bool")
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


class MideaAppliance(MideaDADevice):
    """Midea DA appliance."""
