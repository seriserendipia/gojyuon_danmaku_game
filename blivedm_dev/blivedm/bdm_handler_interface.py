class HandlerInterface:
    """
    直播消息处理器接口
    """

    async def handle(self, client, command: dict):
        raise NotImplementedError
