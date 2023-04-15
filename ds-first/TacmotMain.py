import discord, json, random

from discord.ext import commands, tasks
from time import time
from config import settings, voiceList
from TechModule import say, translit, preparKey, saveReminder

answer = json.load(open('json\\answer.json','r'))
remind = json.load(open('json\\remind.json', 'r'))
print('Запуск бота. Словарь загружен. Ключи словаря: ', answer.keys())

intents = discord.Intents.all()
bot = commands.Bot(settings['prefix'], intents=intents)

botWork = bool()

@bot.event
async def on_ready():
    global botWork
    botWork = True
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
    temp = str(' '.join(map(''.join,args))) # list to str
    await ctx.send(temp)
    return

@bot.command(name = 'ответь')
async def _reply(ctx, *args):
    msgUser = preparKey(str(''.join(map(''.join,args)))) # list args to str key
    temp = answer.get(msgUser)
    if temp != None:
        await ctx.send(temp)
    else:
        msgAuthor = ctx.message.author
        await ctx.send(f'{msgAuthor.mention}, в моём словаре не найденно ответа, прости')
    return

@bot.command(name = 'запомни')
async def _train(ctx, arg1, arg2):
    if (ctx.message.channel.id == settings['techChannel'] or
            ctx.message.author.id == settings['idLords']): # if no techCanel or no lords then ignore
        json.dump(answer, open('json\\answerBACKUP.json','w')) # backup
        answer.update({preparKey(arg1): arg2}) # update answer from {command: reply}
        json.dump(answer, open('json\\answer.json','w')) # save new answer
        msgAuthor = ctx.message.author
        await ctx.send(f'{msgAuthor.mention}, **Готово!**\nСловарь успешно обновлён!')
        await ctx.message.add_reaction('✅')
        return
    else:
        await ctx.send('**ОТКАЗАНО В ДОСТУПЕ** Простите, но данная комманда не доступна вам ):')
        return

@bot.command(name = 'замени')
async def _repace(ctx, arg1, arg2):
    if (ctx.message.channel.id == settings['techChannel'] or
            ctx.message.author.id == settings['idLords']): # if no techCanel or no lords then ignore
        cmd = preparKey(arg1) # command
        rpr = preparKey(arg2) # repair
        msgAuthor = ctx.message.author
        if answer.get(cmd) == None:
            await ctx.send(f'{msgAuthor.mention}, **ОШИБКА** В моём словаре не найденно введённого вами ключа. Проверьте правильность ввода')
            return
        elif cmd == rpr:
            await ctx.send(f'{msgAuthor.mention}, **ОШИБКА** Ты ввёл одинаковые значения! Я так не играю')
            return
        json.dump(answer, open('json\\answerBACKUP.json','w')) # backup
        temp = answer.pop(cmd)
        answer.update({rpr: temp})
        json.dump(answer, open('json\\answer.json','w')) # save new answer
        await ctx.send(f'{msgAuthor.mention}, **Готово!**\nКлюч словаря успешно заменён')
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
        json.dump(answer, open('json\\answerBACKUP.json','w')) # backup
        await ctx.message.add_reaction('✅')
        await ctx.send(f'{msgAuthor.mention}, **Готово!**\nРезервная копия словаря созданна (предыдущая копия удалена)')
        return
    else:
        await ctx.send('**ОТКАЗАНО В ДОСТУПЕ** Простите, но данная комманда не доступна вам ):')
        return

@bot.command(name = 'восстановить')
async def _repair(ctx):
    global answer
    if (ctx.message.channel.id == settings['techChannel'] or
            ctx.message.author.id == settings['idLords']): # if no techCanel or no lords then ignore
        msgAuthor = ctx.message.author
        answer = json.load(open('json\\answerBACKUP.json','r')) # load backup
        json.dump(answer, open('json\\answer.json','w')) # save new answer
        await ctx.message.add_reaction('✅')
        await ctx.send(f'{msgAuthor.mention}, **Готово!**\nСловарь востановлен из резервной копии')
        return
    else:
        await ctx.send('**ОТКАЗАНО В ДОСТУПЕ** Простите, но данная комманда не доступна вам ):')
        return

@bot.command(name = 'реши')
async def _example(ctx, *args):
    msgAuthor = ctx.message.author
    arg = str(''.join(map(''.join,args)))
    if arg.isalpha() == True: # if in message alpha, then warn
        await ctx.send(f'{msgAuthor.mention}, **ОШИБКА**\nКак я тебе букавки решу? Я тут вам не ЕГЭ решаю')
        return
    await ctx.send(eval(arg))
    return

@bot.command(name = 'кнб')
async def _stoneScissorsPaper(ctx, *args):
    msgAuthor = ctx.message.author
    if len(args) == 0:
        await ctx.send(f'{msgAuthor.mention}, **ОШИБКА**\nЭй! Требую хотяб одного аргумента для команды')
        return
    temp = str(args[0]).lower()
    sspH = int() # sspH - id stone scissors paper human
    if (temp == 'камень') or (temp== 'к'): sspH = 1     # setting an id for a sign chosen by a
    elif (temp == 'ножницы') or (temp == 'н'): sspH = 2 # person (it's easier to analyze this way)
    elif (temp == 'бумага') or (temp == 'б'): sspH = 3
    else:
        await ctx.send(f'{msgAuthor.mention}, **ОШИБКА**\n Я не понял что ты имел ввиду')
        return # if the user wrote crap, then stop
    sspR = (random.randint(1,3)) # sspR - stone scissors paper robot
    if sspR == sspH:
        await ctx.send(f'{msgAuthor.mention}, ого) у меня тоже) Ничья, но ты не расслабляйся)\n\nВсё равно победю ヽ(⌐■_■)ノ♪♬')
        return
    if sspR == 1: await ctx.send('У меня камень')
    elif sspR == 2: await ctx.send('У меня ножницы')
    elif sspR == 3: await ctx.send('У меня бумага')
    if (sspH == 1 and sspR == 2) or (sspH == 2 and sspR == 3) or (sspH == 3 and sspR == 1):
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
async def _coin(ctx, *args):
    temp = random.randint(0,6)
    if len(args) < 2:
        if temp > 3 and temp != 7: await ctx.send('Решка'); return
        elif temp == 7:
            await ctx.send('**ОЙ** монетку спиздил кот...')
            await ctx.send('https://tenor.com/Ft1N.gif')
            return
        else: await ctx.send('Орёл'); return
    else:
        arg1 = args[0]
        arg2 = args[1]
        if temp > 3 and temp != 7: await ctx.send(arg1); return
        elif temp == 7:
            await ctx.send('**ОЙ** монетку спиздил кот...')
            await ctx.send('https://tenor.com/Ft1N.gif')
            return
        else: await ctx.send(arg2); return

@bot.command(name = 'ттс')
async def _textToSpeach(ctx, *args):
    temp = list(args)
    if temp == []: # if list empy, then warn
        await ctx.send('**ОШИБКА** Вы не ввели ни одного аргумента комманды')
        return
    if temp[0] == 'помощь':
        reply = ('**Как озвучить сообщение?**\n**Оформление:**\nбот.ттс <текс> < опционально голос>\n' +
                  '**Список голосов:\n**' + (str(', '.join(map(''.join,voiceList)))) +
                 '\n**Голос по умолчанию (сменить нельзя):\n**' + str(settings['defalutVoice']))
        await ctx.message.author.send(reply)
        await ctx.send('Отправил инструкцию тебе в ЛС :white_check_mark:')
        return
    temp.reverse() 
    setVoice = temp[0]
    if setVoice in voiceList: setVoice = temp.pop(0); temp.reverse() # checking the last argument for the presence 
    else: setVoice = str(settings['defalutVoice']); temp.reverse()   # of a voice setting and returning the normal list
    msgUser = str(' '.join(map(''.join,temp)))
    a = (len(msgUser))//3
    if a > 20: a = 20 # so that the file name is not too long
    nameFile = translit(msgUser[0:a:1]) + '_tts.mp3'
    say(setVoice, msgUser, nameFile) # dubbing
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
    global remind
    if len(args) == 0:
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
        remind = json.load(open('json\\remind.json', 'r'))
    else: await ctx.send('**ОШИБКА** Вероятно вы не правильно сформировали запрос или превышен лимит времени \n`Введите <бот.напомни помошь> для получения справки`')

@bot.command(name = 'число')
async def _randNum(ctx, *args):
    repl = ''
    minimum = 1
    maximum = 100
    if len(args) > 1:
        if args[0].isdigit() == True: minimum = int(args[0])
        else: repl = repl + '**Ах ты...** Минимальное не верно... Взято по умолчанию(1)...\n'
        if args[1].isdigit() == True: maximum = int(args[1])
        else: repl = repl + '**Ах ты..** Максимальное не верно... Взято по умолчанию(100)...\n'
        if minimum > maximum:
            repl = repl + '**Ну ты совсем...** Минимум > максимум... Меняю их местами...\n'
            temp = maximum; maximum = minimum; minimum = temp
    repl = repl + 'Я сгенерировал: ' + str(random.randint(minimum, maximum))
    await ctx.send(repl)

@tasks.loop(seconds = 5.0)
async def reminderSending():
    global botWork, remind
    if botWork != True: # if bot not started, then ignore
        print('Бот не успел включиться! Пропускаю проверку напоминаний...')
        return
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
    json.dump(remind, open('json\\remind.json', 'w')) # writing a new dictionary
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
    reply = (f'{remindChannel.mention}, привет :wave:! Тебе пришло напоминание!\n' +
             '\n:point_right: ' + remindMsg)
    await remindChannel.send(reply)
    return

reminderSending.start()

bot.run(settings['token'])
