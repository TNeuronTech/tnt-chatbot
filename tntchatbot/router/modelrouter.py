# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

from fastapi import APIRouter, status, File, UploadFile, Header

from tntchatbot.schemas import schema
from tntchatbot.api import api
from tntchatbot.logger.logger import logger

router = APIRouter(tags=["AI-Model"], prefix="/model")

@router.post("/predict", status_code=status.HTTP_200_OK, response_model=schema.PredictResp)
async def predict(request: schema.PredictReq, AI_API_KEY: str = Header()):
    #logger.debug(f"/predict request {AI_API_KEY}")
    response = api.query_model(request, AI_API_KEY)
    logger.debug(f"/predict response {response}")
    return response

@router.post("/train", status_code=status.HTTP_201_CREATED, response_model=schema.TrainResp)
async def train(request: schema.TrainReq, AI_API_KEY: str = Header()):
    logger.debug(f"/train request {request}")
    response = api.train_model(request, AI_API_KEY)
    logger.debug(f"/train response {response}")
    return response

@router.post("/sheet/predict", status_code=status.HTTP_200_OK, response_model=schema.PredictSheetResp)
async def predict(request: schema.PredictSheetReq, AI_API_KEY: str = Header()):
    response = api.query_sheet_model(request, AI_API_KEY)
    logger.debug(f"/sheet/predict response {response}")
    return response