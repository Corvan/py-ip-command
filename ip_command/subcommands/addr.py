from __future__ import annotations

import dataclasses
import ipaddress
import re
from dataclasses import dataclass
from typing import Dict, List, Pattern, Union


class Address:
    regexes = {"number": r'(?P<number>[0-9]+):\s+',
               "name": r'(?P<name>[0-9a-zA-Z-@]+):\s+',
               "flags": r'(?:<)(?P<flags>(.*?))(?:>)\s+',
               "mtu": r'(?:mtu\s)(?P<mtu>[0-9]+)\s+',
               "qdisc": r'(?:qdisc\s)(?P<qdisc>[a-z]+)\s+',
               "state": r'(?:state\s)(?P<state>[A-Z]+)\s+',
               "group": r'(?:group\s)(?P<group>[a-z]+)\s+',
               "qlen": r'(?:qlen\s)(?P<qlen>[0-9]+)\s+',
               "link_type": r'(?:link/)(?P<link_type>[a-z]+)\s+',
               "link_mac_address": r'(?P<link_mac_address>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))\s+',
               "link_mac_broadcast":
                   r'(?:brd\s)(?P<link_mac_broadcast>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))\s{1}',
               "addresses": r'(?P<addresses>(\s+inet.*\n.*\n)*)'}
    all_pattern: Pattern = re.compile(str().join(regexes.values()))

    @staticmethod
    def show(as_dict: bool = False) -> Union[List[Interface], Dict]:
        from ip_command.ip import run
        output = run(['addr', 'show']).stdout.decode()

        interfaces: List[Interface] = list()
        for find in re.finditer(Address.all_pattern, output):
            interfaces.append(Interface(number=int(find.group('number')),
                                        name=find.group('name'),
                                        flags=find.group('flags').split(','),
                                        mtu=int(find.group('mtu')),
                                        qdisc=find.group('qdisc'),
                                        state=find.group('state'),
                                        group=find.group('group'),
                                        qlen=find.group('qlen'),
                                        link=Link(type=find.group('link_type'),
                                                  mac_address=find.group('link_mac_address'),
                                                  mac_broadcast=find.group('link_mac_broadcast')),
                                        addresses=Address._parse_addresses(find.group('addresses'), as_dict)))
        if as_dict:
            return {interface.number: dataclasses.asdict(interface) for interface in interfaces}

        return interfaces

    @staticmethod
    def _parse_addresses(address_definitions: str, as_dict: bool) -> Union[List[Dict], List[IpAddress]]:
        regexes = {
            "address_family": r'\s+(?P<address_family>((\binet\b)|(\binet6\b)))\s+',
            "ip_address": r'(?P<ip>(([0-9a-f]{0,4}:+){0,8}([0-9a-f]{0,4})/[0-9]{0,3})|'  # IPv6
                          r'([0-9]{1,3}\.){3}[0-9]{0,3}/[0-9]{2})\s+'            # IPv4
        }

        all_pattern = re.compile(str().join(regexes.values()))

        addresses = list()
        for find in re.finditer(all_pattern, address_definitions):

            address = IpAddress(family=find.group('address_family'),
                                address=ipaddress.ip_interface(find.group('ip')))

            addresses.append(address)
        if as_dict:
            return [dataclasses.asdict(address) for address in addresses]
        return addresses


@dataclass
class Interface:

    number: int
    name: str
    flags: List[str]
    mtu: int
    qdisc: str
    state: str
    group: str
    qlen: str
    link: Link
    addresses: List[IpAddress]


@dataclass
class Link:

    type: str
    mac_address: str
    mac_broadcast: str


@dataclass
class IpAddress:

    family: str
    address: Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]
