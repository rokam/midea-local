"""Midea local message."""

import logging
from enum import IntEnum
from typing import Generic, SupportsIndex, TypeVar, cast

_LOGGER = logging.getLogger(__name__)


class BodyType(IntEnum):
    """Body Type."""

    A0 = 0xA0
    A1 = 0xA1
    A4 = 0xA4
    B0 = 0xB0
    B1 = 0xB1
    B5 = 0xB5
    BB = 0xBB
    C0 = 0xC0
    C1 = 0xC1
    C3 = 0xC3
    C8 = 0xC8
    FF = 0xFF
    X00 = 0x00
    X01 = 0x01
    X02 = 0x02
    X03 = 0x03
    X04 = 0x04
    X05 = 0x05
    X06 = 0x06
    X07 = 0x07
    X0A = 0x0A
    X11 = 0x11
    X21 = 0x21
    X22 = 0x22
    X24 = 0x24
    X31 = 0x31
    X32 = 0x32
    X41 = 0x41
    X80 = 0x80


class SubBodyType(IntEnum):
    """Sub Body Type."""

    A0 = 0xA0
    A1 = 0xA1
    A2 = 0xA2
    B0 = 0xB0
    B1 = 0xB1
    B5 = 0xB5
    BB = 0xBB
    C0 = 0xC0
    C1 = 0xC1
    C3 = 0xC3
    X01 = 0x01
    X02 = 0x02
    X03 = 0x03
    X04 = 0x04
    X05 = 0x05
    X06 = 0x06
    X0A = 0x0A
    X10 = 0x10
    X11 = 0x11
    X12 = 0x12
    X13 = 0x13
    X16 = 0x16
    X20 = 0x20
    X21 = 0x21
    X22 = 0x22
    X24 = 0x24
    X30 = 0x30
    X31 = 0x31
    X32 = 0x32
    X3D = 0x3D
    X41 = 0x41
    X52 = 0x52


class MessageLenError(Exception):
    """Message length exception."""


class MessageBodyError(Exception):
    """Message body exception."""


class MessageCheckSumError(Exception):
    """Message checksum exception."""


class MessageType(IntEnum):
    """Message type."""

    set = (0x02,)
    query = (0x03,)
    notify1 = (0x04,)
    notify2 = (0x05,)
    exception = (0x06,)
    exception2 = (0x0A,)
    query_appliance = 0xA0


NONE_VALUE = 0x00


class MessageBase:
    """Message base."""

    HEADER_LENGTH = 10

    def __init__(self) -> None:
        """Initialize message base."""
        self._device_type = NONE_VALUE
        self._message_type = NONE_VALUE
        self._body_type = NONE_VALUE
        self._protocol_version = NONE_VALUE

    @staticmethod
    def checksum(data: bytes) -> SupportsIndex:
        """Message checksum."""
        return cast(SupportsIndex, (~sum(data) + 1) & 0xFF)

    @property
    def header(self) -> bytearray:
        """Message header."""
        raise NotImplementedError

    @property
    def body(self) -> bytearray:
        """Message body."""
        raise NotImplementedError

    @property
    def message_type(self) -> int:
        """Message type."""
        return self._message_type

    @message_type.setter
    def message_type(self, value: int) -> None:
        self._message_type = value

    @property
    def device_type(self) -> int:
        """Message device type."""
        return self._device_type

    @device_type.setter
    def device_type(self, value: int) -> None:
        self._device_type = value

    @property
    def body_type(self) -> int:
        """Message body type."""
        return self._body_type

    @body_type.setter
    def body_type(self, value: int) -> None:
        self._body_type = value

    @property
    def protocol_version(self) -> int:
        """Message protocol version."""
        return self._protocol_version

    @protocol_version.setter
    def protocol_version(self, protocol_version: int) -> None:
        self._protocol_version = protocol_version

    def __str__(self) -> str:
        """Parse to string."""
        output = {
            "header": self.header.hex(),
            "body": self.body.hex(),
            "message type": f".{f'{self.message_type:02x}'}",
            "body type": (
                f".{f'{self._body_type:02x}'}"
                if self._body_type != NONE_VALUE
                else "None"
            ),
        }
        return str(output)


class MessageRequest(MessageBase):
    """Message request."""

    def __init__(
        self,
        device_type: int,
        protocol_version: int,
        message_type: int,
        body_type: int,
    ) -> None:
        """Initialize message request."""
        super().__init__()
        self.device_type = device_type
        self.protocol_version = protocol_version
        self.message_type = message_type
        self.body_type = body_type

    @property
    def header(self) -> bytearray:
        """Message header."""
        length = self.HEADER_LENGTH + len(self.body)
        return bytearray(
            [
                # flag
                0xAA,
                # length
                length,
                # device type
                self.device_type,
                # frame checksum
                0x00,  # self._device_type ^ length,
                # unused
                0x00,
                0x00,
                # frame ID
                0x00,
                # frame protocol version
                0x00,
                # device protocol version
                self.protocol_version,
                # frame type
                self.message_type,
            ],
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError

    @property
    def body(self) -> bytearray:
        """Message body."""
        body = bytearray([])
        if self.body_type != NONE_VALUE:
            body.append(self.body_type)
        if self._body is not None:
            body.extend(self._body)
        return body

    def serialize(self) -> bytearray:
        """Serialize message."""
        stream = self.header + self.body
        stream.append(MessageBase.checksum(stream[1:]))
        return stream


class MessageQuestCustom(MessageRequest):
    """Message quest custom."""

    def __init__(
        self,
        device_type: int,
        protocol_version: int,
        cmd_type: int,
        cmd_body: bytearray,
    ) -> None:
        """Initialize message quest custom."""
        super().__init__(
            device_type=device_type,
            protocol_version=protocol_version,
            message_type=cmd_type,
            body_type=NONE_VALUE,
        )
        self._cmd_body = cmd_body

    @property
    def _body(self) -> bytearray:
        return bytearray([])

    @property
    def body(self) -> bytearray:
        """Message body."""
        return self._cmd_body


class MessageQueryAppliance(MessageRequest):
    """Message query appliance."""

    def __init__(self, device_type: int) -> None:
        """Initialize message query appliance."""
        super().__init__(
            device_type=device_type,
            protocol_version=0,
            message_type=MessageType.query_appliance,
            body_type=NONE_VALUE,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])

    @property
    def body(self) -> bytearray:
        """Message body."""
        return bytearray([0x00] * 19)


T = TypeVar("T")
E = TypeVar("E", bound="IntEnum")


class BodyParser(Generic[T]):
    """Body parser to decode message."""

    def __init__(
        self,
        name: str,
        byte: int,
        bit: int | None = None,
        length_in_bytes: int = 1,
        first_upper: bool = True,
        default_raw_value: int = 0,
    ) -> None:
        """Init body parser with attribute name."""
        self.name = name
        self._byte = byte
        self._bit = bit
        self._length_in_bytes = length_in_bytes
        self._first_upper = first_upper
        self._default_raw_value = default_raw_value
        if length_in_bytes < 0:
            raise ValueError("Length in bytes must be a positive value.")
        if bit is not None and (bit < 0 or bit >= length_in_bytes * 8):
            raise ValueError(
                "Bit, if set, must be a valid value position for %d bytes.",
                length_in_bytes,
            )

    def _get_raw_value(self, body: bytearray) -> int:
        """Get raw value from body."""
        if len(body) < self._byte + self._length_in_bytes:
            return self._default_raw_value
        data = 0
        for i in range(self._length_in_bytes):
            byte = (
                self._byte + self._length_in_bytes - 1 - i
                if self._first_upper
                else self._byte + i
            )
            data += body[byte] << (8 * i)
        if self._bit is not None:
            data = (data & (1 << self._bit)) >> self._bit
        return data

    def get_value(self, body: bytearray) -> T:
        """Get attribute value."""
        return self._parse(self._get_raw_value(body))

    def _parse(self, raw_value: int) -> T:
        """Convert raw value to attribute value."""
        raise NotImplementedError


class BoolParser(BodyParser[bool]):
    """Bool message body parser."""

    def __init__(
        self,
        name: str,
        byte: int,
        bit: int | None = None,
        true_value: int = 1,
        false_value: int = 0,
        default_value: bool = True,
    ) -> None:
        """Init bool body parser."""
        super().__init__(name, byte, bit)
        self._true_value = true_value
        self._default_value = default_value
        self._false_value = false_value

    def _parse(self, raw_value: int) -> bool:
        if raw_value not in [self._true_value, self._false_value]:
            return self._default_value
        return raw_value == self._true_value


class IntEnumParser(BodyParser[E]):
    """IntEnum message body parser."""

    def __init__(
        self,
        name: str,
        byte: int,
        enum_class: type[E],
        length_in_bytes: int = 1,
        first_upper: bool = False,
        default_value: E | None = None,
    ) -> None:
        """Init IntEnum body parser."""
        super().__init__(
            name,
            byte,
            length_in_bytes=length_in_bytes,
            first_upper=first_upper,
        )
        self._enum_class = enum_class
        self._default_value = default_value

    def _parse(self, raw_value: int) -> E:
        try:
            return self._enum_class(raw_value)
        except ValueError:
            return (
                self._default_value
                if self._default_value is not None
                else self._enum_class(0)
            )


class IntParser(BodyParser[int]):
    """IntEnum message body parser."""

    def __init__(
        self,
        name: str,
        byte: int,
        max_value: int = 255,
        min_value: int = 0,
        length_in_bytes: int = 1,
        first_upper: bool = False,
    ) -> None:
        """Init IntEnum body parser."""
        super().__init__(
            name,
            byte,
            length_in_bytes=length_in_bytes,
            first_upper=first_upper,
        )
        self._max_value = max_value
        self._min_value = min_value

    def _parse(self, raw_value: int) -> int:
        if raw_value > self._max_value:
            return self._max_value
        if raw_value < self._min_value:
            return self._min_value
        return raw_value


class MessageBody:
    """Message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize message body."""
        self._data = body
        self.parser_list: list[BodyParser] = []

    @property
    def data(self) -> bytearray:
        """Message body data."""
        return self._data

    @property
    def body_type(self) -> int:
        """Message body type."""
        return self._data[0]

    @staticmethod
    def read_byte(body: bytearray, byte: int, default_value: int = 0) -> int:
        """Read bytes for message body."""
        return body[byte] if len(body) > byte else default_value

    def parse_all(self) -> None:
        """Process parses and set body attrs."""
        for parse in self.parser_list:
            setattr(self, parse.name, parse.get_value(self._data))


class NewProtocolPackLength(IntEnum):
    """New Protocol Pack Length."""

    FOUR = 4
    FIVE = 5


class NewProtocolMessageBody(MessageBody):
    """New protocol message body."""

    def __init__(self, body: bytearray, bt: int) -> None:
        """Initialize new protocol message body."""
        super().__init__(body)
        if bt == BodyType.B5:
            self._pack_len = NewProtocolPackLength.FOUR
        else:
            self._pack_len = NewProtocolPackLength.FIVE

    @staticmethod
    def pack(param: int, value: bytearray, pack_len: int = 4) -> bytearray:
        """Pack for new protocol."""
        length = len(value)
        if pack_len == NewProtocolPackLength.FOUR:
            stream = bytearray([param & 0xFF, param >> 8, length]) + value
        else:
            stream = bytearray([param & 0xFF, param >> 8, 0x00, length]) + value
        return stream

    def parse(self) -> dict[int, bytearray]:
        """Parse new protocol body."""
        result = {}
        try:
            pos = 2
            for _ in range(self.data[1]):
                param = self.data[pos] + (self.data[pos + 1] << 8)
                if self._pack_len == NewProtocolPackLength.FIVE:
                    pos += 1
                length = self.data[pos + 2]
                if length > 0:
                    value = self.data[pos + 3 : pos + 3 + length]
                    result[param] = value
                pos += 3 + length
        except IndexError:
            # Some device used non-standard new-protocol(美的乐享三代中央空调?)
            _LOGGER.debug("Non-standard new-protocol %s", self.data.hex())
        return result


class MessageResponse(MessageBase):
    """Message response."""

    def __init__(self, message: bytearray) -> None:
        """Initialize message response."""
        super().__init__()
        if message is None or len(message) < self.HEADER_LENGTH + 1:
            raise MessageLenError
        self._header = message[: self.HEADER_LENGTH]
        self.protocol_version = self._header[-2]
        self.message_type = self._header[-1]
        self.device_type = self._header[2]
        body = message[self.HEADER_LENGTH : -1]
        self._body = MessageBody(body)
        self.body_type = self._body.body_type

    @property
    def header(self) -> bytearray:
        """Message response header."""
        return self._header

    @property
    def body(self) -> bytearray:
        """Message response body."""
        return self._body.data

    def set_body(self, body: MessageBody) -> None:
        """Message response set body."""
        self._body = body

    def set_attr(self) -> None:
        """Message response set attribute."""
        for key in vars(self._body):
            if key != "data":
                value = getattr(self._body, key, None)
                setattr(self, key, value)


class MessageApplianceResponse(MessageResponse):
    """Message appliance response."""

    def __init__(self, message: bytearray) -> None:
        """Initialize message appliance response."""
        super().__init__(message)
