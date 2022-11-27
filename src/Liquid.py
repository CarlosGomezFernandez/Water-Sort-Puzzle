#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

class Liquid:

    def __init__(self, color: int, quantity: int):
        self.color = color
        self.quantity = quantity

    def getColor(self) -> int:
        return self.color

    def getQuantity(self) -> int:
        return self.quantity

    def setColor(self, color: int) -> None:
        self.color = color

    def setQuantity(self, quantity: int) -> None:
        self.quantity = quantity

    def drain(self, qtty: int) -> None:
        self.quantity -= qtty

    def fill(self, qtty: int) -> None:
        self.quantity += qtty

    def toJsonList(self) -> list:
        return [self.color, self.quantity]

if __name__ == "__main__":
    print("Error: Este archivo no deberia ser ejecutado por separado")
    exit(1)