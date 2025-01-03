import argparse
import pprint

from analyze_with_gemini2 import Analyzer_With_GenAI
from analyze_with_librosa import AudioAnalyzer
from analyze_with_mutagen import Analyzer_With_Mutagen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE_PATH")
    parse = parser.parse_args()

    FILE_PATH = parse.FILE_PATH

    analyzed = AudioAnalyzer(file_path=FILE_PATH).analyze_technical_features()

    mutagenized = Analyzer_With_Mutagen(FILE_PATH).analyze()

    geminized = Analyzer_With_GenAI(FILE_PATH).analyze(
        refference=(analyzed | mutagenized)
    )

    all_data = analyzed | geminized | mutagenized

    pprint.pprint(all_data)
    if all_data["error"] == True:
        print("エラーです！")


main()
