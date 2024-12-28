from mutagen.easyid3 import EasyID3
import argparse


def print_mp3_tags(file_path):
    """
    MP3ファイルからすべてのタグ情報を読み取り、表示します。

    Args:
      file_path: MP3ファイルのパス
    """
    try:
        audio = EasyID3(file_path)
        for tag, value in audio.items():
            print(f"{tag}: {value}")
    except Exception as e:
        print(f"エラー: {e}")


# MP3ファイルのパスを指定してください
parser = argparse.ArgumentParser()
parser.add_argument("FILE_PATH")
parse = parser.parse_args()

print_mp3_tags(parse.FILE_PATH)
