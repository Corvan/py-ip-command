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
IP.addr.show()
```
or 
```bash 
ip neigh show
```
with
```python
IP.neigh.show()
```
The return of both is 
* An object oriented representation of the data reurned by both commands
* a dict (addr) or a list of dicts (neigh) consisting of all the information the commands return but split 
into single elements, if you pass `as_dict=True` to `show()` or simply call `show(True)`
