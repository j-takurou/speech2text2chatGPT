import os
import uvicorn
import requests
from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import TokenTextSplitter


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
    return subtitles_data


def get_subtitles(video_id):
    # XXX: 関数分割してLoaderとsummarizerのデバッグしやすいように
    # XXX: https://python.langchain.com/docs/integrations/document_loaders/youtube_transcript
    # langchainで実装可能...!
    # from: https://nikkie-ftnext.hatenablog.com/entry/how-easy-youtube-transcript-api-and-langchain-youtubeloader

    try:
        loader = (
            YoutubeLoader
            .from_youtube_url(
                f"https://www.youtube.com/watch?v={video_id}",
                language=["ja"]
            )
        )
        documents = loader.load()
        # Prepare LLM Chain
        text_splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=1000)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1.0)
        
        # Summarizer Chain
        summarize_chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            verbose=True
        )

        # Template Chain
        promptSubject = PromptTemplate(
            input_variables=["text"], 
            template="""\"\"\"{text}\"\"\"\上記のテーマのは以下の通り：\n\n* """)
        chainSubject = LLMChain(llm=llm, prompt=promptSubject)
        
        # Connect Chains
        overall_chain_map_reduce = SimpleSequentialChain(
            chains=[summarize_chain, chainSubject]
        )
        # Run Chains
        subject = overall_chain_map_reduce.run(
            text_splitter.create_documents([documents])
        )
        return subject
    except Exception as e:
        # エラーハンドリング - 通信エラーなどの例外が発生した場合
        return {"error": str(e)}


if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
