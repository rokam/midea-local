"""Midea local B1 device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageB1Response, MessageQuery

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea local B1 device attribute."""

    door = "door"
    status = "status"
    time_remaining = "time_remaining"
    current_temperature = "current_temperature"
    tank_ejected = "tank_ejected"
    water_change_reminder = "water_change_reminder"
    water_shortage = "water_shortage"


class MideaB1Device(MideaDevice):
    """Midea B1 device."""

    _status: ClassVar[dict[int, str]] = {
        0x01: "Standby",
        0x02: "Idle",
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
        """Initialize Midea B1 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.B1,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.door: False,
                DeviceAttributes.status: None,
                DeviceAttributes.time_remaining: None,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.tank_ejected: False,
                DeviceAttributes.water_change_reminder: False,
                DeviceAttributes.water_shortage: False,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea B1 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea B1 device process message."""
        message = MessageB1Response(bytearray(msg))
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.status:
                    if value in MideaB1Device._status:
                        self._attributes[DeviceAttributes.status] = (
                            MideaB1Device._status.get(value)
                        )
                    else:
                        self._attributes[DeviceAttributes.status] = None
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea B1 device set attribute."""


class MideaAppliance(MideaB1Device):
    """Midea B1 appliance."""
