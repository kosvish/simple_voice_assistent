import random
import webbrowser

import pyttsx3
import speech_recognition
import wave  # Создание и чтение аудиофайлов формата wav
import json  # работа с json файлами и строками
import os  # Работа с файловой системой
# Машинное обучение
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC


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
            return

        # Использование онлайн-распознание через Гугл
        try:
            print('Распознование началось...')
            recognized_data = recognizer.recognize_google(audio, language='ru').lower()

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


def search_for_video_on_youtube(*args: tuple):
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    play_voice_assistant_speech("Here is what I found on youtube")


def prepare_corpus():
    """
    Подготовка модели для угадывания намерений пользователя
    """
    corpus = []
    target_vector = []
    for intent_name, intent_data in config['intents'].items():
        for example in intent_data['examples']:
            corpus.append(example)
            target_vector.append(intent_name)

    training_vector = vectorizer.fit_transform(corpus)
    classifier_probability.fit(training_vector, target_vector)
    classifier.fit(training_vector, target_vector)


def get_intent(request):
    """
    Получение наиболее вероятного намерения пользователя в зависимости от запроса пользователя
    :param request: запрос пользователя
    :return: наиболее вероятное намерение
    """
    best_intent = classifier.predict(vectorizer.transform([request]))[0]

    index_of_best_intent = list(classifier_probability.classes_).index(best_intent)
    probabilities = classifier_probability.predict_proba(vectorizer.transform([request]))[0]

    best_intent_probability = probabilities[index_of_best_intent]

    # При добавлении новых намерений стоит уменьшать этот показатель
    print(best_intent_probability)
    if best_intent_probability > 0.157:
        return best_intent


def make_preparations():
    """
    Подготовка глобальных переменных к запуску приложения
    """
    global recognizer, microphone, ttsEngine, assistant, vectorizer, classifier_probability, classifier

    # инициализация интсрумента распознования
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация интсрумента речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = 'Alice'
    assistant.sex = 'female'
    assistant.speech_language = 'ru'

    # установка голоса по умолчанию
    setup_assistant_voice()

    # Подготовка корпуса для распознование запросов пользователя с некоторой верятностью
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
    classifier_probability = LogisticRegression()
    classifier = LinearSVC()
    prepare_corpus()


config = {
    'intents': {
        'greeting': {
            'examples': ['привет', 'здравствуй', 'ку',
                         'hello', 'good morning'],
            'responses': play_greetings
        },
        'youtube_search': {
            'examples': ['найди видео', 'покажи видео',
                         'find video', 'find on youtube'],
            'responses': search_for_video_on_youtube
        }
    }
}

if __name__ == "__main__":
    make_preparations()

    while True:
        # Старт записи речи с последующим выводом распознаной речи и удалением записанного в микрофон
        voice_input = record_and_recognize_audio()
        if os.path.exists('microphone-results.wav'):
            os.remove('microphone-results.wav')

        print(voice_input)

        # отделение команд от дополнительной информации
        if voice_input:
            voice_input_parts = voice_input.split(' ')

            # если было сказано одно слово - выполняем команду сразу без доп аргументов
            if len(voice_input_parts) == 1:
                intent = get_intent(voice_input)
                if intent:
                    config['intents'][intent]['responses']()
                else:
                    config['failure_phrases']()
