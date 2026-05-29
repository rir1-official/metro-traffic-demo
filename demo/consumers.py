import json

from channels.generic.websocket import AsyncWebsocketConsumer


class FlowConsumer(AsyncWebsocketConsumer):
    group_name = "metro_flow"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "type": "system",
                    "message": "WebSocket connected",
                    "station": "厦门地铁演示站",
                },
                ensure_ascii=False,
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def flow_message(self, event):
        await self.send(text_data=json.dumps(event["payload"], ensure_ascii=False))
