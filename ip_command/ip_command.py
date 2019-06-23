from __future__ import annotations
import subprocess
from .subcommands import Address
from .subcommands import Neighbour


def run(command: str) -> subprocess.CompletedProcess:
    ip_path = subprocess.run(['which', 'ip'], capture_output=True).stdout.decode().strip()
    return subprocess.run([ip_path, command], capture_output=True)


class IP:

    @staticmethod
    def addr() -> Address:
        return Address()

    @staticmethod
    def neigh() -> Neighbour:
        return Neighbour()


if __name__ == '__main__':
    print(IP
          .addr()
          .show())
