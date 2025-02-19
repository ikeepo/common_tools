import argparse
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import os
from vosk import Model, KaldiRecognizer
import json


# 将音频文件转换为WAV格式（支持MP3和M4A）
def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_file = audio_file.rsplit('.', 1)[0] + '.wav'
    audio.export(wav_file, format="wav")
    return wav_file


# 使用SpeechRecognition库的Google Web Speech API
def transcribe_speech_recognition(wav_file, language="auto"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)

    try:
        print(f"Transcribing with SpeechRecognition (Language: {language})...")
        if language == "auto":
            language = "zh-CN"  # 默认中文
        text = recognizer.recognize_google(audio, language=language)
        return text
    except Exception as e:
        print(f"SpeechRecognition error: {e}")
        return None


# 使用Whisper模型
def transcribe_whisper(wav_file, language="auto", model_type="base"):
    print(f"Transcribing with Whisper ({model_type} model, Language: {language})...")
    model = whisper.load_model(model_type)

    # 自动检测语言或使用指定语言
    if language == "auto":
        result = model.transcribe(wav_file)
    else:
        result = model.transcribe(wav_file, language=language)

    return result["text"]


# 使用Vosk模型
def transcribe_vosk(wav_file, language="auto"):
    print("Transcribing with Vosk...")
    model_path = f"model/{language}"  # 根据语言选择模型路径
    if not os.path.exists(model_path):
        raise Exception(f"Vosk model not found for language: {language}. Please download and extract the Vosk model.")

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    with open(wav_file, "rb") as f:
        audio_data = f.read()
        if recognizer.AcceptWaveform(audio_data):
            result = json.loads(recognizer.Result())
            return result["text"]
        else:
            return None


# 主函数，选择模型并进行转录
def main(audio_file, model="speech_recognition", language="auto"):
    wav_file = convert_to_wav(audio_file)

    if model == "speech_recognition":
        text = transcribe_speech_recognition(wav_file, language)
    elif model == "whisper":
        text = transcribe_whisper(wav_file, language)
    elif model == "vosk":
        text = transcribe_vosk(wav_file, language)
    else:
        print("Invalid model selected.")
        return

    if text:
        print(f"Transcription:\n{text}")
    else:
        print("Could not transcribe the audio.")


# 命令行参数
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert audio to text using different models.")
    parser.add_argument("audio_file", help="Path to the audio file (MP3 or M4A)")
    parser.add_argument("--model", choices=["speech_recognition", "whisper", "vosk"], default="speech_recognition",
                        help="Model to use for transcription (default: speech_recognition)")
    parser.add_argument("--language", default="auto",
                        help="Language for transcription (default: auto-detect). Examples: 'en-US', 'zh-CN', 'ru-RU'")
    args = parser.parse_args()

    main(args.audio_file, args.model, args.language)

