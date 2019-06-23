from __future__ import annotations
import subprocess

from ip_command.subcommands import Address, Neighbour


def run(command: str) -> subprocess.CompletedProcess:
    try:
        ip_path = subprocess.run(['which', 'ip'], capture_output=True).stdout.decode().strip()
        return subprocess.run([ip_path, command], capture_output=True)
    except subprocess.SubprocessError as e:
        print(e)
        exit(0)


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
