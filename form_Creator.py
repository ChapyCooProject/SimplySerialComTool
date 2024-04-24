import sys
import tkinter as tk
import serial.tools.list_ports
import threading

from tkinter import ttk
from tkinter import messagebox
from pprint import pformat
from module_Serial import SerialSetting
from module_Serial import SerialClose
from module_Serial import SerialReceiveStart
from module_Serial import SerialReceiveLoop
from module_Serial import SerialSendDataSingle
from module_Serial import SerialSendDataAll 
from module_Serial import SerialSendDataLine
from module_Serial import StatusFlowControl
from module_Serial import changeRTS
from module_Serial import changeDTR
from module_Logger import loggingGetLogger
from module_Threading import ThreadCustom

CHARACTOR_CODE = "ascii"

SERIAL_THREAD = None
SERIAL_STATE = False
FLOW_THREAD = None

SV_SEND_LINE = 0 # SV送受信モード時の送信データ行番号

"""
FormCreatorクラス　（tk.Frameを継承）
"""
class FormCreator(tk.Frame):

    """
    クラス初期化（定型文）
    """
    def __init__(self, master = None):

        # Window初期設定（定型文）
        super().__init__(master) # 「tk.Frame(master)」と同じ意味
        
        # メインウィンドウのタイトルを設定
        self.master.title("シリアル通信")

        # メインウィンドウのサイズを設定
        w = 1024
        h = 768
        self.master.geometry(str(w) + "x" + str(h))

        # メインウィンドウを画面中央に配置
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        self.master.geometry("+" + str(int((sw-w)/2)) + "+" + str(int((sh-h)/2)))
        
        # メニューバーの作成
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="終了", command=self.form_destroy)
        #menubar.add_command(label="設定保存", command=self.save_config)
        #menubar.add_cascade(label="終了", menu=setting_menu)
        #setting_menu.add_command(label="終了", command=self.form_destroy)

        # PanedWindowの作成
        self.panelWindow = tk.PanedWindow(self.master, orient=tk.VERTICAL, sashpad=2, sashrelief=tk.RAISED)
        #sashrelief:tk.RAISED, tk.GROOVE, tk.SUNKEN, tk.RIDGE, tk.FLAT

        # 入れ子フレームの作成
        self.frame1 = ttk.Labelframe(self.master, text="通信設定")
        self.frame2 = ttk.Labelframe(self.master, text="フロー制御・モニタ")
        self.frame3 = ttk.Labelframe(self.master, text="データ送信方法 [CL]")
        self.frame4 = ttk.Labelframe(self.panelWindow, text="送信データ")
        self.frame5 = ttk.Labelframe(self.panelWindow, text="送受信ログ")

        # PanedWindowにLabelframeを追加
        self.panelWindow.add(self.frame4)
        self.panelWindow.add(self.frame5)
        
        # //////////
        # frame1
        # //////////
        
        # ラベルの作成
        self.label1 = ttk.Label(self.frame1, text="COMポート")
        self.label2 = ttk.Label(self.frame1, text="通信速度")
        self.label3 = ttk.Label(self.frame1, text="データビット")
        self.label4 = ttk.Label(self.frame1, text="パリティ")
        self.label5 = ttk.Label(self.frame1, text="ストップビット")
        self.label6 = ttk.Label(self.frame1, text="フロー制御")
        self.label7 = ttk.Label(self.frame1, text="文字コード")

        # テキストボックスの作成
        self.tbBaudRate = ttk.Entry(self.frame1)
        self.tbBaudRate.insert(0, "9600")

        # 指定可能なCOMポートを取得
        ports = serial.tools.list_ports.comports()
        ports_asc = sorted(ports) # COMポート名でソート

        # コンボボックスにセットするリストの作成
        databitList = [4,5,6,7,8]
        parityList = ["なし（None）","奇数（Odd）","偶数（Even）"]
        stopbitList = [1,2]
        handshakeList = ["なし","Xon/Xoff","RTS/CTS","DTR/DSR"]
        charCodeList = ["ascii","shift-jis","utf-8"]

        # コンボボックスの作成
        self.cbComPort = ttk.Combobox(self.frame1, values=[port.device for port in ports_asc], state="readonly")
        self.cbDataBit = ttk.Combobox(self.frame1, values=databitList, state="readonly")
        self.cbParity = ttk.Combobox(self.frame1, values=parityList, state="readonly")
        self.cbStopBit = ttk.Combobox(self.frame1, values=stopbitList, state="readonly")
        self.cbHandShake = ttk.Combobox(self.frame1, values=handshakeList, state="readonly")
        self.cbCharCode = ttk.Combobox(self.frame1, values=charCodeList, state="readonly")
        if len(ports_asc) > 1:
            self.cbComPort.set(ports_asc[0].device)
        self.cbDataBit.set(databitList[4])
        self.cbParity.set(parityList[0])
        self.cbStopBit.set(stopbitList[0])
        self.cbHandShake.set(handshakeList[0])
        self.cbCharCode.set(charCodeList[1])

        # コマンドボタンの作成
        self.btnSerialOpen = ttk.Button(self.frame1, text="接続", command=self.SerialOpen)

        # frame1内の配置
        self.label1.grid(        row=0, column=0, padx=10, pady=2)
        self.label2.grid(        row=1, column=0, padx=10, pady=2)
        self.label3.grid(        row=2, column=0, padx=10, pady=2)
        self.label4.grid(        row=3, column=0, padx=10, pady=2)
        self.label5.grid(        row=4, column=0, padx=10, pady=2)
        self.label6.grid(        row=5, column=0, padx=10, pady=2)
        self.label7.grid(        row=6, column=0, padx=10, pady=2)
        self.cbComPort.grid(     row=0, column=1, padx=10, pady=2)
        self.tbBaudRate.grid(    row=1, column=1, padx=10, pady=2)
        self.cbDataBit.grid(     row=2, column=1, padx=10, pady=2)
        self.cbParity.grid(      row=3, column=1, padx=10, pady=2)
        self.cbStopBit.grid(     row=4, column=1, padx=10, pady=2)
        self.cbHandShake.grid(   row=5, column=1, padx=10, pady=2)
        self.cbCharCode.grid(    row=6, column=1, padx=10, pady=2)
        self.btnSerialOpen.grid( row=7, column=1, padx=10, pady=2, sticky=tk.E)
        
        # //////////
        # frame2
        # //////////

        # ラベルの作成
        self.lblRtsStatus = ttk.Label(self.frame2, text="RTS-off")
        self.lblCtsStatus = ttk.Label(self.frame2, text="CTS-off")
        self.lblDtrStatus = ttk.Label(self.frame2, text="DTR-off")
        self.lblDsrStatus = ttk.Label(self.frame2, text="DSR-off")

        # コマンドボタンの作成
        self.btnRtsOnOff = ttk.Button(self.frame2, text="RTS", command=lambda: changeRTS(self))
        self.btnDtrOnOff = ttk.Button(self.frame2, text="DTR", command=lambda: changeDTR(self))

        # frame2内の配置
        self.lblRtsStatus.grid( row=0, column=0, padx=10, pady=2)
        self.lblCtsStatus.grid( row=0, column=1, padx=10, pady=2)
        self.btnRtsOnOff.grid(  row=0, column=2, padx=10, pady=2, sticky=tk.E)
        self.lblDtrStatus.grid( row=1, column=0, padx=10, pady=2)
        self.lblDsrStatus.grid( row=1, column=1, padx=10, pady=2)
        self.btnDtrOnOff.grid(  row=1, column=2, padx=10, pady=2, sticky=tk.E)

        # //////////
        # frame3
        # //////////

        # データ送信方法の定義
        optionSendType = ["テキスト内の文字列を一度に送信","テキスト内の文字列を1行ずつ送信"]
        optionNextSend = ["ACK/NAK","指定時間毎に送信"]
        self.valSendType = tk.IntVar()
        self.valNextSend = tk.IntVar()
        
        # ラジオボタンの作成
        self.rbSendType1 = tk.Radiobutton(self.frame3, text=optionSendType[0], value=0, variable=self.valSendType, command=self.enable_radioButton)
        self.rbSendType2 = tk.Radiobutton(self.frame3, text=optionSendType[1], value=1, variable=self.valSendType, command=self.enable_radioButton)
        self.rbNextSend1 = tk.Radiobutton(self.frame3, text=optionNextSend[0], value=0, variable=self.valNextSend, state=tk.DISABLED)
        self.rbNextSend2 = tk.Radiobutton(self.frame3, text=optionNextSend[1], value=1, variable=self.valNextSend, state=tk.DISABLED)

        # ラジオボタンの初期値を設定
        self.valSendType.set(0)
        self.valNextSend.set(0)

        # ラベルの作成
        self.lblAckNak1 = ttk.Label(self.frame3, text="・ACK受信で次の行を送信", state=tk.DISABLED)
        self.lblAckNak2 = ttk.Label(self.frame3, text="・NAK受信で送信中止", state=tk.DISABLED)
        self.lblSendTime = ttk.Label(self.frame3, text="秒毎に送信", state=tk.DISABLED)

        # テキストボックスの作成
        self.tbSendTime = ttk.Entry(self.frame3, width=5, justify=tk.RIGHT)
        self.tbSendTime.insert(0, "1.0")
        self.tbSendTime.configure(state=tk.DISABLED)

        # frame3内の配置
        self.rbSendType1.grid(row=0, column=0, padx=10, pady=2, sticky=tk.W)
        self.rbSendType2.grid(row=1, column=0, padx=10, pady=2, sticky=tk.W)
        self.rbNextSend1.grid(row=2, column=0, padx=30, pady=2, sticky=tk.W)
        self.lblAckNak1.grid( row=3, column=0, padx=60, pady=2, sticky=tk.W)
        self.lblAckNak2.grid( row=4, column=0, padx=60, pady=2, sticky=tk.W)
        self.rbNextSend2.grid(row=5, column=0, padx=30, pady=2, sticky=tk.W)
        self.tbSendTime.grid( row=6, column=0, padx=60, pady=2, sticky=tk.W)
        self.lblSendTime.grid(row=6, column=0, padx=100, pady=2, sticky=tk.W)

        # //////////
        # frame4
        # //////////

        # スクロールバー付きテキストボックスの作成
        self.txtSendText = tk.Text(self.frame4, width=10, height=10, wrap=tk.NONE, font=("BIZ UDゴシック", 9)) #font="TkDefaultFont"
        self.vscSendText = tk.Scrollbar(self.frame4, orient=tk.VERTICAL, command=self.txtSendText.yview)
        self.hscSendText = tk.Scrollbar(self.frame4, orient=tk.HORIZONTAL, command=self.txtSendText.xview)
        self.txtSendText["yscrollcommand"] = self.vscSendText.set
        self.txtSendText["xscrollcommand"] = self.hscSendText.set

        # テキストボックスの選択行に適用するタグ
        self.txtSendText.tag_configure("selected", background="yellow")  

        # コマンドボタン用フレームの作成
        self.frame4b = tk.Frame(self.frame4)

        # ラベルの作成
        self.lblSerialState = ttk.Label(self.frame4b, text="[ SV送受信モード：停止中 ]")
        self.lblSerialClient = ttk.Label(self.frame4b, text="[ CL送信モード ]")

        # コマンドボタンの作成
        self.btnThreadStart = ttk.Button(self.frame4b, text="[SV]待ち受け開始", command=self.threadStart)
        self.btnServerSend = ttk.Button(self.frame4b, text="[SV]データ送信", command=self.SerialServerSend)
        self.btnThreadEnd = ttk.Button(self.frame4b, text="[SV]待ち受け停止", command=self.threadEnd)
        self.btnClientSend = ttk.Button(self.frame4b, text="[CL]データ送信", command=self.SerialClientSend)

        # frame4内の配置
        self.txtSendText.grid(row=0, column=0, padx=1, pady=1, sticky=tk.EW+tk.NS)
        self.hscSendText.grid(row=1, column=0, padx=1, pady=1, sticky=tk.EW)
        self.vscSendText.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NS+tk.E)
        self.frame4b.grid(    row=2, column=0, padx=1,  pady=1, sticky=tk.EW+tk.NS)
        # frame4b内の配置
        self.lblSerialState.grid(  row=0, column=0, padx=5, pady=10)
        self.btnThreadStart.grid(  row=0, column=1, padx=5, pady=10)
        self.btnServerSend.grid(   row=0, column=2, padx=5, pady=10)
        self.btnThreadEnd.grid(    row=0, column=3, padx=5, pady=10)
        self.lblSerialClient.grid( row=0, column=4, padx=5, pady=10)
        self.btnClientSend.grid(   row=0, column=5, padx=5, pady=10)

        self.frame4.grid_columnconfigure(0, weight=1) # 列の調整
        self.frame4.grid_rowconfigure(0, weight=1) # 行の調整

        # //////////
        # frame5
        # //////////

        # スクロールバー付きテキストボックスの作成
        self.txtSerialLog = tk.Text(self.frame5, width=10, height=10, wrap=tk.NONE, font=("BIZ UDゴシック", 9)) #font="TkDefaultFont"
        self.vscSerialLog = tk.Scrollbar(self.frame5, orient=tk.VERTICAL, command=self.txtSerialLog.yview)
        self.hscSerialLog = tk.Scrollbar(self.frame5, orient=tk.HORIZONTAL, command=self.txtSerialLog.xview)
        self.txtSerialLog["yscrollcommand"] = self.vscSerialLog.set
        self.txtSerialLog["xscrollcommand"] = self.hscSerialLog.set

        # frame5内の配置
        self.txtSerialLog.grid(row=0, column=0, padx=1, pady=1, sticky=tk.EW+tk.NS)
        self.hscSerialLog.grid(row=1, column=0, padx=1, pady=1, sticky=tk.EW)
        self.vscSerialLog.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NS)
        self.frame5.grid_columnconfigure(0, weight=1) # 列の調整
        self.frame5.grid_rowconfigure(0, weight=1) # 行の調整

        # //////////
        # frameの配置
        # //////////

        # 要素の配置
        self.frame1.grid(row=0, column=0, padx=10, pady=5)
        self.frame2.grid(row=1, column=0, padx=10, pady=5)
        self.frame3.grid(row=2, column=0, padx=10, pady=5, sticky=tk.EW+tk.NS)
        self.panelWindow.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky=tk.EW+tk.NS)

        # ウィンドウのリサイズに合わせて幅と高さを広げる
        self.master.grid_columnconfigure(1, weight=1) # 列の調整
        self.master.grid_rowconfigure(2, weight=1) # 行の調整

        # //////////
        # Windowボタン
        # //////////

        # xボタンが押下された時
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.form_destroy())

    """
    シリアル通信 接続／切断
    """
    def SerialOpen(self):

        try:

            global SERIAL_STATE

            if SERIAL_STATE:
                
                self.threadEnd()
                SerialClose(self)
                SERIAL_STATE = False
                self.btnSerialOpen.configure(text="接続")
                self.btnSerialOpen.state(["active"])

            else:

                SerialSetting(self)
                SERIAL_STATE = True
                self.btnSerialOpen.configure(text="切断")
                self.btnSerialOpen.state(["pressed"])
                self.FlowControlStart()

        except Exception as e:

            messagebox.showinfo("SerialOpen", pformat(e))
            logger = loggingGetLogger()
            logger.error(pformat(e))
        

    """
    送受信スレッド 開始
    """
    def threadStart(self):

        try:

            if not SERIAL_STATE:
                messagebox.showerror("送受信スレッド 開始", "未接続のため、送受信スレッドを開始できません。")
                return

            # 送受信変数 初期化
            SerialReceiveStart
            global SV_SEND_LINE
            SV_SEND_LINE = 0
            self.txtSendText.tag_remove("selected", "1.0", "end")

            # 送受信スレッド 開始
            global SERIAL_THREAD
            SERIAL_THREAD = None
            SERIAL_THREAD = ThreadCustom(SerialReceiveLoop, (self,), "シリアル送受信スレッド", 0.01)
            SERIAL_THREAD.begin()

            self.lblSerialState.configure(text="[ SV送受信モード：動作中 ]")

        except Exception as e:

            messagebox.showinfo("threadStart", pformat(e))
            logger = loggingGetLogger()
            logger.error(pformat(e))


    """
    送受信スレッド 一時停止
    """
    def threadStop(self):

        try:

            tcnt = threading.active_count()
    
            global SERIAL_THREAD
            
            if tcnt > 1:
                SERIAL_THREAD.stop()
                self.lblSerialState.configure(text="[ SV送受信モード：一時停止 ]")

        except Exception as e:

            messagebox.showinfo("threadStop", pformat(e))
            logger = loggingGetLogger()
            logger.error(pformat(e))

    """
    送受信スレッド 再開
    """
    def threadRestart(self):

        try:

            tcnt = threading.active_count()
    
            global SERIAL_THREAD
            
            if tcnt > 1:
                SERIAL_THREAD.restart()
                self.lblSerialState.configure(text="[ SV送受信モード：動作中 ]")

        except Exception as e:

            messagebox.showinfo("threadRestart", pformat(e))
            logger = loggingGetLogger()
            logger.error(pformat(e))

    """
    送受信スレッド 停止
    """
    def threadEnd(self):

        try:

            global SERIAL_THREAD

            if SERIAL_THREAD == None:
                return

            if SERIAL_THREAD.alive:
                SERIAL_THREAD.end()
                SERIAL_THREAD = None
                self.lblSerialState.configure(text="[ SV送受信モード：停止中 ]")

        except Exception as e:

            messagebox.showinfo("threadEnd", pformat(e))
            logger = loggingGetLogger()
            logger.error(pformat(e))


    """
    フロー制御スレッド 開始
    """
    def FlowControlStart(self):

        try:

            if not SERIAL_STATE:
                messagebox.showerror("フロー制御スレッド 開始", "未接続のため、フロー制御スレッドを開始できません。")
                return

            # フロー制御スレッド 開始
            global FLOW_THREAD
            FLOW_THREAD = None
            FLOW_THREAD = ThreadCustom(StatusFlowControl, (self,), "フロー制御スレッド", 0.1)
            FLOW_THREAD.begin()

        except Exception as e:

            messagebox.showinfo("FlowthreadStart", pformat(e))
            logger = loggingGetLogger()
            logger.error(pformat(e))


    """
    フロー制御スレッド 停止
    """
    def FlowControlEnd(self):

        try:

            global FLOW_THREAD
            
            if FLOW_THREAD == None:
                return

            if FLOW_THREAD.alive:
                FLOW_THREAD.end()
                FLOW_THREAD = None

        except Exception as e:

            messagebox.showinfo("FlowthreadEnd", pformat(e))
            logger = loggingGetLogger()
            logger.error(pformat(e))


    def save_config(self):
        # 通信設定の保存（iniファイル形式）
        messagebox.showinfo("シリアル通信","通信設定を保存しました。")


    def SerialServerSend(self):
        # [SV]データ送信ボタンのクリック時の処理

        global SV_SEND_LINE

        # 行数の取得        
        lineCount = self.txtSendText.index("end-1c").split(".")[0]

        if int(lineCount) > SV_SEND_LINE:

            # 対象行の表示        
            self.txtSendText.tag_remove("selected", "1.0", "end")
            lineStart = f"{SV_SEND_LINE + 1}.0"
            lineEnd = f"{SV_SEND_LINE + 2}.0"
            self.txtSendText.tag_add("selected", lineStart, lineEnd)
            self.txtSendText.see(lineStart)

            # 対象行の文字列を取得        
            sendStr = self.txtSendText.get(lineStart, lineEnd)
            sendStr = sendStr.rstrip("\r\n")

            # データ送信
            SerialSendDataSingle(self, sendStr)

            # 次の行へ
            SV_SEND_LINE += 1

            if int(lineCount) == SV_SEND_LINE:
                messagebox.showinfo("シリアル通信","最後の行までデータを送信しました。")


    def SerialClientSend(self):
        # [CL]データ送信ボタンのクリック時の処理
        if self.valSendType.get() == 0:
            SerialSendDataAll(self)
        else:
            SerialSendDataLine(self, 
                               self.valNextSend.get(), 
                               self.tbSendTime.get())

        messagebox.showinfo("シリアル通信","データ送信が終了しました。")


    def form_destroy(self):
        # プログラム終了

        if SERIAL_STATE:
            messagebox.showerror("終了確認", "接続中のため終了できません。先に切断してください。")
            return

        if messagebox.askokcancel("終了前の確認","終了しますか？"):
            # スレッド停止
            self.threadEnd()
            self.FlowControlEnd()
            SERIAL_THREAD = None
            FLOW_THREAD = None
            # プログラム終了
            #self.master.destroy()
            sys.exit()

    
    def enable_radioButton(self):
        if self.valSendType.get() == 0:
            self.rbNextSend1.configure(state=tk.DISABLED)
            self.lblAckNak1.configure(state=tk.DISABLED)
            self.lblAckNak2.configure(state=tk.DISABLED)
            self.rbNextSend2.configure(state=tk.DISABLED)
            self.tbSendTime.configure(state=tk.DISABLED)
            self.lblSendTime.configure(state=tk.DISABLED)
        else:
            self.rbNextSend1.configure(state=tk.NORMAL)
            self.lblAckNak1.configure(state=tk.NORMAL)
            self.lblAckNak2.configure(state=tk.NORMAL)
            self.rbNextSend2.configure(state=tk.NORMAL)
            self.tbSendTime.configure(state=tk.NORMAL)
            self.lblSendTime.configure(state=tk.NORMAL)

