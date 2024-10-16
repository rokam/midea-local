"""Midea local E8 device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageE8Response, MessageQuery

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea E8 device."""

    status = "status"
    time_remaining = "time_remaining"
    keep_warm_remaining = "keep_warm_remaining"
    working_time = "working_time"
    target_temperature = "target_temperature"
    current_temperature = "current_temperature"
    finished = "finished"
    water_shortage = "water_shortage"


class MideaE8Device(MideaDevice):
    """Midea E8 device."""

    _status: ClassVar[dict[int, str]] = {
        0x00: "Standby",
        0x01: "Delay",
        0x02: "Working",
        0x03: "Paused",
        0x04: "Keep-Warming",
        0xFF: "Error",
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
        """Initialize Midea E8 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.E8,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.status: None,
                DeviceAttributes.time_remaining: None,
                DeviceAttributes.keep_warm_remaining: None,
                DeviceAttributes.working_time: None,
                DeviceAttributes.target_temperature: None,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.finished: None,
                DeviceAttributes.water_shortage: None,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea E8 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea E8 device process message."""
        message = MessageE8Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.status:
                    if value in MideaE8Device._status:
                        self._attributes[DeviceAttributes.status] = (
                            MideaE8Device._status.get(value)
                        )
                    else:
                        self._attributes[DeviceAttributes.status] = None
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea E8 device set attribute."""


class MideaAppliance(MideaE8Device):
    """Midea E8 appliance."""
