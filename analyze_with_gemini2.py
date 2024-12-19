import json
import os
from google import genai
from google.genai import types
from pydantic import BaseModel


class SongInfo(BaseModel):
    tags: list[str]
    jenre: str
    instruments: list[str]
    liner_notes: str
    tempo_feel: str
    associated_words: list[str]
    associated_color: str


class Analyzer_With_GenAI:
    def __init__(self, file_path: str):
        self.FILE_PATH = file_path
        self.API_KEY = os.environ.get("GOOGLE_API_KEY")

    def analyze(self):
        client = genai.Client(api_key=self.API_KEY)
        myfile = client.files.upload(path=self.FILE_PATH)

        uri = myfile.uri
        mime = myfile.mime_type
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Part.from_uri(uri, mime),
                types.Part.from_text(
                    "この曲のジャンル、タグなどの情報をJSON形式で書き出してみてほしい。タグと連想単語は10個程度ほしい。"
                ),
                types.Part.from_text(
                    """例: {
              instruments: ['エレキギター','シンセベース'], 
              jenre: "ネオソウル",  
              tags: [ネオソウル, チルアウト, ローファイ, ギター, スローテンポ, シャッフルビート, 16フィール, インストゥルメンタル],
              tempo_feel: "スロー",
              liner_notes: "この作品には素晴らしく情感のこもったギターと美しい音色があります。"
              associated_words: ["夜", "星空", "冬", "夜明け", "煙草"],
              associated_color: "deep blue"
              }
            """
                ),
            ],
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=SongInfo,
            ),
        )

        loaded = json.loads(response.text)
        return loaded
