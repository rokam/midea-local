"""Midea local constants."""

from enum import IntEnum

MAX_BYTE_VALUE = 0xFF
MAX_DOUBLE_BYTE_VALUE = 0xFFFF


class DeviceType(IntEnum):
    """Device Type."""

    A0 = 0xA0
    A1 = 0xA1
    AC = 0xAC
    B0 = 0xB0
    B1 = 0xB1
    B3 = 0xB3
    B4 = 0xB4
    B6 = 0xB6
    B8 = 0xB8
    BF = 0xBF
    C2 = 0xC2
    C3 = 0xC3
    CA = 0xCA
    CC = 0xCC
    CD = 0xCD
    CE = 0xCE
    CF = 0xCF
    DA = 0xDA
    DB = 0xDB
    DC = 0xDC
    E1 = 0xE1
    E2 = 0xE2
    E3 = 0xE3
    E6 = 0xE6
    E8 = 0xE8
    EA = 0xEA
    EC = 0xEC
    ED = 0xED
    FA = 0xFA
    FB = 0xFB
    FC = 0xFC
    FD = 0xFD
    X13 = 0x13
    X26 = 0x26
    X34 = 0x34
    X40 = 0x40
    X00 = 0x00


class ProtocolVersion(IntEnum):
    """Protocol version."""

    V1 = 1
    V2 = 2
    V3 = 3
