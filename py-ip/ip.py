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
        regexes = {"number": r'(?P<number>[0-9]+): ',
                   "name": r'(?P<name>[0-9a-zA-Z-@]+): ',
                   "flags": r'(?:<)(?P<flags>(.*?))(?:>) ',
                   "mtu": r'(?:mtu )(?P<mtu>[0-9]+) ',
                   "qdisc": r'(?:qdisc )(?P<qdisc>[a-z]+) ',
                   "state": r'(?:state )(?P<state>[A-Z]+) ',
                   "group": r'(?:group )(?P<group>[a-z]+) ',
                   "qlen": r'(?:qlen )(?P<qlen>[0-9]+)\n',
                   "link_type": r'\s+(?:link/)(?P<link_type>[a-z]+) ',
                   "link_mac_address": r'(?P<link_mac_address>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))'}

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
                            "mac_address":  find.group('link_mac_address')
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
