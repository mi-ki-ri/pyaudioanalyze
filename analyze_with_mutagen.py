from mutagen.easyid3 import EasyID3
import argparse


class Analyzer_With_Mutagen:
    def __init__(self, file_path: str):
        self.FILE_PATH = file_path

    def analyze(self):
        audio_items = print_mp3_tags(self.FILE_PATH)
        if audio_items is None:
            return {"error": True}
        return {
            "error": False,
            "audio_items": audio_items,
        }


def print_mp3_tags(file_path):
    """
    MP3ファイルからすべてのタグ情報を読み取り、表示します。

    Args:
      file_path: MP3ファイルのパス
    """
    try:
        audio = EasyID3(file_path)
        return audio.items()
    except Exception as e:
        print(f"エラー: {e}")


# MP3ファイルのパスを指定してください
parser = argparse.ArgumentParser()
parser.add_argument("FILE_PATH")
parse = parser.parse_args()

print_mp3_tags(parse.FILE_PATH)
