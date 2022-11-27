#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

from Liquid import Liquid
import constants
import sys

class Bottle:
    
    def __init__(self, id: int, contenidoLista: list):
        self.id = id

        self.contenido = []
        for x in contenidoLista:
            if (len(x) != 2):
                print("Error: se esperaba [color, cantidad] en la informacion del json. Saliendo...")
                sys.exit(1)
            if (self.getSpaceTaken() + x[1] > constants.BOTTLE_MAX_CONTENT):
                print("Error: Se ha superado la capacidad maxima de la botella. Saliendo...")
                sys.exit(1)
            if x[1] >= 1:
                self.contenido.append(Liquid(int(x[0]), int(x[1])))
            else:
                print("Introducido numero negativo en el json. Saliendo...")
                sys.exit(1)

    def getId(self) -> int:
        return self.id

    def getLiquidtoDrain(self) -> Liquid:
        return self.contenido[0]

    def getSpaceTaken(self) -> int:
        actualContent = 0
        for l in self.contenido:
            actualContent += l.getQuantity()
        return actualContent

    def getFreeSpace(self) -> int:
        return constants.BOTTLE_MAX_CONTENT - self.getSpaceTaken()

    def drainLiquid(self, qtty: int) -> None:
        if self.contenido[0].getQuantity() < qtty:
            return None # Error
        elif self.contenido[0].getQuantity() == qtty:
            self.contenido.pop(0)
        else:
            self.contenido[0].drain(qtty)

    def fillLiquid(self, liquid: Liquid):
        if self.getFreeSpace() < liquid.getQuantity():
            return None # Error
        elif len(self.contenido) == 0:
            self.contenido.append(liquid)
        elif self.contenido[0].getColor() == liquid.getColor():
            self.contenido[0].fill(liquid.getQuantity())
        else:
            self.contenido.insert(0, liquid)

    def getLiquidCount(self) -> int:
        return len(self.contenido)

    def toJsonList(self) -> list:
        res = []
        for l in self.contenido:
            res.append(l.toJsonList())
        return res

if __name__ == "__main__":
    print("Error: Este archivo no deberia ser ejecutado por separado")
    exit(1)