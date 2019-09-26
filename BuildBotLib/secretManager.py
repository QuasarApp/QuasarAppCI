# This Python file uses the following encoding: utf-8
import json
from pathlib import Path

class SecretManager:

    def __init__(self, jsFile):
        try:
            contents = Path(jsFile).read_text()
            self.jsfile = json.loads(contents)
        except:
            pass


    def getValue(self, key):
        try:
            return self.jsfile[key]
        except:
            pass
