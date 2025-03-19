import speech_recognition as sr
import librosa
import soundfile as sf


def voice_to_text():
    audio_path = 'bot/files/audio.ogg'
    y, srr = librosa.load(audio_path, sr=None)
    sf.write('bot/files/audio.wav', y, srr)

    recognizer = sr.Recognizer()

    with sr.AudioFile("bot/files/audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(
                audio_data, language="ru-RU")
            print("Распознанный текст: ", text)
            return text
        except Exception:
            return 0


# voice_to_text()
