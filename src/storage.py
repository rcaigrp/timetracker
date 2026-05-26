import json
import os

class LocalStorage:
    '''Simulates chrome.storage.local for testing and persistence logic.'''
    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.get(key)

    def set(self, key, value):
        self._data[key] = value

    def remove(self, key):
        if key in self._data:
            del self._data[key]

    def clear(self):
        self._data.clear()
