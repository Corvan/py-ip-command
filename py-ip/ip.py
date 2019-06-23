import re
import subprocess
from typing import Dict


def ip():
    return IP()


class IP:

    def addr(self) -> Dict:
        output = IP.run('addr').stdout.decode()
        regexes = {"numbers": '(?P<number>[0-9]+: )',
                   "interfaces": '(?P<interface>[0-9a-zA-Z-@]+: )',
                   "flags": '(?P<flags><(.*?)>)'}

        all_pattern = re.compile(f"{regexes['numbers']}"
                                 f"{regexes['interfaces']}"
                                 f"{regexes['flags']}")

        interfaces = {int(self._remove_colon(i[0])): {"name": self._remove_colon(i[1]),
                                                      "flags": self._remove_angle_brackets(i[2])}
                      for i in re.findall(all_pattern, output)}

        definition = re.split(all_pattern, output)
        definition.pop()
        for interface_number in interfaces:
            definition.pop()
            definition.pop()
            interfaces[interface_number]['definition'] = definition.pop()

        pass

    @staticmethod
    def run(command: str) -> subprocess.CompletedProcess:
        ip_path = subprocess.run(['which', 'ip'], capture_output=True).stdout.decode().strip()
        return subprocess.run([ip_path, command], capture_output=True)

    def _remove_colon(self, text: str) -> str:
        return self._remove(":", text)

    def _remove_angle_brackets(self, text: str) -> str:
        text = self._remove("<", text)
        return self._remove(">", text)

    def _remove(self, character: str, text: str) -> str:
        return re.sub(character, "", text)

class Address:

    def __init__(self):
        self.number: int


    def __str__(self):
        pass


if __name__ == '__main__':
    ip().addr()
