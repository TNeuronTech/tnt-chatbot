# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

import os

from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import AnalyzeDocumentChain

from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI as Pandasai_OpenAI
from pandasai.schemas.df_config import Config

from tntchatbot.config.settings import settings
from tntchatbot.logger.logger import logger

from youtube_transcript_api import YouTubeTranscriptApi


class Model:
    def __init__(self) -> None:
        self.textSplitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        pass

    def get_query_results(self, AI_API_KEY, prompt, history, session_id) -> str:
        index = Chroma(
            persist_directory=f"{settings.DB_LOCATION}/{session_id}", 
            embedding_function=OpenAIEmbeddings(openai_api_key=AI_API_KEY))
        
        # self.retrieval = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=OPENAI_API_KEY), chain_type="stuff", retriever=index.as_retriever())

        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(
                openai_api_key=AI_API_KEY,
                model_name=settings.LLM_NAME, 
                temperature=settings.TEMPERATURE),
            retriever=index.as_retriever(search_kwargs = {'k':10}), 
            verbose=True, 
            return_source_documents=True, 
            max_tokens_limit=1024,
            combine_docs_chain_kwargs={'prompt': PromptTemplate(template=settings.QA_TEMPLATE, input_variables=["context","question" ])})
        
        chain_input = {"question": prompt, "chat_history": history}
        # chain_input = {"question": prompt, "chat_history": []}
        response = chain(chain_input)
        logger.debug("api response {response}")
        return response['answer']

    def train_and_get_key(self, AI_API_KEY, key, data):
        
        texts = self.textSplitter.split_documents(data)
        db_embedding_path = f"{settings.DB_LOCATION}/{key}"
        # check if this document already exist in db
        if not os.path.exists(db_embedding_path):
            index = Chroma.from_documents(
                texts, 
                OpenAIEmbeddings(openai_api_key=AI_API_KEY), 
                persist_directory=db_embedding_path)
            index.persist()
    
        
    def get_video_query_results(self, AI_API_KEY, video_id) -> str:
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('en','fr','es', 'zh-cn', 'hi', 'ar', 'bn', 'ru', 'pt', 'sw' ))
        finalString = ""
        for item in transcript:
            text = item['text']
            finalString += text + " "
        
        texts = self.textSplitter.split_text(finalString)
        logger.debug(f"Video transcript {texts}")
        
        summary_chain = load_summarize_chain(OpenAI(temperature=settings.TEMPERATURE, openai_api_key=AI_API_KEY),
                                            chain_type="map_reduce",verbose=True)
            
        summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

        answer = summarize_document_chain.run(texts[0])
        logger.debug(f"api response {answer}")
        return answer
        
    def get_sheet_query_results(self, AI_API_KEY, df, prompt) -> str:
        
        # pandas_ai = PandasAI(
        #     llm=Pandasai_OpenAI(
        #     temperature=float(settings.TEMPERATURE),
        #     api_token=AI_API_KEY), 
        #     verbose=True)
        # answer = pandas_ai.run(data_frame = df, prompt=prompt)

        smartDataframe = SmartDataframe(
            df=df,
            config=Config(
                llm=Pandasai_OpenAI(
                    temperature=float(settings.TEMPERATURE),
                    api_token=AI_API_KEY
                    ),
                save_logs=False))
        
        answer = str(smartDataframe.chat(query=prompt))
        
        # logger.debug(f"type of response {type(answer)}")
        
        logger.debug(f"api response {answer}")
        return answer

    def train_chat_sheet_and_get_key(self, AI_API_KEY, key, data):
            
        texts = self.textSplitter.split_documents(data)
        
        db_embedding_path = f"{settings.DB_LOCATION}/{key}"
        # check if this document already exist in db
        if not os.path.exists(db_embedding_path):
            index = Chroma.from_documents(
                texts, 
                OpenAIEmbeddings(openai_api_key=AI_API_KEY), 
                persist_directory=db_embedding_path)
            index.persist()
    
ai_model = Model()


