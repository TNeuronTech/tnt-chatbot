# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

import base64

import pandas as pd

from tempfile import NamedTemporaryFile

from tntchatbot.schemas import schema
from tntchatbot.models.model import ai_model
from tntchatbot.utils.common import DataType
from tntchatbot.logger.logger import logger
from tntchatbot.utils import common

from langchain.document_loaders import PyPDFLoader, CSVLoader, TextLoader

from fastapi import HTTPException


def query_model(request: schema.PredictReq, AI_API_KEY):
    
    if(request.data_type in [DataType.VIDEO]):
        logger.debug("video file format")
        return {"result": ai_model.get_video_query_results(AI_API_KEY, request.prompt)}

    elif(request.data_type in [DataType.PDF, DataType.CSV, DataType.TEXT]):
        logger.debug("pdf, CSV or TEXT file format")
        return {"result": ai_model.get_query_results(AI_API_KEY, request.prompt, request.history, request.session_id)}
    
    else:
       raise HTTPException(status_code=400, detail="Invalid file type")


def train_model(request: schema.TrainReq, AI_API_KEY):

    if(request.data_type in [DataType.PDF]):
        logger.debug(f"PDF file format")

        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(base64.b64decode(request.data.encode('utf-8')))
            temp_file.seek(0)
            temp_file_path = temp_file.name
            loader = PyPDFLoader(temp_file_path)
            data = loader.load()
        
        key = common.generate_hash(request.data.encode('utf-8'))
        
        ai_model.train_and_get_key(AI_API_KEY, key, data)

        return {"key": key}
    elif(request.data_type in [DataType.TEXT]):
        logger.debug("TEXT file format")

        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(base64.b64decode(request.data.encode('utf-8')))
            temp_file.seek(0)
            temp_file_path = temp_file.name
            loader = TextLoader(temp_file_path)
            data = loader.load()
        
        key = common.generate_hash(request.data.encode('utf-8'))
        
        ai_model.train_and_get_key(AI_API_KEY, key, data)

        return {"key": key}
    elif(request.data_type in [DataType.CSV, DataType.EXCEL]):
        logger.debug("excel file format")

        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(base64.b64decode(request.data.encode('utf-8')))
            temp_file.seek(0)
            temp_file_path = temp_file.name
            loader = CSVLoader(temp_file_path)
            data = loader.load()

        key = common.generate_hash(request.data.encode('utf-8'))

        ai_model.train_chat_sheet_and_get_key(AI_API_KEY, key, data)

        return {"key": key}
        
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")


def query_sheet_model(request: schema.PredictSheetReq, AI_API_KEY):
    
    if(request.data_type in [DataType.CSV]):

        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(base64.b64decode(request.data.encode('utf-8')))
            temp_file.seek(0)
            temp_file_path = temp_file.name
            df = pd.read_csv(temp_file_path)

        return {"result": ai_model.get_sheet_query_results(AI_API_KEY, df, request.prompt)}

    elif(request.data_type in [DataType.EXCEL]):
        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(base64.b64decode(request.data.encode('utf-8')))
            temp_file.seek(0)
            temp_file_path = temp_file.name
            df = pd.read_excel(temp_file_path)

        return {"result": ai_model.get_sheet_query_results(AI_API_KEY, df, request.prompt)}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")

    