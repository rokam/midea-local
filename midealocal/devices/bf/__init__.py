"""Midea local BF device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageBFResponse, MessageQuery

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea BF device attributes."""

    door = "door"
    status = "status"
    time_remaining = "time_remaining"
    current_temperature = "current_temperature"
    tank_ejected = "tank_ejected"
    water_change_reminder = "water_change_reminder"
    water_shortage = "water_shortage"


class MideaBFDevice(MideaDevice):
    """Midea BF device."""

    _status: ClassVar[dict[int, str]] = {
        0x01: "PowerSave",
        0x02: "Standby",
        0x03: "Working",
        0x04: "Finished",
        0x05: "Delay",
        0x06: "Paused",
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
        """Initialize Midea BF device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.BF,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.door: None,
                DeviceAttributes.status: None,
                DeviceAttributes.time_remaining: None,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.tank_ejected: None,
                DeviceAttributes.water_change_reminder: None,
                DeviceAttributes.water_shortage: None,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea BF device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea BF device process message."""
        message = MessageBFResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.status:
                    if value in MideaBFDevice._status:
                        self._attributes[DeviceAttributes.status] = (
                            MideaBFDevice._status.get(value)
                        )
                    else:
                        self._attributes[DeviceAttributes.status] = "Unknown"
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea BF device set attribute."""


class MideaAppliance(MideaBFDevice):
    """Midea BF appliance."""
