class ping_data:
    def __init__(self, data, stat, str, val, errs, speed, proxy, proxy_num):
        self.data = data
        self.stat = stat
        self.str = str
        self.valid = val
        self.errs = errs
        self.speed = speed
        self.proxy = proxy
        self.proxy_num = proxy_num

class comm_data:
    def __init__(self, data, ar):
        self.comm = data
        self.ar = ar
class msg_data:

    def __init__(self, msg):
        self.msg = msg

class client_item:

    def __init__(self, obj, addr, id):
        self.sock = obj
        self.addr = addr
        self.id = id
        self.stat = None
        self.str = None
        self.valid = None
        self.errs = None
        self.speed = None
        self.proxy = None
        self.proxy_num = None


    def getbynum(self,n=None):
        if n==0:
            return self.id
        elif n==1:
            return self.addr
        elif n==2:
            if self.stat == 1:
                res = "Working"
            elif self.stat == 2:
                res = "Zanyat"
            else:
                res = "Chilling"
            return res
        elif n==3:return self.str
        elif n==4:return self.valid
        elif n==5:return self.errs
        elif n==6:return self.proxy
        elif n==None: return 7

import ssl
import datetime

from socks import create_connection
from socks import PROXY_TYPE_SOCKS4
from socks import PROXY_TYPE_SOCKS5
from socks import PROXY_TYPE_HTTP

from imaplib import IMAP4
from imaplib import IMAP4_PORT
from imaplib import IMAP4_SSL_PORT

__author__ = "sstevan"
__license__ = "GPLv3"
__version__ = "0.1"


class SocksIMAP4(IMAP4):

    """
    IMAP service trough SOCKS proxy. PySocks module required.
    """

    PROXY_TYPES = {"socks4": PROXY_TYPE_SOCKS4,
                   "socks5": PROXY_TYPE_SOCKS5,
                   "http": PROXY_TYPE_HTTP}

    def __init__(self, host, port=IMAP4_PORT, proxy_addr=None, proxy_port=None,
                 rdns=True, username=None, password=None, proxy_type="socks5"):

        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
        self.rdns = rdns
        self.username = username
        self.password = password
        self.proxy_type = SocksIMAP4.PROXY_TYPES[proxy_type.lower()]

        IMAP4.__init__(self, host, port)

    def _create_socket(self):
        return create_connection((self.host, self.port), proxy_type=self.proxy_type, proxy_addr=self.proxy_addr,
                                 proxy_port=self.proxy_port, proxy_rdns=self.rdns, proxy_username=self.username,
                                 proxy_password=self.password)


class SocksIMAP4SSL(SocksIMAP4):

    def __init__(self, host='', port=IMAP4_SSL_PORT, keyfile=None, certfile=None, ssl_context=None, proxy_addr=None,
                 proxy_port=None, rdns=True, username=None, password=None, proxy_type="socks5"):

        if ssl_context is not None and keyfile is not None:
                raise ValueError("ssl_context and keyfile arguments are mutually "
                                 "exclusive")
        if ssl_context is not None and certfile is not None:
            raise ValueError("ssl_context and certfile arguments are mutually "
                             "exclusive")

        self.keyfile = keyfile
        self.certfile = certfile
        if ssl_context is None:
            ssl_context = ssl._create_stdlib_context(certfile=certfile,
                                                     keyfile=keyfile)
        self.ssl_context = ssl_context

        SocksIMAP4.__init__(self, host, port, proxy_addr=proxy_addr, proxy_port=proxy_port,
                            rdns=rdns, username=username, password=password, proxy_type=proxy_type)

    def _create_socket(self):
        sock = SocksIMAP4._create_socket(self)
        server_hostname = self.host if ssl.HAS_SNI else None
        return self.ssl_context.wrap_socket(sock, server_hostname=server_hostname)

    def open(self, host='', port=IMAP4_PORT):
        SocksIMAP4.open(self, host, port)


if __name__ == "__main__":

    email = "mynewmixfair@yahoo.com"
    password = "fpctx&intl"
    imap_server = "imap.mail.yahoo.com"
    imap_port = 993

    proxy_addr = "127.0.0.1"
    proxy_port = 8118
    proxy_type = "http"



def _get_connection():
    from stem import Signal
    from stem.control import Controller

    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="testpw")
        controller.signal(Signal.NEWNYM)
        controller.close()

class ErrorTypeSns():
    def __init__(self, type):
        self.type = type
        self.n = 1

        now = datetime.datetime.now()
        fd = open(self.type+'.txt', 'a')
        fd.write('\n' + now.strftime("%d-%m-%Y %H:%M") + '\n\n')

    def WriteError(self, info, signal=False, place="Unknown"):
        data = ""
        print(type(info[0]))
        if type(info) == list:
            for i in info:
                data = data + str(i) + " || "
        else:
            data = info

        if signal: self.PrintSignalErr(data, place)
        fd = open(self.type+'.txt', 'a')
        fd.write(str(self.n)  + '. Place: ' + place + '. ' + data + '\n')
        fd.close()

        self.ErrorInc()
    def PrintSignalErr(self, data, place="Unknown"):
        print("Detected: "+self.type+". Place:" + place + ". Info:" + data)

    def GetName(self):
        return self.type

    def GetErrNum(self):
        return self.n

    def ErrorInc(self):
        self.n = self.n + 1

