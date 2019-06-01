#!/usr/bin/env python
# coding: utf-8
"""
Project:  nvwa
Title:    wumpus 
Author:   Liuyl 
DateTime: 2014/10/14 14:08 
UpdateLog:
1、Liuyl 2014/10/14 Create this File.

wumpus
>>> print("No Test")
No Test
"""
__author__ = 'Liuyl'
# -*- coding: utf-8 -*-

import random
def affichemenu():
    b = True
    while b:
        print"Choisissez le niveau de difficulte"
        print"niveau 1 : pour les nuls"
        print"niveau 2 : pour les moins nuls"
        print"niveau 3 : pour les bons"
        print u"niveau 4 : pour les expérimentés"
        niveau = raw_input()
        if niveau.isdigit():
            if int(niveau) == 1 or int(niveau) == 2 or int(niveau) == 3 or int(niveau) == 4:
                vie = 0
                life = 1
                b = False
    return int(niveau)

def avance(salle):
    b = True
    print "Vous êtes dans la salle",salle,"."
    if salle in [laby[numerowumpus][0],laby[numerowumpus][1],laby[numerowumpus][2]]:
        print "GRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR!!!!!!!!!!!!!!!!"
        print"Le wumpus grogne, il n'est pas loin!"
        print u"Il est même dans une des salles adjacentes a la vôäéèöütre!"
    print "Les salles adjacentes sont:",laby[salle][0],",",laby[salle][1],"et",laby[salle][2],"."
    while b:
        print "Tapez 0 pour tirer ou le numéro de la salle dans laquelle vous voulez aller."
        rep = raw_input()
        if rep.isdigit():
            if int(rep) in laby[salle][:-1]:
                b = False
                vie = 1
                life = 1
                salle = int(rep)
            if int(rep) == 0:
                vie,life = flecheoui(rep)
                b = False
    return salle,vie,life

def flecheoui(rep):
    b = True
    print"Dans quelle numéro de salle voulez-vous la tirer?"
    while b:
        print 'Choisissez une salle.'
        salle2 = raw_input()
        if salle2.isdigit():
            if int(salle2) == numerowumpus:
                print "VOUS AVEZ GAGNE! LE WUMPUS EST MORT!!!!!!"
                print"Voulez-vous recommencer le jeu? "
                vie,life = reponse()
                b = False
                salle2 = 0
            if int(salle2) in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
                print"Vous avez raté le wumpus.C'est fini.....Vous êtes mort!Il était dans la salle", numerowumpus, ","
                print"Voulez-vous recommencer le jeu?"
                vie,life = reponse()
                b = False
    return vie,life

def piegeenXpuits():
        print "Ahhhhhhhhhhhhh, vous êtes tombé dans un puits sans fonds."
        print"Voulez-vous recommencer la partie? "
        vie,life = reponse()
        return vie,life

def piegenXportail(salle):
       salle = random.randrange(1,21,1)
       print " Vous êtes automatiquement redirigé dans la salle",salle
       return salle

def reponse():
    b = True
    while b:
        print "Tapez 1 pour recommencer et 0 pour arrêter le jeu."
        rep = raw_input()
        if rep.isdigit():
            if int(rep) == 1:
                vie = 0
                life = 1
                b = False
            if int(rep) == 0:
                print "the END!"
                vie = 0
                life = 0
                b = False
    return vie,life

if __name__ == '__main__':
#Programme principal :
    print"Bonjour, vous êtes un chasseur de Wumpus."
    print"Après avoir choisi votre niveau de difficulté, vous serez parachuté dans un labyrinthe de vingt salles dans lequel le Wumpus se trouve.Ce dernier hiberne, il ne se déplacera donc jamais.\n Vous, en revanche, vous pouvez vous déplacer dans une des trois salles adjacentes à la votre afin de le traquer.Une fois dans une salle, vous pouvez décider de tirer une flèche magique dans n’importe quelle salle du labyrinthe.\n Si elle est tirée dans la salle du wumpus, vous gagnez !! Sinon, vous mourez. Si vous entrez dans la salle du Wumpus, il vous mangera  et vous mourrez.\n Si vous êtes dans une salle adjacente au Wumpus, vous l’entendrez grogner. \n Mais attention, certaines salles contiennent des pièges. Vous tomberez peut être sur un puits auquel cas vous mourrez, ou sur un portail qui vous transportera  aléatoirement dans une salle."
    print"Nous vous souhaitons bonne chance, et bonne partie !"
    print""

    life = 1
    while life == 1:
        laby = [[0,0,0,0],[5,12,14,0],[8,10,19,0],[18,11,7,0],[8,17,13,0],[9,1,13,0],[11,9,14,0],[3,14,15,0],[16,4,2,0],[6,5,17,0],[2,18,15,0],[6,3,20,0],[15,1,19,0],[19,5,4,0],[1,6,7,0],[10,12,7,0],[20,8,18,0],[20,4,9,0],[16,10,3,0],[2,12,13,0],[16,17,11,0]]
        vie = 1
        niveau = affichemenu()

        for i in range(1,niveau+1):
            x = random.randrange(1,21,1)
            while laby[x][3]!= 0:
                x = random.randrange(1,21,1)
            laby[x][3] = random.choice([30,40])#puits = 30 et portail = chauve souris = 40
        salle = random.randrange(1,21,1)
        while laby[salle][3]!= 0:
            salle = random.randrange(1,21,1)
        laby[salle][3] = 50
        numerowumpus = random.randrange(1,21,1)
        while laby[numerowumpus][3]!= 0:
            numerowumpus = random.randrange(1,21,1)
        while vie == 1:
            salle,vie,life = avance(salle)
            if laby[salle][3] == 30:
                vie,life =piegeenXpuits()
            if laby[salle][3] == 40:
                salle = piegenXportail(salle)
            if salle == numerowumpus:
                print" Le wumpus vous a mangé!!!! gnark, gnark, gnark!"
                print"Voulez vous recommencerle jeu?"
                vie,life =reponse()
