from __future__ import annotations
import ipaddress
from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class Interface:
    """
    A network interface
    """

    number: int
    name: str
    flags: List[str]
    mtu: int
    qdisc: str
    state: str
    group: str
    qlen: str
    link: Link
    addresses: List[Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]]


@dataclass
class Link:
    """
    An :Interface:'s physical link
    """
    type: str
    mac_address: str
    mac_broadcast: str


@dataclass
class Neighbour:
    """
    A network neighbour
    """
    address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
    status: str
    device: str
    mac_address: str = field(default="")
