# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

from pydantic import BaseModel

class ChatHistory(BaseModel):
    question: str
    asnwer: str

class PredictReq(BaseModel):
    prompt: str
    history: list[tuple[str,str]]
    session_id: str
    data_type: int

class PredictSheetReq(BaseModel):
    prompt: str
    data: str
    data_type: int

class PredictSheetResp(BaseModel):
    result: str
    agent_thoughts: str

class PredictResp(BaseModel):
    result: str
    agent_thoughts: str

class TrainReq(BaseModel):    
    data: str
    data_type: int

class TrainResp(BaseModel):
    key: str