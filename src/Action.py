#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

class Action:
    def __init__(self, sourceBottleN: int, destinationBottleN: int, quantity: int):
        self.sourceBottleN = sourceBottleN
        self.destinationBottleN = destinationBottleN
        self.quantity = quantity

    def getSourceBottleN(self):
        return self.sourceBottleN

    def getDestinationBottleN(self):
        return self.destinationBottleN

    def getQuantity(self):
        return self.quantity
