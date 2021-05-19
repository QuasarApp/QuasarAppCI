# This Python file uses the following encoding: utf-8
import json
from pathlib import Path


class SecretManager:

    def __init__(self, jsFile, properties=None):
        contents = Path(jsFile).read_text()
        self.jsfile = json.loads(contents)
        self.prop = properties

    def getValue(self, key):
        value = self.jsfile[key]

        if self.prop:
            self.prop.useSecret(value, key)

        return value

    def convertToCmakeDefines(self):
        defines = []
        for key in self.jsfile:
            defines += '-D' + key + '=' + str(self.jsfile[key])

        return defines
