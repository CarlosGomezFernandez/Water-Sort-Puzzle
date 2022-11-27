#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

from typing import List

class Node:
    id = -1
    def __init__(self, cost: int, state: list, parentID: int, action: tuple, depth: int, heuristic: float, value: float):
        Node.id = Node.id+1
        self.id = Node.id
        self.cost = cost
        self.state = state
        self.parentID = parentID
        self.action = action
        self.depth = depth
        self.heuristic = heuristic
        self.value = value

    def __lt__(self, other):
        selfPriority = (self.value, self.id)
        otherPriority = (other.value, other.id)
        return selfPriority < otherPriority
    
    def getID(self) -> int:
        return self.id

    def getCost(self) -> int:
        return self.cost

    def getState(self) -> list:
        return self.state
    
    def getDepth(self) -> int:
        return self.depth
    
    def getHeuristic(self) -> float:
        return self.heuristic
    
    def getValue(self) -> float:
        return self.value

    def getParentID(self) -> int:
        return self.parentID

    def getAction(self) -> tuple:
        return self.action

    def setID(self, id: int) -> None:
        self.id = id

    def setCost(self, cost: int) -> None:
        self.cost = cost

    def setState(self, state: list) -> None:
        self.state = state
    
    def setDepth(self, depth: int) -> None:
        self.depth = depth
    
    def setHeuristic(self, heuristic: float) -> None:
        self.heuristic = heuristic
    
    def setValue(self, value: int) -> None:
        self.value = value

if __name__ == "__main__":
    print("Error: Este archivo no deberia ser ejecutado por separado")
    exit(1)