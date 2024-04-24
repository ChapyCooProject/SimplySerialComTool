import threading
import time
import logging

class ThreadCustom(threading.Thread):

    """
    クラス初期化
    """
    def __init__(self, target, args, name, interval):

        super().__init__()

        self.target = target
        self.args = args
        self.name = name
        self.interval = interval
        self.alive = False
        self.daemon = True #2024.01.25 終了時にフリーズする問題を回避（RuntimeError: main thread is not in main loop）

        self.event = threading.Event()
        self.event.clear() #内部フラグ=False

        self.start()

        #logging.basicConfig(
        #    filename="ThreadCustom.log",
        #    level=logging.DEBUG,
        #    format="%(asctime)s.%(msecs)d\t[%(levelname)s] %(message)s",
        #    datefmt="%Y/%m/%d %H:%M:%S"
        #)
        #logging.debug(f"{self.name}: start")

    """
    スレッド開始
    """
    def begin(self):
        #logging.debug(f"{self.name}: begin")
        self.alive = True
        self.event.set() #内部フラグ=True

    """
    スレッド停止
    """
    def stop(self):
        #logging.debug(f"{self.name}: stop")
        self.event.clear() #内部フラグ=False

    """
    スレッド再開
    """
    def restart(self):
        #logging.debug(f"{self.name}: restart")
        self.event.set() #内部フラグ=True

    """
    スレッド終了
    """
    def end(self):
        #logging.debug(f"{self.name}: end")
        self.alive = False
        self.event.set() #内部フラグ=True
        self.join()

    def run(self):

        self.event.wait() #内部フラグがTrueならば以降の処理へ

        while self.alive:

            #logging.debug(f"{self.name}: alive")
            
            # シリアル通信処理（エラー発生時はループを抜ける）
            ret = self.target(self.args[0])
            if ret == False:
                self.event.clear() #内部フラグ=False
                self.alive = False #end
                break

            # 指定の秒数だけ待機
            time.sleep(self.interval)
            
            self.event.wait() #内部フラグがTrueならば以降の処理へ

