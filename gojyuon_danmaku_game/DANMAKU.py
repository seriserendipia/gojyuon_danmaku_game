# -*- coding: utf-8 -*-
import asyncio
import random

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

import 五十音互动.blivedm_dev.blivedm as blivedm

# 直播间ID的取值看直播间URL
TEST_ROOM_IDS = [
    697
]


class DANMAKU(QThread):
    testSignal = QtCore.pyqtSignal(str)

    def run(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(DANMAKU.main(self))

    async def main(self):
        await self.run_single_client()
        # await run_multi_client()

    async def run_single_client(self):
        """
        演示监听一个直播间
        """
        room_id = random.choice(TEST_ROOM_IDS)
        # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
        client = blivedm.BLiveClient(room_id, ssl=True)
        handler = MyHandler()
        handler.notice = self.testSignal
        client.add_handler(handler)

        client.start()
        try:
            # 演示5秒后停止
            await asyncio.sleep(100)
            client.stop()

            await client.join()
        finally:
            await client.stop_and_close()


class MyHandler(blivedm.BaseHandler):

    # # 演示如何添加自定义回调
    # _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    #
    # # 入场消息回调
    # async def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
    #     print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
    #           f" uname={command['data']['uname']}")
    # _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa

    async def _on_heartbeat(self, client: blivedm.BLiveClient, message: blivedm.HeartbeatMessage):
        print(f'[{client.room_id}] 当前人气值：{message.popularity}')

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        message = f'>> {message.uname}：{message.msg}'
        print(message)
        self.notice.emit(message)

    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')

    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(DANMAKU.main())
