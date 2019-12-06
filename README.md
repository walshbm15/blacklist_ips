# blacklist_ips

Based on code found here: [https://github.com/open-downloads/odl/blob/master/odl/blacklist.py](https://github.com/open-downloads/odl/blob/master/odl/blacklist.py).

Another way to do the initialization and lookup with performance on par without using the `pytricia` module.

<br/>


## Run code
To call this from the command line, call the `blacklist_ips.py` file with python and pass the ip you want to check against as an argument. If it returns `True` it means it is blacklisted otherwise it will return `False`. 

See below example how to run:

	python blacklist_ips.py 3.0.0.0