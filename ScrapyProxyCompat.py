import logging
import subprocess
from threading import Thread
from time import sleep

# A Python Module to Wrap PPython for use with Scrapy
class ScrapyProxyController:
    _proxyThreads = []
    _proxyAddresses = []
    _started = False

    # Initialize Class Variables
    def __init__(self, retry_time:float=300.0, retry_count: int=5, proxies:list=[], starting_port:int=2000):
        self.proxies = proxies
        self.retry_time = retry_time
        self.retry_count = retry_count
        self.starting_port = starting_port

    # Thread to handle a single proxy instance
    class ProxyThread(Thread):
        def __init__(
            self,
            proxy,
            localport,
            retry_time: float,
            retry_count: int,
            group=None,
            target=None,
            name=None,
            args=(),
            kwargs=None,
        ):
            super().__init__(group=group, target=target, name=name)
            self.args = args
            self.kwargs = kwargs
            self.proxy = proxy
            self.localport = localport
            self.retry_time = retry_time
            self.retry_count = retry_count

        def run(self):
            # Track number of retries
            i = 0

            # Get proxy string without creds for logging purposes
            proxyNoCreds = self.proxy.split("#")[0]

            # Loop for number of retries
            while i <= self.retry_count:
                i += 1

                logging.debug(
                    "PProxy starting for " + proxyNoCreds + " on try " + str(i) + "."
                )

                # Start a subprocess running the proxy
                ret = subprocess.run(
                    "pproxy -l http://:"
                    + str(self.localport)
                    + ' -r "'
                    + self.proxy
                    + '"',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    shell=True,
                )

                # This code will only be reached if the subprocess exits
                # Check if this is the last retry
                if i == self.retry_count + 1:
                    logging.warning(
                        "PProxy has exited for the final time for "
                        + proxyNoCreds
                        + " with status code "
                        + str(ret.returncode)
                        + ". Program output as follows:\n"
                        + ret.stdout
                    )
                else:
                    logging.warning(
                        "PProxy has exited for "
                        + proxyNoCreds
                        + " with status code "
                        + str(ret.returncode)
                        + ". Retrying in "
                        + str(self.retry_time)
                        + " seconds. Program output as follows:\n"
                        + ret.stdout
                    )
                    sleep(self.retry_time)

    # Starts the Proxies Provided in the Constructor
    def startProxies(self):
        for i, proxy in enumerate(self.proxies):
            self._proxyThreads.append(
                self.ProxyThread(
                    proxy=proxy,
                    localport=self.starting_port + i,
                    retry_time=self.retry_time,
                    retry_count=self.retry_count,
                )
            )
            self._proxyAddresses.append("http://127.0.0.1:" + str(self.starting_port + 1))
            self._proxyThreads[i].start()

    # Can be Used to Read Proxies to Connect PProxy to if 
    def readProxies(self, filePath):
        if self._started:
            raise Exception("Proxies already started!")

        proxyFile = open(filePath, "r")

        # Loop for each proxy in provided file
        for line in proxyFile:
            # Skip line if it's a comment
            if line[0] == "#" or line == "":
                continue

            self.proxies.append(line.strip())

        proxyFile.close()

    # Used to write Local Proxies to the Scrapy Proxy File
    def writeProxies(self, filePath):
        if not self._started:
            raise Exception("Proxies not yet started!")

        proxyFile = open(filePath, "w")

        for proxy in self._proxyAddresses:
            if proxy.split(":")[-1] == self.starting_port:
                proxyFile.write(proxy)
            else:
                proxyFile.write("\n" + proxy)

        proxyFile.close()

    # Used to get a list of Proxy Threads
    def getProxies(self):
        if not self._started:
            raise Exception("Proxies not yet started!")

        return self._proxyThreads

    # Used to get a list of Local Proxy Addresses.
    # Can be used as a way to self handle connecting proxies to Scrapy.
    def getProxyAddresses(self):
        if not self._started:
            raise Exception("Proxies not yet started!")

        return self._proxyAddresses
