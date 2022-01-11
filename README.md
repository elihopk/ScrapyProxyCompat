# ScrapyProxyCompat

## Introduction
ScrapyProxyCompat is a Python module that wraps [pproxy](https://pypi.org/project/pproxy/) to allow a greater range of proxy types to be used with [Scrapy](https://scrapy.org/). It supports any type of remote connection that is supported by pproxy. This module should be used with a rotating proxy middleware such as [scrapy-rotating-proxy](https://github.com/TeamHG-Memex/scrapy-rotating-proxies). ScrapyProxyCompat should be started before Scrapy and should be allowed to run in the background while Scrapy is crawling. The middleware that you write or choose to use must accept a file input made up of one proxy server per line if you would like to use the `writeProxies(filePath)` method.
For example:
```
http://127.0.0.1:2000
http://127.0.0.1:2001
http://127.0.0.1:2002
```

## Installation
To install ScrapyProxyCompat run `pip install ScrapyProxyCompat`
    
## Usage
To begin using ScrapyProxyCompat, create an instance of the `ScrapyProxyController` class.
```
from ScrapyProxyCompat.ScrapyProxyCompat import ScrapyProxyController

# Usage: ScrapyProxyController(retry_time:float=300.0, retry_count: int=5, proxies:list=[], starting_port:int=2000)
# Where:
# retry_time is optional, the amount of time in seconds to wait before retrying a pproxy connection that has exited
# retry_count is optional, the number of times to retry establishing a pproxy connection before allowing the Thread to die
# proxies is an optional list of proxies following the normal PProxy syntax: [http, socks, ss, ssl, secure (Or a combination of these)]://ip_address:port#username:password
# starting_port is an optional valid port number to be used as the starting local port. You should expect it to use this port +1 for each proxy
controller = ScrapyProxyController(500.0, 10, ["http+ssl://proxyip.com:2323#Good:Creds", "socks5://proxyip.com:2323#Good:Creds"], 3000)
```
If you provided a proxy list when creating the `ScrapyProxyController`, you can now start your proxies.
```
controller.startProxies()
```
If you did not provide a proxy list when creating the `ScrapyProxyController`, you must read your proxies from a text file made up of one proxy server per line. This function may also be used to overwrite the passed proxies before the proxies have been started.
```
# Usage: ScrapyProxyController.readProxies(filePath)
# Where:
# filePath is the String path to the file you want to read
controller.readProxies("/path/to/remote/proxies/file.txt")
```
Once you have started your proxies, you can get a list of all proxy Threads with `getProxies()` or get a list of all local proxy addresses with `getProxyAddresses()`.
You can also write the proxies to a file. Typically this will be a Scrapy proxy file.
```
# Usage: ScrapyProxyController.writeProxies(filePath)
# Where:
# filePath is the String path to the file you want to write
controller.writeProxies("/path/to/scrapy/proxies/file.txt")
```
