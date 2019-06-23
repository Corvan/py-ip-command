from __future__ import annotations
import subprocess
from typing import Iterable

from ip_command.subcommands import Address, Neighbour


def run(command: Iterable[str]) -> subprocess.CompletedProcess:
    try:
        subprocess_result = subprocess.run(['which', 'ip'], capture_output=True)
        if subprocess_result.returncode == 1:
            print("ip command not found")
            exit(1)
        ip_path = subprocess_result.stdout.decode().strip()
        argv = list([ip_path])
        argv.extend(command)
        return subprocess.run(argv, capture_output=True)
    except subprocess.SubprocessError as e:
        print(e)
        exit(1)


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
    print(IP.neigh().show())
