import os
import sys
import serial
import datetime

from time import sleep
from tkinter import messagebox
from pprint import pformat
from module_Logger import loggingGetLogger
from controlCodes import *

ISerial = None
RecvBytes = b""
WaitCount = 0

# ログ出力
def outputSerialLog(logStr, logType):
    
    # 日時取得
    dt_now = datetime.datetime.now()

    # 出力先フルパス
    currentPath = os.path.dirname(sys.argv[0])
    txtPath = os.path.join(currentPath, "serialLog" + dt_now.strftime("%Y%m%d") + ".txt")

    # 送信ログ、受信ログ、それ以外
    logOpt = ""
    if logType == "None":
        logOpt = "\t----\t" # その他ログ
    if logType == "Send":
        logOpt = "\t--->\t" # 送信ログ
    if logType == "Recv":
        logOpt = "\t<---\t" # 受信ログ

    # ファイル書き出し
    f = open(txtPath, "a")
    f.write(dt_now.strftime("%Y/%m/%d %H:%M:%S"))
    f.write(logOpt)
    f.write(logStr)
    f.write("\n")
    f.close()


def SerialSetting(self):

    global ISerial

    try:
        ISerial = serial.Serial()
        
        # COMポート
        ISerial.port = self.cbComPort.get()

        # 通信速度（ボーレート）
        ISerial.baudrate = self.tbBaudRate.get()

        # データビット
        ISerial.bytesize = int(self.cbDataBit.get())

        # パリティ
        if self.cbParity.current() == 0:
            # なし（None）
            ISerial.parity = "N"
        if self.cbParity.current() == 1:
            # 奇数（Odd）
            ISerial.parity = "O"
        if self.cbParity.current() == 2:
            # 偶数（Even）
            ISerial.parity = "E"

        # ストップビット
        ISerial.stopbits = int(self.cbStopBit.get())

        # ハンドシェイク
        if self.cbHandShake.current() == 0:
            # なし
            ISerial.xonxoff = False
            ISerial.rtscts = False
            ISerial.dsrdtr = False
        if self.cbHandShake.current() == 1:
            # Xon/Xoff
            ISerial.xonxoff = True
            ISerial.rtscts = False
            ISerial.dsrdtr = False
        if self.cbHandShake.current() == 2:
            # RTS/CTS
            ISerial.xonxoff = False
            ISerial.rtscts = True
            ISerial.dsrdtr = False
        if self.cbHandShake.current() == 3:
            # DTR/DSR
            ISerial.xonxoff = False
            ISerial.rtscts = False
            ISerial.dsrdtr = True

        # タイムアウト
        # None: 受信/送信が完了するまで待つ
        # 0   : 直ちに処理が返る（ノンブロッキングモード）
        # n   : n秒でタイムアウト
        ISerial.timeout = 0
        ISerial.write_timeout = 5
        
        # 文字コード
        global CHARACTOR_CODE
        CHARACTOR_CODE = self.cbCharCode.get()

        ISerial.open()

        outputSerialLog("シリアル通信 接続", "None")

    except Exception as e:
        messagebox.showinfo("SettingSerial", pformat(e))
        logger = loggingGetLogger()
        logger.error(pformat(e))


def SerialClose(self):

    global ISerial
    ISerial.close()

    outputSerialLog("シリアル通信 切断", "None")


def StatusFlowControl(self):

    global ISerial
    
    if not ISerial.isOpen():
        self.lblRtsStatus.configure(text="RTS-off")
        self.lblCtsStatus.configure(text="CTS-off")
        self.lblDtrStatus.configure(text="DTR-off")
        self.lblDsrStatus.configure(text="DSR-off")
        return
    
    if ISerial.rts:
        self.lblRtsStatus.configure(text="RTS-on")
    else:
        self.lblRtsStatus.configure(text="RTS-off")

    if ISerial.cts:
        self.lblCtsStatus.configure(text="CTS-on")
    else:
        self.lblCtsStatus.configure(text="CTS-off")

    if ISerial.dtr:
        self.lblDtrStatus.configure(text="DTR-on")
    else:
        self.lblDtrStatus.configure(text="DTR-off")

    if ISerial.dsr:
        self.lblDsrStatus.configure(text="DSR-on")
    else:
        self.lblDsrStatus.configure(text="DSR-off")


def changeRTS(self):

    global ISerial

    if ISerial.rts:
        ISerial.rts = False
    else:
        ISerial.rts = True

    outputSerialLog("RTS変更", "None")


def changeDTR(self):

    global ISerial

    if ISerial.dtr:
        ISerial.dtr = False
    else:
        ISerial.dtr = True

    outputSerialLog("DTR変更", "None")


def SerialReceiveStart(self):
    global RecvBytes
    global WaitCount
    RecvBytes = b""
    WaitCount = 0

    
def SerialReceiveLoop(self):

    try:

        # データ受信

        global RecvBytes
        global WaitCount

        recvFin = False

        data = ISerial.read(256)
        if data:
            RecvBytes += data
        else:
            WaitCount += 1
            
        if WaitCount > 150: # 最大1.5秒待機
            recvFin = True

        # ASTM対応・制御コード
        if RecvBytes.decode(CHARACTOR_CODE).startswith(ACK):
            recvFin = True
        if RecvBytes.decode(CHARACTOR_CODE).startswith(NAK):
            recvFin = True
        if RecvBytes.decode(CHARACTOR_CODE).startswith(ENQ):
            recvFin = True
        if RecvBytes.decode(CHARACTOR_CODE).endswith(LF):
            recvFin = True
        if RecvBytes.decode(CHARACTOR_CODE).startswith(EOT):
            recvFin = True

        if recvFin and RecvBytes:
            # バイト列を文字列に変換
            recvStr = RecvBytes.decode(CHARACTOR_CODE)
        
            # 送受信テキストボックスに出力
            dt_now = datetime.datetime.now()
            self.txtSerialLog.insert("1.0", 
                                     dt_now.strftime("%Y/%m/%d %H:%M:%S") 
                                     + "\t<---\t" 
                                     + bin2str_controlCode(recvStr) 
                                     + "\r\n")
            self.txtSerialLog.update()
            outputSerialLog(bin2str_controlCode(recvStr), "Recv")
            
        if recvFin:
            # 受信変数リセット
            SerialReceiveStart(self)

        # 故意にエラー発生
        #raise ValueError("error!")

        """
        # テキストボックスの有効無効を繰り返す
        state = self.tbBaudRate["state"]
        print(type(state))
        print("A:" + str(state))
        if str(state) == "normal":
            print("B:normal")
            self.tbBaudRate.after(0, update_textbox, self, tk.DISABLED)
        else:
            print("B:disabled")
            self.tbBaudRate.after(0, update_textbox, self, tk.NORMAL)
        """

        return True

    except Exception as e:

        messagebox.showinfo("SerialReceiveLoop", pformat(e))
        logger = loggingGetLogger()
        logger.error(pformat(e))

        return False


def update_textbox(self, value):

    self.tbBaudRate.configure(state=value)


def SerialSendDataSingle(self, sendData):

    if sendData:
        # データ送信（文字列をバイト列に変換）
        ISerial.write(str2bin_controlCode(sendData).encode(CHARACTOR_CODE))

        # 送受信テキストボックスに出力
        dt_now = datetime.datetime.now()
        self.txtSerialLog.insert("1.0", 
                                 dt_now.strftime("%Y/%m/%d %H:%M:%S") 
                                 + "\t--->\t" 
                                 + sendData
                                 + "\r\n")
        self.txtSerialLog.update()
        outputSerialLog(sendData, "Send")


def SerialSendDataAll(self):

    sendData = ""

    # 各行を配列で取得
    records = self.txtSendText.get("1.0", "end").splitlines()

    for rec in records:
        if rec.strip():  # 空行を無視
            sendData += rec

    if sendData:
        # データ送信（文字列をバイト列に変換）
        ISerial.write(str2bin_controlCode(sendData).encode(CHARACTOR_CODE))

        # 送受信テキストボックスに出力
        dt_now = datetime.datetime.now()
        self.txtSerialLog.insert("1.0", 
                                 dt_now.strftime("%Y/%m/%d %H:%M:%S") 
                                 + "\t--->\t" 
                                 + sendData
                                 + "\r\n")
        self.txtSerialLog.update()
        outputSerialLog(sendData, "Send")


def SerialSendDataLine(self, nextSend, sendTime):

    sendStatus = True

    # 各行を配列で取得
    records = self.txtSendText.get("1.0", "end").splitlines()

    for rec in records:

        if rec.strip():  # 空行を無視

            # データ送信（文字列をバイト列に変換）
            ISerial.write(str2bin_controlCode(rec).encode(CHARACTOR_CODE))

            # フォーム上のテキストボックスにログを表示
            dt_now = datetime.datetime.now()
            self.txtSerialLog.insert("1.0", 
                                     dt_now.strftime("%Y/%m/%d %H:%M:%S") 
                                     + "\t--->\t" 
                                     + rec 
                                     + "\r\n")
            self.txtSerialLog.update()
            outputSerialLog(rec, "Send")
            
            if nextSend == 0:
                # 応答電文[ACK]の受信待ち（0.1x30秒でタイムアウト）
                waitCount = 0
                recvBin = b""

                while waitCount < 30:
                    data = ISerial.read(1)
                    if data:
                        recvBin += data
                    if data.decode(CHARACTOR_CODE) == ACK:
                        break
                    if data.decode(CHARACTOR_CODE) == NAK:
                        sendStatus = False
                        break
                    sleep(0.1)
                    waitCount += 1

                if recvBin:
                    # バイト列を文字列に変換
                    recvStr = recvBin.decode(CHARACTOR_CODE)
        
                    # 送受信テキストボックスに出力
                    dt_now = datetime.datetime.now()
                    self.txtSerialLog.insert("1.0", 
                                             dt_now.strftime("%Y/%m/%d %H:%M:%S") 
                                             + "\t<---\t" 
                                             + bin2str_controlCode(recvStr) 
                                             + "\r\n")
                    self.txtSerialLog.update()
                    outputSerialLog(bin2str_controlCode(recvStr), "Recv")

            else:
                # 指定秒数待機
                sleep(float(sendTime))

        if not sendStatus:
            break # for
