# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    LLM_NAME: str = "gpt-3.5-turbo"
    TEMPERATURE: str = "0.5"
    DB_LOCATION: str = "data"
    QA_TEMPLATE: str = """
        You are a helpful AI assistant. The user gives you a file its content is represented by the following pieces of context, use them to answer the question at the end.
        If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
        Use as much detail as possible when responding.

        context: {context}
        =========
        question: {question}
        ======
        """

    # log configuration
    LOG_FILE_NAME: str =  "logs/app_{time}.log"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILTER: str = None
    LOG_ROTATION: str = "100 MB"
    LOG_RETENTION: str = "2 days"
    LOG_FORMAT: str = "{time} {level} {name}:{function}:{line} {message}"

    pass


path = Path(__file__).parent.parent.absolute()
settings = Settings(_env_file=path.joinpath(".env"), _env_file_encoding="utf-8")