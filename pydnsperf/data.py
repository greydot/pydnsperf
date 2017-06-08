import ipaddress
import logging
from random import randint

from dnstypes import *


class SourceNetworks(object):
    """Stores or generates network addresses and allows iteration over them."""
    def __init__(self, filename=None):
        self.rand_networks = True

        if filename is not None:
            f = open(filename)
            lines = f.readlines()
            f.close()

            self.networks = []
            self.rand_networks = True
            for line in lines:
                try:
                    net = ipaddress.ip_network(unicode(line.strip()))
                    self.networks.append(net)
                except:
                    logging.info("Unable to parse network address: {0}".format(line))

            if len(self.networks) > 0:
                self.rand_networks = False
            else:
                self.rand_networks = True
                logging.info("No valid network addresses read.\
                              Reverting to random source IPs.")

    def __iter__(self):
        if not self.rand_networks:
            self.index = 0
        return self

    def next(self):
        if self.rand_networks:
            min_ip = 1 << 23      # 1.0.0.0
            max_ip = 2 ** 32 - 1  # 255.255.255.254
            ip = ipaddress.ip_address(randint(min_ip, max_ip))
            mask = randint(8, 28)

            addr = unicode(str(ip) + '/' + str(mask))

            iface = ipaddress.IPv4Interface(addr)
            return iface.network
        elif self.index < len(self.networks):
            n = self.networks[self.index]
            self.index = self.index + 1
            return n
        else:
            raise StopIteration()


class QueryData(object):
    """QueryData class represents domain/type pair"""
    def __init__(self, dom, typ=A()):
        self.domain = dom
        self.type = typ

    def __str__(self):
        return (self.domain + ' ' + str(self.type))

    @staticmethod
    def parse(str):
        n = 2
        chunks = str.split()
        chunks += [None] * (n - len(chunks))

        dom, typ = chunks

        if typ is None:
            return QueryData(dom)
        else:
            return QueryData(dom, typ=parse_query_type(typ))


class ParseError(Exception):
    def __init__(self, str):
        self.message = str

    def __str__(self):
        return ('Parse error: ' + self.message)


class QueryStorage(object):
    """Stores QueryData objects"""
    def __init__(self, filename):
        self.queries = []
        for line in open(filename):
            try:
                q = QueryData.parse(line)
                self.queries.append(q)
            except:
                logging.info("Failed to parse dns query data ({0})".format(line))

        if len(self.queries) == 0:
            raise ParseError("unable to parse query data")

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        if self.index < len(self.queries):
            q = self.queries[self.index]
            self.index += 1
            return q
        else:
            raise StopIteration()
