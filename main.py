import speech_recognition
import wave  # Создание и чтение аудиофайлов формата wav
import json  # работа с json файлами и строками
import os  # Работа с файловой системой


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


if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        voice_input = record_and_recognize_audio()
        # Удаление записанного в микрофон аудио
        os.remove('microphone-results.wav')
        print(voice_input)

