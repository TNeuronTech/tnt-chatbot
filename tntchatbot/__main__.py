# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

import uvicorn
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from tntchatbot.router import modelrouter
import os


# add end points
# package and deploy BE to server and query from internet
# how to optimize the results



app = FastAPI(
    title="tntchatbot",
    description="APIs for chatbot",
    version="1.0.0",
)

app.include_router(modelrouter.router)

if __name__ == "__main__":  
     uvicorn.run(app, host="0.0.0.0", port=8000)