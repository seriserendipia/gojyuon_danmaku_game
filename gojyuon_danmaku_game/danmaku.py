# -*- coding: utf-8 -*-
import asyncio
import random

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from blivedm_dev import blivedm
from gojyuon_danmaku_game.initdata import TEST_ROOM_IDS


class DANMAKU(QThread):
    danmaku_message_signal = QtCore.pyqtSignal(str, str)
    
    def __init__(self):
        super(DANMAKU, self).__init__()

    def run(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(DANMAKU.main(self))

    async def main(self):
        await self.run_single_client()

    async def run_single_client(self):
        """
        演示监听一个直播间
        """
        room_id = random.choice(TEST_ROOM_IDS)
        # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
        self.client = blivedm.BLiveClient(room_id, ssl=True)
        handler = MyHandler()
        handler.danmaku_message_signal = self.danmaku_message_signal
        self.client.add_handler(handler)
        self.client.start()

    async def properly_stop(self):
        try:
            self.client.stop()
            await self.client.join()
        finally:
            await self.client.stop_and_close()


class MyHandler(blivedm.BaseHandler):

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        self.danmaku_message_signal.emit(message.uname,message.msg)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(DANMAKU.main())
