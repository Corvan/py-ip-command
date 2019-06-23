from __future__ import annotations
import re
import subprocess
from typing import Dict


class IP:

    @staticmethod
    def addr() -> Address:
        return Address()

    @staticmethod
    def run(command: str) -> subprocess.CompletedProcess:
        ip_path = subprocess.run(['which', 'ip'], capture_output=True).stdout.decode().strip()
        return subprocess.run([ip_path, command], capture_output=True)


class Address:

    @staticmethod
    def show() -> Dict:
        output = IP.run('addr').stdout.decode()
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
                       r'(?:brd\s)(?P<link_mac_broadcast>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))\s{1}'}

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
                        }
                 }

        return interfaces

    @staticmethod
    def _remove_colon(text: str) -> str:
        return Address._remove(":", text)

    @staticmethod
    def _remove_angle_brackets(text: str) -> str:
        text = Address._remove("<", text)
        return Address._remove(">", text)

    @staticmethod
    def _remove(character: str, text: str) -> str:
        return re.sub(character, "", text)


if __name__ == '__main__':
    print(IP
          .addr()
          .show())
