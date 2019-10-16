from pydub import AudioSegment
from functions import getFiles, splitFile
import os

def main():
    """Cuts mp3 audio files in ../data/audio/ into 5 seconds files"""
    for lang in os.listdir('../data/audio/'):
        print('Spliting {}'.format(lang))
        for file in getFiles('../data/audio/{}'.format(lang)):
            audio = AudioSegment.from_mp3(file)
            for chunks,i in splitFile(audio):
                if not os.path.exists("../data/samples/{0}".format(lang)):
                    os.makedirs("../data/samples/{0}".format(lang))
                chunks.export("../data/samples/{0}/{0}_{1}_{2}.mp3".format(lang,file[-6:-4],i), format="mp3")

if __name__ == "__main__":
    main()