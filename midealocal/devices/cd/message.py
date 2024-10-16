"""Midea local CD message."""

from typing import Any

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class MessageCDBase(MessageRequest):
    """CD message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize CD message base."""
        super().__init__(
            device_type=DeviceType.CD,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageCDBase):
    """CD message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize CD message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageSet(MessageCDBase):
    """CD message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize CD message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X01,
        )
        self.power = False
        self.target_temperature = 0
        self.aux_heating = False
        self.fields: dict[Any, Any] = {}
        self.mode = 1

    def read_field(self, field: str) -> int:
        """CD message set read field."""
        value = self.fields.get(field, 0)
        return int(value) if value else 0

    @property
    def _body(self) -> bytearray:
        power = 0x01 if self.power else 0x00
        mode = self.mode + 1
        target_temperature = round(self.target_temperature * 2 + 30)
        return bytearray(
            [
                0x01,
                power,
                mode,
                target_temperature,
                self.read_field("trValue"),
                self.read_field("openPTC"),
                self.read_field("ptcTemp"),
                0,  # self.read_field("byte8")
            ],
        )


class CDGeneralMessageBody(MessageBody):
    """CD message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CD message general body."""
        super().__init__(body)
        self.power = (body[2] & 0x01) > 0
        self.target_temperature = round((body[3] - 30) / 2)
        if (body[2] & 0x02) > 0:
            self.mode = 0
        elif (body[2] & 0x04) > 0:
            self.mode = 1
        elif (body[2] & 0x08) > 0:
            self.mode = 2
        self.current_temperature = round((body[4] - 30) / 2)
        self.condenser_temperature = (body[7] - 30) / 2
        self.outdoor_temperature = (body[8] - 30) / 2
        self.compressor_temperature = (body[9] - 30) / 2
        self.max_temperature = round((body[10] - 30) / 2)
        self.min_temperature = round((body[11] - 30) / 2)
        self.compressor_status = (body[27] & 0x08) > 0
        if (body[28] & 0x20) > 0:
            self.mode = 3


class CD02MessageBody(MessageBody):
    """CD message 02 body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CD message 02 body."""
        super().__init__(body)
        self.fields = {}
        self.power = (body[2] & 0x01) > 0
        self.mode = body[3]
        self.target_temperature = round((body[4] - 30) / 2)
        self.fields["trValue"] = body[5]
        self.fields["openPTC"] = body[5]
        self.fields["ptcTemp"] = body[7]
        self.fields["byte8"] = body[8]


class MessageCDResponse(MessageResponse):
    """CD message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize CD message response."""
        super().__init__(bytearray(message))
        if self.message_type in [MessageType.query, MessageType.notify2]:
            self.set_body(CDGeneralMessageBody(super().body))
        elif self.message_type == MessageType.set and self.body_type == 0x01:
            self.set_body(CD02MessageBody(super().body))
        self.set_attr()
