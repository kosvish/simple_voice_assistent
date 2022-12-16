# Простой голосовой ассистент на питоне

> Как однажды _Пабло Пикассо_ сказал: "Вдохновение, когда оно приходит ко мне, застает меня за работой."
---
>А теперь можно приступать к написанию самого ассистента 
---

### Для начала, какие библеотки мне понадобились:


| Название библиотеки |     Команда для установки     |             Предназначение |
|:--------------------|:-----------------------------:|---------------------------:|
| Google              |      pip install google       |     Поисковые запросы гугл |
| SpeechRecognition   | pip install SpeechRecognition |         Распознование речи |
| pyttsx3             |      pip install pyttsx3      |        Оффлайн синтез речи |
| PyAudio             |      pip install PyAudio      |   Возможность записи аудио |

---

____Теперь импорты следующих пакетов библиотек которые будут использованы в будущем:____
````
import random                   # Для случайного выбора фразы нашего ассистента
import traceback                # Во избежании ошибок 
import webbrowser               # Для открытия браузера(который стоит по умолчанию)
from googlesearch import search # Сам поиск по гуглу
import pyttsx3                  # Синтезатор речи
import speech_recognition       # Распознование речи 
import os                       # Для работы с файлами
````
----
### Создадим следующие переменные в нашем main condition:
```
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = 'Alice'
    assistant.sex = 'female'
    assistant.speech_language = 'ru'
```
----
### Теперь создадим класс нашего голосового Ассистента с рядом переменных для его настройки:
```
class VoiceAssistant:
    name = ''
    sex = ''
    speech_language = ''
    recognition_language = ''

```
---

### Создадим основной функционал для записи , распознования  и проигрования голоса:

____Настройка голоса нашего ассистента____
``` 
def setup_assistant_voice():

    voices = ttsEngine.getProperty('voices')

    if assistant.speech_language == 'en':
        assistant.recognition_language = 'en-US'
        if assistant.sex == 'female':
            ttsEngine.setProperty('voice', voices[1].id)
        else:
            ttsEngine.setProperty('voice', voices[2].id)

    else:
        assistant.recognition_language = 'ru-RU'
        ttsEngine.setProperty('voice', voices[0].id)
```

> _Индексы голоса могут отличаться в зависимости от ОП на компьютере_



____Прогирование речи выглядит следующим образом:____

_На вход данная функция принимает речь пользователя и преобразовывает в str-строку_

````
def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

````
____Сама функция для записи и распознования аудио:____

```
def record_and_recognize_audio(*args: tuple):
 
    with microphone:
        recognized_data = ""

        # регулирование уровня шума окружаюшего мира(опционально)
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print('Слушаю...')
            audio = recognizer.listen(microphone, 5, 5)

            with open('microphone-results.wav', 'wb') as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print('Не могли бы вы проверить, включен ли ваш микрофон?')
            traceback.print_exc()
            return

        # Использование онлайн-распознание через Гугл
        try:
            print('Распознование началось...')
            recognized_data = recognizer.recognize_google(audio, language=assistant.recognition_language).lower()

        except speech_recognition.UnknownValueError:
            print('Проверьте пожалуйта ваше соединение с интернетом')

        return recognized_data
```
> Для записи голоса, я использовал создание временного _wav_ файла
----
## Мы закончили с функционалом для распознания речи пользователя

---
### Теперь создадим ряд объектов:
* _функцию для обработки команд_
* _hashe-tuple словарь где будут храниться будущие команды_
* _саму команду_
* _и дополним наш main condition бесконечным циклом_

____Функция для обработки команд выглядит следующим образом:____
```
def execute_command_with_name(command_name: str, *args: list):
   
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            print('Команда не найдена')
```
> На вход программа принимает:
> * 1: Первое (ключевое слово)  для  определения чего хочет пользователь
> * 2: И аргументы после ключего слова, которые будут переданны в саму функцию которая будет иполнять команду
>  
> Далее вложенным циклом проходимся по ключям запроса нашего пользователя для вывзова команды 

____Hash-tuple словарь где будут храниться будущие команды:____

```
commands = {
    ('привет', 'здравствуй', 'доброе утро'): play_greetings,
}
```

____Первая команда, она же функция приветсвия:____
```
def play_greetings(*args: tuple):

    greetings = [
        'Привет! Чем я могу помочь?',
        'Рада  снова тебя видеть! Чем я могу помочь?'
    ]
    play_voice_assistant_speech(greetings[random.randint(0, len(greetings) - 1)])
    
```
> Модулем random выбираем случайную приветсвенную фразу

____Бесконечный цикл в main condition:____
```
 while True:
        # старт записи речи с последующим выводом распознанной речи и удалением записанного в микрофон аудио
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(voice_input)

        # отделение комманд от дополнительной информации (аргументов)
        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)
```
# Вывод
> Ассистента можно улучшать множеством команд (добавлять в словарь) и дополнять различными функциями, но в своём проекте
> я показал лишь основы по его созданию.
