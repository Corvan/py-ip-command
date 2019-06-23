py-ip-command
======
Wrapping the Linux `ip` command in Python.

Note
-----
This is still work in progess, but you can already use it. Help is very welcome!

Usage
-----
At the moment only two commands of `ip` are implemented.

Just use 
```python
from ip_command.ip import IP
 ```
and then you can issue commands like 
 ```bash
 ip addr show
 ``` 
 with
 ```python
IP.addr().show()
```
or 
```bash 
ip neigh show
```
with
```python
IP.neigh().show()
```
The return of both is a dict (addr) or a list (neigh) consisting of all the information the commands return but split 
into single elements. 