import os
from pico2d import *
from Singleton import Singleton

class ResourceMgr(metaclass=Singleton):
    def __init__(self):
        self.resources = {}

    def __call__(self, key):
        return self.resources.get(key, None)

    def Load(self):
        for fileName in os.listdir("./resource"):
            self.resources[os.path.splitext(fileName)[0]] = load_image("resource/" + fileName)
