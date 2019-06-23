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
        regexes = {"numbers": '(?P<number>[0-9]+: )',
                   "interfaces": '(?P<interface>[0-9a-zA-Z-@]+: )',
                   "flags": '(?P<flags><(.*?)>)',
                   "mtu": '(?: mtu )(?P<mtu>[0-9]+)'}

        all_pattern = re.compile(str().join(regexes.values()))

        interfaces = dict()
        for find in re.finditer(all_pattern, output):
            number = int(Address._remove_colon(find.group('number')))
            name = Address._remove_colon(find.group('interface'))
            flags = Address._remove_angle_brackets(find.group('flags')).split(",")
            mtu = find.group('mtu')
            interfaces[number] = {"name": name,
                                  "flags": flags,
                                  "mtu": mtu}

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
