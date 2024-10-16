"""Midea local message."""

import logging
import warnings
from enum import IntEnum
from typing import Any, Generic, SupportsIndex, TypeVar, cast

from deprecated import deprecated

from midealocal.const import DeviceType

_LOGGER = logging.getLogger(__name__)


class ListTypes(IntEnum):
    """Body and SubBody Types."""

    A0 = 0xA0
    A1 = 0xA1
    A2 = 0xA2
    A3 = 0xA3
    A4 = 0xA4
    A5 = 0xA5
    A6 = 0xA6
    A7 = 0xA7
    A8 = 0xA8
    A9 = 0xA9
    AA = 0xAA
    AB = 0xAB
    AC = 0xAC
    AD = 0xAD
    AE = 0xAE
    AF = 0xAF
    B0 = 0xB0
    B1 = 0xB1
    B2 = 0xB2
    B3 = 0xB3
    B4 = 0xB4
    B5 = 0xB5
    B6 = 0xB6
    B7 = 0xB7
    B8 = 0xB8
    B9 = 0xB9
    BA = 0xBA
    BB = 0xBB
    BC = 0xBC
    BD = 0xBD
    BE = 0xBE
    BF = 0xBF
    C0 = 0xC0
    C1 = 0xC1
    C2 = 0xC2
    C3 = 0xC3
    C4 = 0xC4
    C5 = 0xC5
    C6 = 0xC6
    C7 = 0xC7
    C8 = 0xC8
    C9 = 0xC9
    CA = 0xCA
    CB = 0xCB
    CC = 0xCC
    CD = 0xCD
    CE = 0xCE
    CF = 0xCF
    D0 = 0xD0
    D1 = 0xD1
    D2 = 0xD2
    D3 = 0xD3
    D4 = 0xD4
    D5 = 0xD5
    D6 = 0xD6
    D7 = 0xD7
    D8 = 0xD8
    D9 = 0xD9
    DA = 0xDA
    DB = 0xDB
    DC = 0xDC
    DD = 0xDD
    DE = 0xDE
    DF = 0xDF
    E0 = 0xE0
    E1 = 0xE1
    E2 = 0xE2
    E3 = 0xE3
    E4 = 0xE4
    E5 = 0xE5
    E6 = 0xE6
    E7 = 0xE7
    E8 = 0xE8
    E9 = 0xE9
    EA = 0xEA
    EB = 0xEB
    EC = 0xEC
    ED = 0xED
    EE = 0xEE
    EF = 0xEF
    F0 = 0xF0
    F1 = 0xF1
    F2 = 0xF2
    F3 = 0xF3
    F4 = 0xF4
    F5 = 0xF5
    F6 = 0xF6
    F7 = 0xF7
    F8 = 0xF8
    F9 = 0xF9
    FA = 0xFA
    FB = 0xFB
    FC = 0xFC
    FD = 0xFD
    FE = 0xFE
    FF = 0xFF
    X00 = 0x00
    X01 = 0x01
    X02 = 0x02
    X03 = 0x03
    X04 = 0x04
    X05 = 0x05
    X06 = 0x06
    X07 = 0x07
    X08 = 0x08
    X09 = 0x09
    X0A = 0x0A
    X0B = 0x0B
    X0C = 0x0C
    X0D = 0x0D
    X0E = 0x0E
    X0F = 0x0F
    X10 = 0x10
    X11 = 0x11
    X12 = 0x12
    X13 = 0x13
    X14 = 0x14
    X15 = 0x15
    X16 = 0x16
    X17 = 0x17
    X18 = 0x18
    X19 = 0x19
    X1A = 0x1A
    X1B = 0x1B
    X1C = 0x1C
    X1D = 0x1D
    X1E = 0x1E
    X1F = 0x1F
    X20 = 0x20
    X21 = 0x21
    X22 = 0x22
    X23 = 0x23
    X24 = 0x24
    X25 = 0x25
    X26 = 0x26
    X27 = 0x27
    X28 = 0x28
    X29 = 0x29
    X2A = 0x2A
    X2B = 0x2B
    X2C = 0x2C
    X2D = 0x2D
    X2E = 0x2E
    X2F = 0x2F
    X30 = 0x30
    X31 = 0x31
    X32 = 0x32
    X33 = 0x33
    X34 = 0x34
    X35 = 0x35
    X36 = 0x36
    X37 = 0x37
    X38 = 0x38
    X39 = 0x39
    X3A = 0x3A
    X3B = 0x3B
    X3C = 0x3C
    X3D = 0x3D
    X3E = 0x3E
    X3F = 0x3F
    X40 = 0x40
    X41 = 0x41
    X42 = 0x42
    X43 = 0x43
    X44 = 0x44
    X45 = 0x45
    X46 = 0x46
    X47 = 0x47
    X48 = 0x48
    X49 = 0x49
    X4A = 0x4A
    X4B = 0x4B
    X4C = 0x4C
    X4D = 0x4D
    X4E = 0x4E
    X4F = 0x4F
    X50 = 0x50
    X51 = 0x51
    X52 = 0x52
    X53 = 0x53
    X54 = 0x54
    X55 = 0x55
    X56 = 0x56
    X57 = 0x57
    X58 = 0x58
    X59 = 0x59
    X5A = 0x5A
    X5B = 0x5B
    X5C = 0x5C
    X5D = 0x5D
    X5E = 0x5E
    X5F = 0x5F
    X60 = 0x60
    X61 = 0x61
    X62 = 0x62
    X63 = 0x63
    X64 = 0x64
    X65 = 0x65
    X66 = 0x66
    X67 = 0x67
    X68 = 0x68
    X69 = 0x69
    X6A = 0x6A
    X6B = 0x6B
    X6C = 0x6C
    X6D = 0x6D
    X6E = 0x6E
    X6F = 0x6F
    X70 = 0x70
    X71 = 0x71
    X72 = 0x72
    X73 = 0x73
    X74 = 0x74
    X75 = 0x75
    X76 = 0x76
    X77 = 0x77
    X78 = 0x78
    X79 = 0x79
    X7A = 0x7A
    X7B = 0x7B
    X7C = 0x7C
    X7D = 0x7D
    X7E = 0x7E
    X7F = 0x7F
    X80 = 0x80
    X81 = 0x81
    X82 = 0x82
    X83 = 0x83
    X84 = 0x84
    X85 = 0x85
    X86 = 0x86
    X87 = 0x87
    X88 = 0x88
    X89 = 0x89
    X8A = 0x8A
    X8B = 0x8B
    X8C = 0x8C
    X8D = 0x8D
    X8E = 0x8E
    X8F = 0x8F
    X90 = 0x90
    X91 = 0x91
    X92 = 0x92
    X93 = 0x93
    X94 = 0x94
    X95 = 0x95
    X96 = 0x96
    X97 = 0x97
    X98 = 0x98
    X99 = 0x99
    X9A = 0x9A
    X9B = 0x9B
    X9C = 0x9C
    X9D = 0x9D
    X9E = 0x9E
    X9F = 0x9F


@deprecated("Use ListTypes instead")
class BodyType(IntEnum):
    """Body Types (Deprecated)."""

    @classmethod
    def _missing_(cls, value: Any) -> IntEnum:  # noqa: ANN401
        warnings.warn(
            "BodyType is deprecated, use ListTypes instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return ListTypes(value)


@deprecated("Use ListTypes instead")
class SubBodyType(IntEnum):
    """SubBody Types (Deprecated)."""

    @classmethod
    def _missing_(cls, value: Any) -> IntEnum:  # noqa: ANN401
        warnings.warn(
            "SubBodyType is deprecated, use ListTypes instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return ListTypes(value)


class MessageLenError(Exception):
    """Message length exception."""


class MessageBodyError(Exception):
    """Message body exception."""


class MessageCheckSumError(Exception):
    """Message checksum exception."""


class MessageType(IntEnum):
    """Message type."""

    default = (0x00,)
    set = (0x02,)
    query = (0x03,)
    notify1 = (0x04,)
    notify2 = (0x05,)
    exception = (0x06,)
    exception2 = (0x0A,)
    query_appliance = (0xA0,)

    @classmethod
    def get_key_from_value(cls, value: int) -> str:
        """Return the key corresponding to the given value."""
        for key, val in cls.__members__.items():
            if val == value:
                return key
        return "Unknown"


class MessageBase:
    """Message base."""

    HEADER_LENGTH = 10

    def __init__(self) -> None:
        """Initialize message base."""
        self._device_type: DeviceType = DeviceType.X00
        self._message_type: MessageType = MessageType.default
        self._body_type: ListTypes = ListTypes.X00
        self._message_protocol_version: int = 0

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
    def message_type(self) -> MessageType:
        """Message type."""
        return self._message_type

    @message_type.setter
    def message_type(self, value: MessageType) -> None:
        self._message_type = value

    @property
    def device_type(self) -> DeviceType:
        """Message device type."""
        return self._device_type

    @device_type.setter
    def device_type(self, value: DeviceType) -> None:
        self._device_type = value

    @property
    def body_type(self) -> ListTypes:
        """Message body type."""
        return self._body_type

    @body_type.setter
    def body_type(self, value: ListTypes) -> None:
        self._body_type = value

    @property
    def protocol_version(self) -> int:
        """Message protocol version."""
        return self._message_protocol_version

    @protocol_version.setter
    def protocol_version(self, protocol_version: int) -> None:
        self._message_protocol_version = protocol_version

    def _format_attribute(
        self,
        value: bytes | bytearray | int | str | bool | object,
    ) -> int | str | bool | object:
        """Format value as a hex string if it's bytes or bytearray.

        Args:
        ----
            value (bytes | bytearray | int | str | bool): value to be formatted.

        Returns:
        -------
            int | str | bool: The formatted result.

        """
        if isinstance(value, bytes | bytearray):
            return value.hex()
        return value

    def __str__(self) -> str:
        """Parse to string."""
        # get attributes and value
        attributes = {
            key: self._format_attribute(value) for key, value in self.__dict__.items()
        }

        # update some attributes
        attributes.update(
            {
                "header": self._format_attribute(self.header),
                "body": self._format_attribute(self.body),
                "message_type": MessageType.get_key_from_value(self.message_type),
                "body_type": (
                    f"{self._body_type:02x}" if self._body_type is not None else "None"
                ),
                "self": self,
            },
        )

        return str(attributes)


class MessageRequest(MessageBase):
    """Message request."""

    def __init__(
        self,
        device_type: DeviceType,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
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
        if self.body_type is not None:
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
        device_type: DeviceType,
        protocol_version: int,
        cmd_type: MessageType,
        cmd_body: bytearray,
    ) -> None:
        """Initialize message quest custom."""
        super().__init__(
            device_type=device_type,
            protocol_version=protocol_version,
            message_type=cmd_type,
            body_type=ListTypes.X00,
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

    def __init__(self, device_type: DeviceType) -> None:
        """Initialize message query appliance."""
        super().__init__(
            device_type=device_type,
            protocol_version=0,
            message_type=MessageType.query_appliance,
            body_type=ListTypes.X00,
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
    def body_type(self) -> ListTypes:
        """Message body type."""
        return ListTypes(self._data[0])

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
        if bt == ListTypes.B5:
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
        self.message_type = MessageType(self._header[-1])
        self.device_type = DeviceType(self._header[2])
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
