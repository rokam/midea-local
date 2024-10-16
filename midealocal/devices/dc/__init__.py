"""Midea local DC device."""

import logging
from enum import StrEnum
from typing import Any

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice
from midealocal.exceptions import ValueWrongType

from .message import MessageDCResponse, MessagePower, MessageQuery, MessageStart

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea DC device attributes."""

    power = "power"
    start = "start"
    washing_data = "washing_data"
    progress = "progress"
    time_remaining = "time_remaining"


class MideaDCDevice(MideaDevice):
    """Midea DC device."""

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
                if status == DeviceAttributes.progress:
                    self._attributes[status] = progress[getattr(message, str(status))]
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
