import discord
import json
import random

from discord.ext import commands, tasks
from time import time, sleep
from config import settings, voiceList
from TechModule import say, translit, preparKey, saveReminder

answer = json.load(open('answer.json','r'))

intents = discord.Intents.all()
bot = commands.Bot(settings['prefix'], intents=intents)

botWork = bool()

@bot.event
async def on_ready():
    global botWork
    botWork = True
    bot.loop.create_task(reminderSending())
    print('Бот запущен! Клиент бота: {0.user}'.format(bot))
    return

@bot.command(name = 'пинг')
async def _ping(ctx):
    msgAuthor = ctx.message.author
    await ctx.send(f'Понг, {msgAuthor.mention}!')
    return

@bot.command(name = 'версия')
async def _ver(ctx):
    await ctx.send('Версия бота:')
    await ctx.send(settings['botVersion'])
    return

@bot.command(name = 'повтори')
async def _repeted(ctx, *args):
    temp = list(args)
    if temp == []: # if list empy, then warn
        await ctx.send('**ОШИБКА** Я не могу повторить пустоту твоего разума')
        return
    
    temp = str(' '.join(map(''.join,args)))
    await ctx.send(temp)
    return

@bot.command(name = 'ответь')
async def _reply(ctx, *args):
    if ctx.author == bot.user:
        return
    
    msgAuthor = ctx.message.author
    msgUser = str(''.join(map(''.join,args)))
    msgUser = preparKey(msgUser)
    if answer.get(msgUser) != None:
        await ctx.send(answer.get(msgUser))
    else:
        await ctx.send(f'{msgAuthor.mention}, в моём словаре не найденно ответа, прости')
    return

@bot.command(name = 'запомни')
async def _train(ctx, arg1, arg2):
    if (ctx.message.channel.id == settings['techChannel'] or
        ctx.message.author.id == settings['idLords']): # if no techCanel or no lords then ignore
        cmd = preparKey(arg1) # command
        rpl = arg2 # reply
        msgAuthor = ctx.message.author
        
        if answer.get(cmd) != None: # if the command is already there, then warn
            await ctx.send(f'{msgAuthor.mention}, **в моём словаре уже найден ответ!...**\n *Значение будет перезаписанно...*')
        
        json.dump(answer, open('answerBACKUP.json','w'))
        answer.update({cmd: rpl}) # update answer from {command: reply}
        json.dump(answer, open('answer.json','w'))
        await ctx.send(f'{msgAuthor.mention}, **Готово!\nСловарь успешно обновлён!**')
        await ctx.message.add_reaction('✅')
        return
    else:
        await ctx.send('**ОТКАЗАНО В ДОСТУПЕ** Простите, но данная комманда не доступна вам ):')
        return

@bot.command(name = 'замени')
async def _repace(ctx, arg1, arg2):
    if (ctx.message.channel.id == settings['techChannel'] or
        ctx.message.author.id == settings['idLords']): # if no techCanel or no lords then ignore
        cmd = arg1 # command
        rpr = preparKey(arg2) # repair
        msgAuthor = ctx.message.author
        
        if answer.get(cmd) == None:
            await ctx.send(f'{msgAuthor.mention}, **ОШИБКА** В моём словаре не найденно введённого вами ключа. Проверьте правильность ввода')
            return
        elif cmd == rpr:
            await ctx.send(f'{msgAuthor.mention}, **ОШИБКА** Ты ввёл одинаковые значения! Я так не играю')
            return
        
        json.dump(answer, open('answerBACKUP.json','w'))
        temp = answer.pop(cmd)
        answer.update({rpr: temp})
        json.dump(answer, open('answer.json','w'))
        await ctx.send(f'{msgAuthor.mention}, **Готово!\nКлюч словаря успешно заменён**')
        await ctx.message.add_reaction('✅')
        return
    else:
        await ctx.send('**ОТКАЗАНО В ДОСТУПЕ** Простите, но данная комманда не доступна вам ):')
        return

@bot.command(name = 'копия')
async def _backup(ctx):
    if (ctx.message.channel.id == settings['techChannel'] or
        ctx.message.author.id == settings['idLords']): # if no techCanel or no lords then ignore
        msgAuthor = ctx.message.author
        
        json.dump(answer, open('answerBACKUP.json','w'))
        await ctx.message.add_reaction('✅')
        await ctx.send(f'{msgAuthor.mention}, **Готово!**\nРезервная копия словаря созданна (предыдущая копия удалена)')
        return
    else:
        await ctx.send('**ОТКАЗАНО В ДОСТУПЕ** Простите, но данная комманда не доступна вам ):')
        return

@bot.command(name = 'восстановить')
async def _repair(ctx):
    if (ctx.message.channel.id == settings['techChannel'] or
        ctx.message.author.id == settings['idLords']): # if no techCanel or no lords then ignore
        msgAuthor = ctx.message.author
        answer = json.load(open('answerBACKUP.json','r'))
        json.dump(answer, open('answer.json','w'))
        await ctx.message.add_reaction('✅')
        await ctx.send(f'{msgAuthor.mention}, **Готово!**\nРезервная копия словаря восстановлена')
        return
    else:
        await ctx.send('**ОТКАЗАНО В ДОСТУПЕ** Простите, но данная комманда не доступна вам ):')
        return

@bot.command(name = 'реши')
async def _example(ctx, arg):
    msgAuthor = ctx.message.author
    if arg.isalpha() == True: # if in message alpha, then warn
        await ctx.send(f'{msgAuthor.mention}, **ОШИБКА**\nКак я тебе букавки решу? Я тут вам не ЕГЭ решаю')
        return
    await ctx.send(eval(arg))
    return

@bot.command(name = 'кнб')
async def _stoneScissorsPaper(ctx, arg):
    msgAuthor = ctx.message.author
    if arg.isalpha() != True:
        await ctx.send(f'{msgAuthor.mention}, **ОШИБКА**\nДавай по новой, Миша. Всё @#%№&')
        return
    
    ssp1 = arg.lower()
    
    if (arg == 'камень') or (arg == 'к'): ssp1 = 1 # ssp1 - stone scissors paper human
    elif (arg == 'ножницы') or (arg == 'н'): ssp1 = 2
    elif (arg == 'бумага') or (arg == 'б'): ssp1 = 3
    
    ssp2 = (random.randint(1,3)) # ssp2 - stone scissors paper robot
    if ssp2 == ssp1:
        await ctx.send(f'{msgAuthor.mention}, ого) у меня тоже) Ничья, но ты не расслабляйся)\n\nВсё равно победю ヽ(⌐■_■)ノ♪♬')
        return
    if ssp2 == 1: await ctx.send('У меня камень')
    elif ssp2 == 2: await ctx.send('У меня ножницы')
    elif ssp2 == 3: await ctx.send('У меня бумага')
    
    if (ssp1 == 1 and ssp2 == 2) or (ssp1 == 2 and ssp2 == 3) or (ssp1 == 3 and ssp2 == 1):
        await ctx.send(f'{msgAuthor.mention}, **НУ И ЛАДНО**.\n\nПобеда не главное ヽ(⌐■_■)ノ♪♬')
    else:
        await ctx.send(f'{msgAuthor.mention}, я победил ( ͡° ͜ʖ ͡°)>⌐■-■')
    return

@bot.command(name = 'дн')
async def _yesOrNo(ctx):
    if random.randint(0,6) > 3:
        await ctx.send('Да')
    else:
        await ctx.send('Нет')
    return

@bot.command(name = 'монетка')
async def _coin(ctx):
    temp = random.randint(0,6)
    if temp > 3 and temp != 7:
        await ctx.send('Решка')
    elif temp == 7:
        await ctx.send('**ОЙ** монетку спиздил кот...')
        await ctx.send('https://tenor.com/Ft1N.gif')
    else:
        await ctx.send('Орёл')
    return

@bot.command(name = 'ттс')
async def _textToSpeach(ctx, *args):
    temp = list(args)
    if temp == []: # if list empy, then warn
        await ctx.send('**ОШИБКА** Вы не ввели ни одного аргумента комманды')
        return
    
    msgUser = temp[0]
    
    if msgUser == 'помощь':
        await ctx.message.author.send('**Как озвучить сообщение?**\n**Оформление:**\nбот.ттс "сообщение" <голос>\n**Список голосов:**')
        await ctx.message.author.send(str(' '.join(map(''.join,voiceList))))
        await ctx.message.author.send('**Голос по умолчанию (сменить нельзя):**')
        await ctx.message.author.send(settings['defalutVoice'])
        await ctx.send('Отправил инструкцию тебе в ЛС :white_check_mark:')
        return
    
    temp.reverse()
    setVoice = str(temp[0])
    nameFile = msgUser[0:((len(msgUser))//3):1]
    nameFile = translit(nameFile) + '_tts.mp3'
    if setVoice in voiceList: say(setVoice, msgUser, nameFile)
    else: setVoice = str(settings['defalutVoice']); say(setVoice, msgUser, nameFile)
    
    await ctx.send(file=discord.File(nameFile))
    return

@bot.command(name = 'помоги')
async def _help(ctx):
    txt = open('help\\Help.txt','r', encoding = 'UTF-8')
    temp = ''
    for line in txt:
        temp = temp + line
    await ctx.message.author.send(temp)
    await ctx.send('Отправил тебе в ЛС :white_check_mark:')
    return

@bot.command(name = 'напомни')
async def _newReminder(ctx, *args):
    if list(args) == []:
        await ctx.send('**ОШИБКА** Вы не ввели ни одного аргумента комманды')
        return
    
    if args[0] == 'помощь':
        txt = open('help\\Remind Help.txt','r', encoding = 'UTF-8')
        temp = str()
        for line in txt:
            temp = temp + line
        await ctx.message.author.send(temp)
        await ctx.send('Отправил инструкцию тебе в ЛС :white_check_mark:')
        return
    
    msgAuthor = ctx.message.author.id
    if saveReminder(msgAuthor, args) == True:
        await ctx.send('**УСПЕХ :white_check_mark:** Ваше напоминание успешно созданно!')
    else: await ctx.send('**ОШИБКА** Вероятно вы не правильно сформировали запрос или превышен лимит времени \n`Введите <бот.напомни помошь> для получения справки`')

@tasks.loop(seconds = 5.0)
async def reminderSending():
    global botWork
    if botWork != True: # if bot not started, then ignore
        print('Бот не успел включиться! Пропускаю проверку напоминаний...')
        return
    
    remind = json.load(open('remind.json', 'r'))
    temp = time() 
    remindKey = list(remind.keys()) # call all reminder dates
    event = 0
    
    for i in remindKey:
        if (str(i)).isalpha() == True:
            continue
        if temp - float(i) > 0: # search for the first issued reminder
            print('Найдено напоминание! Запускаю отправку!')
            event = i
            break
    else: return
    
    temp = remind.pop(event) # remove this event from the list
    json.dump(remind, open('remind.json', 'w')) # writing a new dictionary
    
    remindAuthor = str() # for the future
    remindMsg = str() # for the future
    author = True
    for i in temp: # getting the user id and his message from the event
        if (i != '%') and (author == True):
            remindAuthor = remindAuthor + i
        else:
            author = False
        if (author == False) and (i != '%'):
            remindMsg = remindMsg + i
    remindChannel = bot.get_user(int(remindAuthor))
    await remindChannel.send('Привет :wave:! Тебе пришло напоминание:')
    await remindChannel.send(remindMsg)
    return

reminderSending.start()

bot.run(settings['token'])
