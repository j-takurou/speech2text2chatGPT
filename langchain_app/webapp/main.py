import os
import uvicorn
import requests
from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Welcome to YouTube Subtitles API"}


@app.get("/get_subtitles_summary/{video_id}")
def get_subtitles_summary(video_id: str):
    # YouTube APIを使用して字幕情報を取得
    subtitles_data = get_subtitles(video_id)
    print(subtitles_data)
    
    # langchainモジュールとLLMを使用して要約
    summarized_data = summarize_subtitles(subtitles_data)
    
    return summarized_data


def get_subtitles(video_id):
    # XXX: https://python.langchain.com/docs/integrations/document_loaders/youtube_transcript
    # langchainで実装可能...!
    # from: https://nikkie-ftnext.hatenablog.com/entry/how-easy-youtube-transcript-api-and-langchain-youtubeloader

    try:
        transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=["ja"])
        concat_text = "".join(map(lambda dic: dic["text"], transcripts))
        # apply summarize_subtitles
        # Write Code
        return concat_text
    except Exception as e:
        # エラーハンドリング - 通信エラーなどの例外が発生した場合
        return {"error": str(e)}


def summarize_subtitles(subtitles_data):
    # langchainモジュールとLLMを使用して字幕情報を要約するロジックを実装
    # サンプルコードでは省略しています
    return "sample"


if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
