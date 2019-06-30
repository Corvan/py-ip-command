from __future__ import annotations

import dataclasses
import ipaddress
import re
from typing import Dict, List, Pattern, Union

from ip_command.model import Interface, Link


class Addr:
    _regexes = {"number": r'(?P<number>[0-9]+):\s+',
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
    _all_pattern: Pattern = re.compile(str().join(_regexes.values()))

    @staticmethod
    def show(as_dict: bool = False) -> Union[List[Interface], Dict]:
        """
        calls `ip addr show`
        :param as_dict: return a dictionary of data elements instead of an object-oriented representation
        :type as_dict: builtins.bool
        :rtype Union[List[Interface], Dict]:
        """
        from ip_command.ip import run
        output = run(['addr', 'show']).stdout.decode()

        interfaces: List[Interface] = list()
        for find in re.finditer(Addr._all_pattern, output):
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
                                        addresses=Addr._parse_addresses(find.group('addresses'))))
        if as_dict:
            return {interface.number: dataclasses.asdict(interface) for interface in interfaces}

        return interfaces

    @staticmethod
    def _parse_addresses(address_definitions: str) -> List[Union[ipaddress.IPv4Interface, ipaddress.IPv6Interface]]:
        regexes = {
            "address_family": r'\s+(?P<address_family>((\binet\b)|(\binet6\b)))\s+',
            "ip_address": r'(?P<ip>(([0-9a-f]{0,4}:+){0,8}([0-9a-f]{0,4})/[0-9]{0,3})|'  # IPv6
                          r'([0-9]{1,3}\.){3}[0-9]{0,3}/[0-9]{2})\s+'                    # IPv4
        }

        all_pattern = re.compile(str().join(regexes.values()))

        addresses = list()
        for find in re.finditer(all_pattern, address_definitions):
            addresses.append(ipaddress.ip_interface(find.group('ip')))
        return addresses


