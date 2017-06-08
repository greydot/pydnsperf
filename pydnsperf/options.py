class Options(object):
    def __init__(self, args):
        self.domain_file = args.d[0]
        self.server_addr = args.s[0]
        self.spoof_ips = args.spoof_source
        self.src_ips_file = args.source_file[0] if args.source_file is not None else None
        self.qps = args.Q
        self.time_to_run = args.l


__options = None


def get_options():
    return __options


def set_options(opts):
    global __options
    __options = opts


def prepare_args(parser):
    parser.add_argument('-d',
                        nargs=1,
                        metavar='<filename>',
                        required=True,
                        help='Domain list')
    parser.add_argument('-s',
                        nargs=1,
                        metavar='<server>',
                        help='Server name',
                        default='localhost')
    parser.add_argument('--spoof-source',
                        default=False,
                        action='store_true',
                        help='Spoof source IPs')
    parser.add_argument('--source-file',
                        nargs=1,
                        metavar='<filename>',
                        help='Path to file with source ips/networks')
    parser.add_argument('-Q',
                        default=1,
                        nargs=1,
                        metavar='<N>',
                        type=int,
                        help='Queries per second')
    parser.add_argument('-l',
                        default=60,
                        nargs=1,
                        metavar='<N>',
                        type=int,
                        help='Run time period')


