import re
from typing import Dict, List

from ip_command import run


class Address:

    @staticmethod
    def show() -> Dict:
        output = run('addr').stdout.decode()
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

        all_pattern = re.compile(str().join(regexes.values()))

        interfaces = dict()
        for find in re.finditer(all_pattern, output):
            interfaces[int(find.group('number'))] = \
                {
                    "name": find.group('name'),
                    "flags": find.group('flags').split(","),
                    "mtu": int(find.group('mtu')),
                    "qdisc": find.group('qdisc'),
                    "state": find.group('state'),
                    "group": find.group('group'),
                    "qlen": int(find.group('qlen')),
                    "link":
                        {
                            "type": find.group('link_type'),
                            "mac_address":  find.group('link_mac_address'),
                            "mac_broadcast": find.group('link_mac_broadcast')
                        },
                    "addresses": Address._parse_addresses(find.group('addresses'))
                 }

        return interfaces

    @staticmethod
    def _parse_addresses(address_definitions: str) -> List[Dict]:
        regexes = {
            "address_family": r'\s+(?P<address_family>((\binet\b)|(\binet6\b)))\s+',
            "ip_address": r'(?P<ipv6>(([0-9a-f]{0,4}:+){0,8}([0-9a-f]{0,4})/[0-9]{0,3}))|'  # IPv6
                          r'(?P<ipv4_address>((([0-9]{1,3}\.){3}[0-9]{0,3}/[0-9]{2}))) '    # IPv4
                          r'(?:brd\s+)(?P<ipv4_broadcast>((([0-9]{1,3}\.){3}[0-9]{0,3})))'        # IPv4 broadcast
        }

        all_pattern = re.compile(str().join(regexes.values()))

        addresses = list()
        for find in re.finditer(all_pattern, address_definitions):
            address = {
                "address_family": find.group('address_family'),
            }
            if find.group('ipv6'):
                address['ip_address'] = find.group('ipv6')
            elif find.group('ipv4_address'):
                address['ip_address'] = find.group('ipv4_address')
                address['broadcast'] = find.group('ipv4_broadcast')
            addresses.append(address)
        return addresses