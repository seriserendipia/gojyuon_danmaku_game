# -*- coding: utf-8 -*-
import asyncio
import random

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from blivedm_dev import blivedm
from customize_config import BLIVE_ROOM_ID

class DANMAKU(QThread):
    danmaku_message_signal = QtCore.pyqtSignal(str, str)
    
    def __init__(self):
        super(DANMAKU, self).__init__()

    def run(self):
        self.new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.new_loop)
        self.new_loop.run_until_complete(DANMAKU.main(self))

    async def main(self):
        await self.run_single_client()

    async def run_single_client(self):
        room_id = BLIVE_ROOM_ID
        # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
        client = blivedm.BLiveClient(room_id, ssl=True)
        handler = MyHandler1(self.danmaku_message_signal)
        client.add_handler(handler)
        client.start()

        try:
            # 演示5秒后停止
            await asyncio.sleep(100)
            client.stop()

            await client.join()
        finally:
            await client.stop_and_close()

    def properly_stop(self):
        print("关闭弹幕抓取线程")
        self.new_loop.close()

class MyHandler1(blivedm.BaseHandler):

    def __init__(self,danmaku_message_signal):
        self.danmaku_message_signal = danmaku_message_signal

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        print("抓取弹幕：")
        self.danmaku_message_signal.emit(message.uname,message.msg)

    async def _on_heartbeat(self, client: blivedm.BLiveClient, message: blivedm.HeartbeatMessage):
        print(f'[{client.room_id}] 当前人气值：{message.popularity}')


    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')

    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(DANMAKU.main())
