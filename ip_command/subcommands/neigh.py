from __future__ import annotations
import dataclasses
import re
import ipaddress
from typing import Dict, List, Union

from ip_command.model import Neighbour


class Neigh:

    _regexes = {
        "ip_address": r'(?P<ip>([0-9a-f]{0,4}:+){0,8}([0-9a-f]{0,4})|([0-9]{1,3}\.){3}[0-9]{0,3})\s+',
        "device": r'(?:dev\s+)(?P<device>[a-z0-9-]*)\s+',
        "lladr": r'((?:lladdr\s+)(?P<lladdr>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))\s+)?',
        "status": r'(?P<status>[A-Z]*)'
    }
    _all_pattern = re.compile(str().join(_regexes.values()))

    @staticmethod
    def show(as_dict: bool = False) -> Union[List[Dict], List[Neighbour]]:
        from ip_command.ip import run
        output = run(['neigh', 'show']).stdout.decode()

        neighbours = list()
        for find in re.finditer(Neigh._all_pattern, output):

            neighbour = Neighbour(
                address=ipaddress.ip_address(find.group('ip')),
                device=find.group('device'),
                status=find.group('status')
            )
            if find.group('lladdr'):
                neighbour.mac_address = find.group('lladdr')

            neighbours.append(neighbour)

        if as_dict:
            return [dataclasses.asdict(neighbour) for neighbour in neighbours]
        return neighbours


