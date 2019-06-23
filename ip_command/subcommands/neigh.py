import re
from typing import Dict, List


class Neighbour:

    @staticmethod
    def show() -> List[Dict]:
        from ip_command.ip import run
        output = run(['neigh', 'show']).stdout.decode().splitlines()
        regexes = {
            "ip_address": r'(?P<ipv4_address>(([0-9a-f]{0,4}:+){0,8}([0-9a-f]{0,4}))|'  # IPv6
                          r'(?P<ipv6_address>(([0-9]{1,3}\.){3}[0-9]{0,3})))\s+',  # IPv4
            "device": r'(?:dev\s+)(?P<device>[a-z0-9-]*)\s+',
            "lladr": r'((?:lladdr\s+)(?P<lladdr>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))\s+)?',
            "status": r'(?P<status>[A-Z]*)'

        }

        all_pattern = re.compile(str().join(regexes.values()))
        neighbours = list()
        for line in output:

            find = re.search(all_pattern, line)
            neighbour = {
                "address": find.group('ipv4_address') if find.group('ipv4_address') else find.group('ipv6_address'),
                "device": find.group('device')
            }
            if find.group('lladdr'):
                neighbour['lladdr'] = find.group('lladdr')
            neighbour['status'] = find.group('status')
            neighbours.append(neighbour)
        return neighbours
