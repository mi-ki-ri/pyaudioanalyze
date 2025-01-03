import argparse
import pprint

from analyze_with_gemini2 import Analyzer_With_GenAI
from analyze_with_librosa import AudioAnalyzer
from analyze_with_mutagen import Analyzer_With_Mutagen

import pydub


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE_PATH")
    parse = parser.parse_args()

    FILE_PATH = parse.FILE_PATH

    if ".wav" in FILE_PATH:
        print("wavファイルです！ mp3に変換します！")
        sound = pydub.AudioSegment.from_wav(FILE_PATH)
        sound.export(FILE_PATH.replace(".wav", ".mp3"), format="mp3", bitrate="96k")
        FILE_PATH = FILE_PATH.replace(".wav", ".mp3")
    elif ".mp3" in FILE_PATH:
        print("mp3ファイルです！ ビットレートを96kに変換します！")
        sound = pydub.AudioSegment.from_mp3(FILE_PATH)
        sound.export(FILE_PATH, format="mp3", bitrate="96k")
    else:
        print("wavでもmp3でもありません！")
        return

    print("Librosaで解析します！")
    analyzed = AudioAnalyzer(file_path=FILE_PATH).analyze_technical_features()

    print("Mutagenで解析します！")
    mutagenized = Analyzer_With_Mutagen(FILE_PATH).analyze()

    print("GenAIで解析します！")
    geminized = Analyzer_With_GenAI(FILE_PATH).analyze(
        refference=(analyzed | mutagenized)
    )

    all_data = analyzed | geminized | mutagenized

    pprint.pprint(all_data)
    if all_data["error"] == True:
        print("エラーです！")


main()
