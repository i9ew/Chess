import os  # работа с файловой системой
from functions import *
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)


class Microphone:
    def __init__(self, funcs):
        self.funcs = funcs
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.rep = {
            "hot": "ход",
            "вход": "ход"
        }
        if __name__ == "__main__":
            self.path = "microphone-results.wav"
        else:
            self.path = create_full_path("/temp/microphone-results.wav")

    def record_and_recognize_audio(self, *args: tuple):
        """
        Запись и распознавание аудио
        """
        with self.microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=1)

            try:
                print("Starting listening...")
                audio = self.recognizer.listen(self.microphone, 5, 5)

                with open(self.path, "wb") as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                # print("Can you check if your microphone is on, please?")
                return

            # использование online-распознавания через Google
            try:
                # print("Started recognition...")
                recognized_data = self.recognizer.recognize_google(audio, language="ru-RU").lower()

            except speech_recognition.UnknownValueError:
                pass

            # в случае проблем с доступом в Интернет происходит попытка
            # использовать offline-распознавание через Vosk
            except speech_recognition.RequestError:
                print("No internet")

            return recognized_data

    def clear_string(self, string, k):
        s = list(map(lambda x: x.strip(), string.strip().split()))
        s = list(filter(lambda x: x != k, s))
        ans = []
        sl = {
            "жэ": "g",
            "е": "e"
        }
        for i in s:
            f1 = False
            for j in i:
                if j.isdigit():
                    f1 = True

            if f1 or len(i) <= 2:
                try:
                    ans.append(sl[i])
                except KeyError:
                    ans.append(i)

            else:
                ans.append(i)

        return " ".join(ans)

    def extract_move(self, string):
        s = list(map(lambda x: x.strip(), string.strip().split()))
        ans = []
        for i in s:
            for j in i:
                if j.isdigit():
                    ans.append(i)
                    break
        ans = "".join(ans)
        if list(map(lambda x: x.isdigit(), list(ans))) == [0, 1, 0, 1] and len(ans) == 4:
            return "".join(ans)
        else:
            pass

    def update(self):
        voice_input = self.record_and_recognize_audio()
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass

        try:
            for i in self.rep:
                voice_input = voice_input.replace(i, self.rep[i])

            if voice_input:
                print(f'Recorded: "{voice_input}"')

            for i in self.funcs.keys():
                if i.lower() in voice_input:
                    cleared = self.clear_string(voice_input, i.lower())
                    extracted = self.extract_move(cleared)
                    if extracted:
                        print(f'Move: "{extracted}"')
                        self.funcs[i](extracted)
        except TypeError:
            pass
        except AttributeError:
            pass


# m = Microphone({"команда": lambda x: print("move", x)})
# while True:
#     m.update()
