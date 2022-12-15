import random
import traceback
import webbrowser

import pyttsx3
import speech_recognition
import wave  # Создание и чтение аудиофайлов формата wav
import json  # работа с json файлами и строками
import os  # Работа с файловой системой


class VoiceAssistant:
    """
    Настройки голосового ассистента
    """
    name = ''
    sex = ''
    speech_language = ''
    recognition_language = ''


def setup_assistant_voice():
    """
    Установка голоса по умолчанию
    """
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


def play_voice_assistant_speech(text_to_speech):
    """
    Проигрование речи ответов ассистента
    :param text_to_speech: текст, который нужно преобразовать в реч
    """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознование аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня шума окружаюшего мира
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


def play_greetings(*args: tuple):
    """
    Проигрование случайной приветсвенной фразы
    """
    greetings = [
        'Привет! Чем я могу помочь?',
        'Рада  снова тебя видеть! Чем я могу помочь?'
    ]
    play_voice_assistant_speech(greetings[random.randint(0, len(greetings) - 1)])


def search_for_term_on_google(*args: tuple):
    """
    Поиск в Гугл с автоматическим открытием ссылок(если возможно)
    :param args:
    """
    if not args[0]: return
    search_term = ' '.join(args[0])

    # открытие ссылки на поисковик в бразуере
    url = 'https://google.com/search?q=' + search_term
    webbrowser.get().open(url)


def search_for_video_on_youtube(*args: tuple):
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])

    # открытие ссылки на поисковик в браузере
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)


def execute_command_with_name(command_name: str, *args: list):
    """
    Выполнение заданной пользователем команды с доп аргументами
    :param command_name: название команнды
    :param args: аргументы которые будут переданны в функцию
    """
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            print('Команда не найдена')


# перечень комманд в виде hashable-tuple словаря
commands = {
    ('привет', 'здравствуй', 'доброе утро'): play_greetings,
    ('видео', 'ютуб',): search_for_video_on_youtube,
    ('найди', 'поищи', 'гугл'): search_for_term_on_google,
}

if __name__ == "__main__":

    # инициализация интсрументов распознания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = 'Alice'
    assistant.sex = 'female'
    assistant.speech_language = 'ru'

    # установка голоса по умолчанию
    setup_assistant_voice()

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
