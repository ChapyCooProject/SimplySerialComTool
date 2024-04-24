from logging import getLogger, Formatter, FileHandler, StreamHandler, DEBUG, ERROR, INFO

def loggingGetLogger():

    # logger定義
    logger = getLogger(__name__)

    # loggerのログレベルをDEBUGに設定（ここではとりあえず全レベルを出力対象とする）
    logger.setLevel(DEBUG)

    # ログ出力フォーマットを設定
    formatter = Formatter("%(asctime)s\t%(levelname)s\t%(funcName)s\t%(filename)s\tLine:%(lineno)d\t%(message)s")

    # ////////////////////////////////////////
    # ファイル出力するためのFileHandlerを設定
    # ////////////////////////////////////////
    file_handler = FileHandler("error.log")
    file_handler.setLevel(ERROR)
    file_handler.setFormatter(formatter)
    
    # ////////////////////////////////////////
    # コンソールに出力するためのStreamHandlerを設定
    # ////////////////////////////////////////
    # stream_handler = StreamHandler()
    # stream_handler.setFormatter(formatter)
    # stream_handler.setLevel(INFO)
    
    # loggerにハンドラーを追加（hasHandlersを使用しないとログが積み重なってしまうため。）
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        # logger.addHandler(stream_handler)

    return logger

# logger.debug("debug")
# logger.info("info")
# logger.warning("warning")
# logger.error("error")
# logger.critical("critical")

