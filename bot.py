import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from vk_api.utils import get_random_id
import requests
import json
class Bot():
    def __init__(self,token='vk1.a.tRZ8mQskj1B81O8crwWmjjO-3zbzSckIljRImn2x1ujHeHN3OSMXIe43pAiVQZU5n4rw9ooKxpY93x7VWqX-yleeI8bK0QNToh4Eb3ypaV4ZkrujJRJ8hKCfgIpURUQgnX-3Ms2eFI3BlFNmO1c0PBF1tqQNMgq_f0x1d4W1ooOt42nGi5VliOWYHxms4c_w',group_id=198162597,prefix = '!'):
        vk_session = vk_api.VkApi(token=token, api_version='5.131')
        self.longpoll = VkBotLongPoll(vk=vk_session, group_id=group_id)
        self.vk = vk_session.get_api()
        self.upload = VkUpload(vk_session)
        self.session = requests.session()
        self.prefix = prefix
        self.commands = {}
        self.blacklist = {364264457:{'text':'','attachments':'video-211920841_456239489'},529152614:{'text':'иди нахуй','attachments':''}}
        self.blacklist_state= True
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
                if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
                    id = event.message.from_id
                    print(id,event.message.text)
                    if event.message.text.lower()[0]==self.prefix:
                        text = event.message.text.lower()[1:].split(' ')
                        if text[0] in self.commands:
                            self.commands[text[0]](event,' '.join(text[1:]))
                    else:
                        if id in self.blacklist and self.blacklist_state:
                            self.send_message(event,self.blacklist[id]['text'],attachments=self.blacklist[id]['attachments'])