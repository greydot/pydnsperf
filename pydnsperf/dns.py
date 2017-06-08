import logging
from data import *
from options import get_options
from dnstypes import *
from scapy.all import IP, UDP, DNS, DNSQR, send
from itertools import cycle,izip
from random import randint
import threading
from time import sleep


def parse_query_params(str):
    n = 2
    chunks = str.split()
    chunks += [None] * (n - len(chunks))

    dom, typ = chunks

    if typ is None:
        return QueryParams(dom)
    else:
        return QueryParams(dom, typ=parse_query_type(typ))


def read_query_params_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()

    return [parse_query_params(line) for line in lines]


def prep_query(params, dst, src):
    opts = get_options()
    res = None
    typ = 'A'
    if src is not None and opts.spoof_ips:
        res = IP(dst=dst,
                 src=src)
    else:
        res = IP(dst=dst)
    if isinstance(params.type, A):
        typ = 'A'
    elif isinstance(params.type, AAAA):
        typ = 'AAAA'
    elif isinstance(params.type, MX):
        typ = 'MX'
    res = res / UDP() / DNS(rd=1, qd=DNSQR(qname=str(params.domain), qtype=typ))

    return res


def send_query(q):
    logging.debug("Sending query {0} from {1} to {2}".format(q[DNS].qd.qname,
                                                             q[IP].src,
                                                             q[IP].dst))
    send(q)


exit_flag = False


def wait():
    global exit_flag
    logging.debug("Stopping")
    exit_flag = True


def random_ip(net):
    return net[randint(1, net.num_addresses - 1)]

def work_loop():
    global exit_flag
    opts = get_options()
    queries = cycle(QueryStorage(opts.domain_file))
    networks = cycle(SourceNetworks(opts.src_ips_file))
    qps = opts.qps
    ttr = opts.time_to_run

    timer = threading.Timer(ttr, wait)
    timer.start()

    interval = 1.0 / float(qps)

    try:
        for net, qd in izip(networks, queries):
            if exit_flag:
                break
            src = random_ip(net) if opts.spoof_ips else None
            query = prep_query(qd, opts.server_addr, src)
            send_query(query)

            sleep(interval)
    except:
        timer.cancel()
        raise
