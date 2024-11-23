import os
from pico2d import *
from Singleton import Singleton

class ResourceMgr(metaclass=Singleton):
    def __init__(self):
        self.resources = {}

    def __call__(self, key):
        return self.resources.get(key, None)

    def load(self):
        for fileName in os.listdir("./resource"):
            self.resources[os.path.splitext(fileName)[0]] = load_image("resource/" + fileName)

        for fileName in os.listdir("./sound"):
            sound = load_wav("sound/" + fileName)
            sound.set_volume(32)
            self.resources[os.path.splitext(fileName)[0]] = sound

resource = ResourceMgr()