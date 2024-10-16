"""Midea local message test."""

import pytest

from midealocal.message import (
    BodyParser,
    BoolParser,
    IntEnumParser,
    IntParser,
    ListTypes,
    MessageBody,
)


def test_init_validations() -> None:
    """Test body parser init validations."""
    with pytest.raises(
        ValueError,
        match="Length in bytes must be a positive value.",
    ):
        BodyParser[int]("name", byte=3, length_in_bytes=-1)

    with pytest.raises(
        ValueError,
        match="('Bit, if set, must be a valid value position for %d bytes.', 2)",
    ):
        BodyParser[int]("name", byte=3, length_in_bytes=2, bit=-1)

    with pytest.raises(
        ValueError,
        match="('Bit, if set, must be a valid value position for %d bytes.', 3)",
    ):
        BodyParser[int]("name", byte=3, length_in_bytes=3, bit=24)


class TestBodyParser:
    """Body parser test."""

    @pytest.fixture(autouse=True)
    def _setup_body(self) -> None:
        """Create body for test."""
        self.body = bytearray(
            [
                0x00,
                0x01,
                0x02,
                0x03,
                0x04,
                0x05,
            ],
        )

    def test_get_raw_value_1_byte(self) -> None:
        """Test get raw value with 1 byte."""
        parser = BodyParser[int]("name", 2)
        value = parser._get_raw_value(self.body)
        assert value == 0x02

    def test_get_raw_value_2_bytes(self) -> None:
        """Test get raw value with 2 bytes."""
        parser = BodyParser[int]("name", 2, length_in_bytes=2)
        value = parser._get_raw_value(self.body)
        assert value == 0x0203

    def test_get_raw_value_2_bytes_first_lower(self) -> None:
        """Test get raw value with 2 bytes first lower."""
        parser = BodyParser[int]("name", 2, length_in_bytes=2, first_upper=False)
        value = parser._get_raw_value(self.body)
        assert value == 0x0302

    def test_get_raw_out_of_bounds(self) -> None:
        """Test get raw value out of bounds."""
        parser = BodyParser[int]("name", 6)
        value = parser._get_raw_value(self.body)
        assert value == 0

    def test_get_raw_data_size_out_of_bounds(self) -> None:
        """Test get raw value out of bounds."""
        parser = BodyParser[int]("name", 5, length_in_bytes=2)
        value = parser._get_raw_value(self.body)
        assert value == 0

    def test_get_raw_data_bit(self) -> None:
        """Test get raw value out of bounds."""
        for i in range(16):
            parser = BodyParser[int]("name", 4, length_in_bytes=2, bit=i)
            value = parser._get_raw_value(self.body)
            assert value == (1 if i in [0, 2, 10] else 0)

    def test_parse_unimplemented(self) -> None:
        """Test parse unimplemented."""
        parser = BodyParser[int]("name", 4, length_in_bytes=2, bit=2)
        with pytest.raises(NotImplementedError):
            parser.get_value(self.body)


class TestBoolParser:
    """Test BoolParser."""

    def test_bool_default(self) -> None:
        """Test default behaviour."""
        parser = BoolParser("name", 0)
        assert parser._parse(0) is False
        assert parser._parse(1) is True
        assert parser._parse(2) is True

    def test_bool_default_false(self) -> None:
        """Test default behaviour with default value false."""
        parser = BoolParser("name", 0, default_value=False)
        assert parser._parse(0) is False
        assert parser._parse(1) is True
        assert parser._parse(2) is False

    def test_bool_inverted(self) -> None:
        """Test True=0 and False=1."""
        parser = BoolParser("name", 0, true_value=0, false_value=1)
        assert parser._parse(0) is True
        assert parser._parse(1) is False
        assert parser._parse(2) is True


class TestIntEnumParser:
    """Test IntEnumParser."""

    def test_intenum_default(self) -> None:
        """Test default behaviour."""
        parser = IntEnumParser[ListTypes]("name", 0, ListTypes)
        assert parser._parse(0x01) == ListTypes.X01
        assert parser._parse(0x00) == ListTypes.X00
        assert parser._parse(0x10) == ListTypes.X10

        parser = IntEnumParser[ListTypes](
            "name",
            0,
            ListTypes,
            default_value=ListTypes.A0,
        )
        assert parser._parse(0x01) == ListTypes.X01
        assert parser._parse(0x00) == ListTypes.X00
        assert parser._parse(0xA0) == ListTypes.A0


class TestIntParser:
    """Test IntParser."""

    def test_int_default(self) -> None:
        """Test default behaviour."""
        parser = IntParser("name", 0)
        for i in range(-10, 260):
            if i < 0:
                assert parser._parse(i) == 0
            elif i > 255:
                assert parser._parse(i) == 255
            else:
                assert parser._parse(i) == i


class TestMessageBody:
    """Test message body."""

    def test_parse_all(self) -> None:
        """Test parse all."""
        data = bytearray(
            [
                0x00,
                0x01,
                0x02,
                0x03,
                0x04,
                0x05,
            ],
        )

        body = MessageBody(data)
        body.parser_list.extend(
            [
                IntEnumParser("bt", 0, ListTypes),
                BoolParser("power", 1),
                BoolParser("feature_1", 2, 0),
                BoolParser("feature_2", 2, 1),
                IntParser("speed", 3),
            ],
        )
        body.parse_all()
        assert hasattr(body, "bt") is True
        assert getattr(body, "bt", None) == ListTypes.X00
        assert hasattr(body, "power") is True
        assert getattr(body, "power", False) is True
        assert hasattr(body, "feature_1") is True
        assert getattr(body, "feature_1", True) is False
        assert hasattr(body, "feature_2") is True
        assert getattr(body, "feature_2", False) is True
        assert hasattr(body, "speed") is True
        assert getattr(body, "speed", 0) == 3
