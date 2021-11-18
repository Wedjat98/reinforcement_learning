#!/usr/local/bin python
# -*- coding:utf-8 -+-

import const
import random

class Field:
    def __init__(self,kind):
        self.reward = 0
        self.kind = kind

    def getr(self):
        return self.reward
    def setr(self, value):
        self.reward = value
    r = property(getr, setr)

    def getk(self):
        return self.kind
    def setk(self, value):
        self.kind = value
    k = property(getk, setk)


