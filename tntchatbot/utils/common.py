# Copyright (c) TNeuron Technology
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

from enum import Enum

import hashlib

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