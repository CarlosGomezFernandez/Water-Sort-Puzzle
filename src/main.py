#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import constants
from Liquid import Liquid
from Bottle import Bottle
from Node import Node

import json
import copy
import hashlib
from typing import List
from os import remove
from pathlib import Path
from queue import PriorityQueue

problemID = 0
initState = 0
bottleList = []
boundary = PriorityQueue()
nodesCreated = []
visitedNodesHashes = []
lastNode = None
totalBottles = 0
strategy = constants.STRATEGY_DEPTH

# Lectura del JSON.
def readJson(jsonReaded: str) -> int:
    try:
        jsonDic = json.loads(jsonReaded)
    except Exception as err:
        return -1
    i = 0
    for bottleReaded in jsonDic:
        bottleList.append(Bottle(i, bottleReaded))
        i = i+1
    return 0

# Impresion de un estado.
def printFormattedState(bottleList: list) -> None:
    i = 0
    for botella in bottleList:
        print("Botella " + str(i))
        for liq in botella.contenido:
            print("Color: " + str(liq.getColor()) + " Cant: " + str(liq.getQuantity()))
        i = i+1

# Comprobacion de si la accion es posible o no.
def checkActionPosible(source: Bottle, dest: Bottle, qtty: int) -> bool:
    if ((source.getSpaceTaken() < qtty) or (dest.getFreeSpace() < qtty) or (source.getId() == dest.getId()) or (qtty < 0)):
        return False
    else:
        return True

# Comprobacion de si la accion es valida o no.
def checkActionValid(source: Bottle, dest: Bottle) -> bool:
    if ((source.getSpaceTaken() > 0) and (dest.getSpaceTaken() == 0 or source.getLiquidtoDrain().getColor() == dest.getLiquidtoDrain().getColor()) and (dest.getFreeSpace() >= source.getLiquidtoDrain().getQuantity())):
        return True
    else:
        return False

# Realizacion de la accion posible.
def doAction(source: Bottle, dest: Bottle, qtty: int) -> None:
    while(qtty > 0):
        if (source.getLiquidtoDrain().getQuantity() <= qtty): #Vertemos el liquido entero
            dest.fillLiquid(source.getLiquidtoDrain())
            qtty -= source.getLiquidtoDrain().getQuantity()
            source.drainLiquid(source.getLiquidtoDrain().getQuantity())
        else: #Vertemos una parte del liquido
            dest.fillLiquid(Liquid(source.getLiquidtoDrain().getColor(), qtty)) 
            source.drainLiquid(qtty)
            qtty = 0

# Comprobacion de si el sucesor es posible y valido o no.
def checkSuccessor(source: Bottle, dest: Bottle) -> bool:
    if (checkActionValid(source, dest) and checkActionPosible(source, dest, source.getLiquidtoDrain().getQuantity())):
        return True
    else:
        return False

# Realizacion de la accion valida.
def doValidAction(source: Bottle, dest: Bottle) -> int:
    qtty = source.getLiquidtoDrain().getQuantity()
    doAction(source, dest, qtty)
    return qtty

# Obtencion de la lista de sucesores.
def getSuccessorList(stateBottleList: list) -> list:
    successorList = []
    actionList = []
    for i in range(len(stateBottleList)):
        for j in range(len(stateBottleList)):
            if checkSuccessor(stateBottleList[i], stateBottleList[j]):
                successorList.append(copy.deepcopy(stateBottleList))
                actionList.append((i, j, doValidAction(successorList[-1][i], successorList[-1][j])))
    return successorList, actionList

# Comprobacion de si el estado es objetivo o no.
def isStateObjetive(stateBottleList: list) -> bool:
    for bottle in stateBottleList:
        if bottle.getLiquidCount() > 1 or (bottle.getLiquidCount() == 1 and bottle.getFreeSpace() != 0):
            return False
    return True

# Lectura del fichero de texto donde se encuentra el problema
def readProblemToJson() -> None:
    Path(constants.PERSISTENCE_FOLDER).mkdir(parents=True, exist_ok=True)
    with open(constants.PERSISTENCE_FOLDER + "Nivel.json", "r") as i:
        myJson = json.load(i)
        global problemID
        global initState
        problemID = myJson["id"]
        constants.BOTTLE_MAX_CONTENT = int(myJson["bottleSize"])
        initState = (str(myJson["initState"])).replace(' ','')

# Escritura del problema en un fichero de texto 
def writeProblemToJson(id: str, bottleSize: int, initState: list) -> None:
    data = {}
    data['id'] = id
    data['bottleSize'] = str(bottleSize)
    data['initState'] = []
    for bottle in initState:
        data['initState'].append(bottle.toJsonList())
    Path(constants.PERSISTENCE_FOLDER).mkdir(parents=True, exist_ok=True)
    with open(constants.PERSISTENCE_FOLDER + id + '.json', 'w') as outJsonFile:
        json.dump(data, outJsonFile)

# Codificador de estados mediante la función hash MD5
def stateEncoder(state: str, p=False) -> str:
    stateEncoded = (hashlib.md5(state.encode())).hexdigest()
    if p:
        print(stateEncoded)
    return stateEncoded

# Calculo de la heuristica del nodo
def heuristic(states: list) -> float:
    topColorList = []
    heuristic = 0
    for bottle in states:
        heuristic += bottle.getLiquidCount()
        if bottle.getSpaceTaken() == 0:
            heuristic += 1
        else:
            if (not bottle.getLiquidtoDrain().getColor() in topColorList):
                topColorList.append(bottle.getLiquidtoDrain().getColor())
            else:
                heuristic += 1
    heuristic = heuristic - totalBottles
    return heuristic

# Calculo del valor del nodo en funcion de la estrategia seleccionada
def calculateValue(depth: int, cost: int, heur: float) -> float:
    value = 0
    if strategy == constants.STRATEGY_BREADTH:
        value = depth
    elif strategy == constants.STRATEGY_DEPTH:
        value = 1/(depth+1)
    elif strategy == constants.STRATEGY_UNIFORM:
        value = cost
    elif strategy == constants.STRATEGY_GREEDY:
        value = heur
    elif strategy == constants.STRATEGY_A:
        value = cost + heur
    return value

# Creacion de nodos
def createNode(parent: Node, lastNode: Node, successor: list, action: tuple) -> Node:
    heur = heuristic(successor)
    if (parent == None):
        return Node(0, successor, None, None, 0, heur, calculateValue(0,0,heur))
    else:
        depth = parent.getDepth() + 1
        cost = parent.getCost() + 1
        return Node(cost, successor, parent.getID(), action, depth, heur, calculateValue(depth, cost, heur))

# Expandir los nodos creados
def expandNode(nodeToExpand: Node) -> None:
    global lastNode
    stateJson = []
    if(isStateObjetive(nodeToExpand.getState())):
        lastNode = nodeToExpand
        return True
    if(isNodeVisited(nodeToExpand)):
        return False
    if(nodeToExpand.getID() == 395):
        print("Espera")
    for bottle in nodeToExpand.getState():
        stateJson.append(bottle.toJsonList())
    visitedNodesHashes.append(stateEncoder(str(stateJson).replace(' ','')))
    successorList, actionList = getSuccessorList(nodeToExpand.getState())
    for i in range(len(successorList)):
        lastNode = createNode(nodeToExpand, lastNode, successorList[i], actionList[i])
        nodesCreated.append(lastNode)
        boundary.put(lastNode)
    return False

# Comprobar si el nodo ya ha sido visitado
def isNodeVisited(nodo: Node) -> bool:
    stateJson = []
    global actualNodeHash
    for bottle in nodo.getState():
        stateJson.append(bottle.toJsonList())
    actualNodeHash = stateEncoder(str(stateJson).replace(' ',''))
    return actualNodeHash in visitedNodesHashes

# Buscar nodo por su identificador
def findNodeById(id: int) -> Node:
    if id == None:
        return None
    else:
        for n in nodesCreated:
            if n.getID() == id:
                return n
    return None

# Imprimir en el fichero de texto la solucion del problema
def printSolution():
    global lastNode
    solutionPath = []
    Path(constants.SOLUTION_FOLDER).mkdir(parents=True, exist_ok=True)
    file = open(constants.SOLUTION_FOLDER + problemID + '_' + strategy.capitalize() +'.txt', 'w')
    while lastNode != None:
        stateJson = []
        for bottle in lastNode.getState():
            stateJson.append(bottle.toJsonList())
        solutionPath.append("[" + str(lastNode.getID()) + "][" + '{:.1f}'.format(round(lastNode.getCost(),1)) + "," + stateEncoder(str(stateJson).replace(' ','')) + "," + str(lastNode.getParentID()) + "," + str(lastNode.getAction()) + "," + str(lastNode.getDepth()) + "," + '{:.2f}'.format(round(lastNode.getHeuristic(),2)) + "," + '{:.2f}'.format((round(lastNode.getValue(),2))) + "]")
        lastNode = findNodeById(lastNode.getParentID())
    for solution in reversed(solutionPath):
        file.write(solution + '\n')
    file.close()

# Programa principal.
if __name__ == "__main__":

    # Lectura del fichero
    readProblemToJson()    
    # Codificacion del estado
    stateEncoder(initState)

    # Lectura del estado
    if (readJson(initState) == -1):
        print("Json introducido erroneo. Saliendo...")
        exit(1)

    # Obtener la cantidad total de botellas del problema
    totalBottles = len(bottleList)

    # Creacion del nodo raiz
    lastNode = createNode(None, None, bottleList, None)

    # Aniadir el nodo raiz a la frontera
    boundary.put(lastNode)
    nodesCreated.append(lastNode)

    # Obtencion de la lista de sucesores
    solutionFound = False
    print("Expanding", end='', flush=True)
    while (not solutionFound):
        print(".",end='', flush=True)
        solutionFound = expandNode(boundary.get())
    print("\n\nSolution found\n")

    for i in nodesCreated:
        if (i.getParentID()==395):
            print(i.getID())
        else:
            pass
        
    # Escritura en el fichero
    writeProblemToJson(problemID, constants.BOTTLE_MAX_CONTENT, bottleList)

    # Imprimir en el fichero de texto la solucion al problema
    printSolution()