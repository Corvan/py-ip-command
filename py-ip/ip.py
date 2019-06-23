import re
import subprocess
from typing import Dict


class IP:

    @staticmethod
    def addr() -> Dict:
        output = IP.run('addr').stdout.decode()
        regexes = {"numbers": '(?P<number>[0-9]+: )',
                   "interfaces": '(?P<interface>[0-9a-zA-Z-@]+: )',
                   "flags": '(?P<flags><(.*?)>)'}

        all_pattern = re.compile(f"{regexes['numbers']}"
                                 f"{regexes['interfaces']}"
                                 f"{regexes['flags']}")

        interfaces = dict()
        for find in re.finditer(all_pattern, output):
            number = int(IP._remove_colon(find.group('number')))
            name = IP._remove_colon(find.group('interface'))
            flags = IP._remove_angle_brackets(find.group('flags')).split(",")
            interfaces[number] = {"name": name,
                                  "flags": flags}

        return interfaces

    @staticmethod
    def run(command: str) -> subprocess.CompletedProcess:
        ip_path = subprocess.run(['which', 'ip'], capture_output=True).stdout.decode().strip()
        return subprocess.run([ip_path, command], capture_output=True)

    @staticmethod
    def _remove_colon(text: str) -> str:
        return IP._remove(":", text)

    @staticmethod
    def _remove_angle_brackets(text: str) -> str:
        text = IP._remove("<", text)
        return IP._remove(">", text)

    @staticmethod
    def _remove(character: str, text: str) -> str:
        return re.sub(character, "", text)


if __name__ == '__main__':
    print(IP.addr())
