from bot import Bot
import genuis
import ximia
import myparse
import ED
import bazar
import random
import niks
def main():
    bot = Bot()
    sl = {'физика_сборник':myparse.fizika_sborbik,
          'физика':myparse.fizika,
          'русский':myparse.russian,
          'литра':myparse.litra,
          'общество':myparse.obshestvo,
          'алгебра':myparse.algebra,
          }
    @bot.add_command
    def команды(event,args):
        bot.send_message(event,'\n'.join(list(bot.commands.keys())))

    @bot.add_command
    def реакция(event,args):
        bot.send_message(event,ximia.get_reaction(args))


    @bot.add_command
    def цепочка(event,args):
        bot.send_message(event,ximia.get_seq_reaction(args))

    @bot.add_command
    def базар(event,args):
        sl = bazar.get()
        if args=='':
            key = random.choice(list(sl.keys()))
            bot.send_message(event,f'{key} -{sl[key]}')
        else:
            try:
                bot.send_message(event,sl[args.lower()])
            except:
                bot.send_message(event, 'Пиздишь')

    @bot.add_command
    def ник(event,args):
        try:
            if args=='':
                bot.send_message(event, niks.get_random())
            else:
                 bot.send_message(event, '\n'.join([niks.get_random() for i in range(int(args))]))
        except:
            bot.send_message(event, 'Ну ёбушки воробушки, тебе 13 лет, команды голос не было')
    @bot.add_command
    def эд(event,args):
        temp = ED.get_all_hometask()
        bot.send_message(event,'\n'.join([i+' : '+temp[i] for i in temp]))

    @bot.add_command
    def текст(event,args):
        bot.send_message(event, genuis.get(args))

    @bot.add_command
    def никбазар(event,args):
        sl = bazar.get()
        bot.send_message(event, bot.send_message(event, random.choice(list(sl.keys()))+' '+random.choice(list(sl.keys()))))

    @bot.add_command
    def посудомойка(event,args):
        if event.message.from_id not in bot.blacklist:
            bot.blacklist_state = False if bot.blacklist_state else True
    @bot.add_command
    def дз(event,args):
        print('+дз')
        for t in args.split('\n')[1:]:
            t = t.lower().split()
            for i in t[1:]:
                if t[0] in sl:
                    print(i)
                    bot.send_message(event,attachments=bot.attach_photos(sl[t[0]](str(i))))
    @bot.add_command
    def предметы(event,args):
        bot.send_message(event,message='\n'.join([i for i in sl]))
    bot.run()
main()