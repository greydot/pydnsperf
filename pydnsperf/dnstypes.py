class QueryType(object):
    pass


class A(QueryType):
    def __str__(self):
        return "A"


class AAAA(QueryType):
    def __str__(self):
        return "AAAA"


class MX(QueryType):
    def __str__(self):
        return "MX"


def parse_query_type(str):
    res = None
    if str == 'A':
        res = A()
    elif str == 'AAAA':
        res = AAAA()
    elif str == 'MX':
        res = MX()

    return res
