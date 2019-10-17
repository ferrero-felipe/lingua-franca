import sounddevice as sd
import soundfile as sf
sd.default.device = 'PCH'

def record(sr=44100, duration=5):
    print('Starting recording...')
    myrecording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
    sd.wait()
    sf.write('../data/test.ogg', myrecording, sr)
    print('Done!')
    return myrecording, sr

def play(audio,sr=44100):
    print('Playing...')
    sd.stop()
    sd.play(audio, sr)