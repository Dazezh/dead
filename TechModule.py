import pyttsx3
import json

from time import time

trans = {
    'а': 'a', 'б': 'b', 'в': 'v',
    'г': 'g', 'д': 'd', 'е': 'e',
    'ё': 'jo', 'ж': 'zh', 'з': 'z',
    'и': 'i', 'й': '', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r',
    'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'c',
    'ч': 'ch', 'ш': 'sh', 'щ': 'shh',
    'ъ': '', 'ы': 'y', 'ь': '',
    'э': 'je', 'ю': 'ju', 'я': 'ja',
    ' ': '_'
    } # rus to eng translit

signs = [
    '!', '(', ')', '-', ';', '?', '@', '#',
    '$', '%', ':', '"', "'", ' ', ',', '.',
    '/', '^', '&', ';', '*', '_', '[', ']',
    '{', '}'
    ]

def translit(*args):
    temp = str(args[0])
    temp = temp.lower()
    temp2 = ''
    for i in temp:
        if i in signs: continue
        else: temp2 = temp2 + trans[i]
    return temp2

def say(setVoice, msgUser, nameFile):
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    for voice in voices: # set TTS voice
        if voice.name == setVoice:
            tts.setProperty('voice', voice.id)
    
    tts.save_to_file(msgUser, nameFile)
    
    tts.runAndWait()

def preparKey(arg):
    temp = str(''.join(map(''.join,arg)))
    temp = temp.lower()
    temp2 = ''
    for i in temp:
        if i in signs: continue
        else: temp2 = temp2 + i
    return temp2

def saveReminder(*args):
    if len(args) < 2: return None
    
    temp = list(args[1])
    msgAuthor = args[0]
    when = temp.pop(0)
    when2 = temp.pop(0)
    when2 = when2.lower()
    msgUser = str(' '.join(map(''.join,temp)))
    
    if when.isdigit == False: # if the user entered not a number, then exit
        return None
    else:
        when = float(when)
    if when2.isalpha == False: # if the user entered not a word, then exit
        return None
    
    if (when2 == 'м' or when2 == 'минут' or
    when2 == 'минута' or when2 == 'минуты'):
        when = when * 60
    elif when2 == 'ч' or when2 == 'часов' or when2 == 'час':
        when = when * 60 * 60
    elif when2 == 'д' or when2 == 'дня' or when2 == 'день':
        when = when * 24 * 60 * 60
    else: return None
    
    if when > 172800: # if the limit (2 day) is exceeded - stop
        return None
    else:
        when = time() + when
    
    temp = str(msgAuthor) + '%' + msgUser
    remind = json.load(open('remind.json', 'r'))
    remind.update({when: temp})
    json.dump(remind, open('remind.json', 'w'))
    return True