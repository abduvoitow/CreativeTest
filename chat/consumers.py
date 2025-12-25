import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'message')
        
        if message_type == 'read_receipt':
            # O'qilgan deb belgilash
            sender = data['sender']
            await self.mark_messages_read(sender)
            
            # Boshqalarga xabar berish
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_update',
                    'reader': sender
                }
            )
        else:
            # Oddiy xabar
            sender = data['sender']
            message = data['message']
            
            # Xabarni saqlash
            msg = await self.save_message(sender, message)
            
            # Barchaga yuborish
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': sender,
                    'message': message,
                    'message_id': msg.id,
                    'timestamp': msg.timestamp.strftime('%H:%M'),
                    'is_read': msg.is_read
                }
            )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender': event['sender'],
            'message': event['message'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
            'is_read': event['is_read']
        }))
    
    async def read_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read_update',
            'reader': event['reader']
        }))
    
    @database_sync_to_async
    def save_message(self, sender, content):
        message = Message.objects.create(sender=sender, content=content)
        return message
    
    @database_sync_to_async
    def mark_messages_read(self, reader):
        # Boshqa foydalanuvchidan kelgan xabarlarni o'qilgan qilish
        Message.objects.filter(is_read=False).exclude(sender=reader).update(
            is_read=True,
            read_at=timezone.now()
        )
