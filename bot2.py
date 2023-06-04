import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from vk_api.audio import VkAudio
from vk_api.utils import get_random_id
import requests
import json
class Bot():
    def __init__(self,login='+79818179073',password='Cdtnkbr178',prefix = '!'):
        vk_session = vk_api.VkApi(login, password)
        self.longpoll = VkLongPoll(vk=vk_session)
        vk_session.auth()
        self.vk = vk_session.get_api()
        self.upload = VkUpload(vk_session)
        self.session = requests.session()
        self.prefix = prefix
        self.commands = {}
        self.audio = VkAudio(vk_session)
    def add_command(self,func,name = None):
        self.commands[func.__name__ if name==None else name] = func
    def attach_photos(self,urls):
        attachments = []
        for url in urls:
            image = self.session.get(url, stream=True)
            photo = self.upload.photo_messages(photos=image.raw)[0]
            attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
        return ','.join(attachments)

    def attach_doc(self,event,docs):
        attachments = []
        for doc in docs:
            result = json.loads(requests.post(self.vk.docs.getMessagesUploadServer(type='doc', peer_id=event.message.peer_id)['upload_url'],
                                              files={'file': open(doc, 'rb')}).text)
            jsonAnswer = self.vk.docs.save(file=result['file'], title=doc, tags=[])
            attachments.append(f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}")
        return ','.join(attachments)

    def send_message(self,event,message='',attachments=''):
        try:
            self.vk.messages.send(peer_id=event.message.peer_id, message=message, random_id=get_random_id(),attachment=attachments)
        except:
            pass
    def run(self):
        while True:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.message.text:
                    if event.message.text.lower()[0]==self.prefix:
                        text = event.message.text.lower()[1:].split()
                        if text[0] in self.commands:
                            self.commands[text[0]](event,text[1:])