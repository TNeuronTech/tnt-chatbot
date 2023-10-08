# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

from enum import Enum

import hashlib
import re

class DataType(int, Enum):
    PDF = 1
    TEXT = 2
    CSV = 3
    EXCEL = 4
    VIDEO = 5


def generate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return str(sha256.hexdigest())

def agent_thought_cleanup(captured_output):
    thoughts = captured_output.getvalue()
    cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
    return re.sub(r'\[1m>', '', cleaned_thoughts)