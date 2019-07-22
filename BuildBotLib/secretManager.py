# This Python file uses the following encoding: utf-8
import json
from pathlib import Path

class SecretManager:

    def __init__(self, jsFile):
        contents = Path(jsFile).read_text()
        self.jsfile = json.loads(contents)

    def getValue(self, key):
        return self.jsfile[key]
