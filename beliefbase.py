#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 20:46:23 2021

@author: sara
"""
from sympy.logic.boolalg import to_cnf, Or, And
from entailment import split
import math

class Belief_Base:
    
    def __init__(self): 
        self.beliefs = []
        
    def add_belief(self, belief): 
        self.beliefs += belief.formula
    
    
class Belief:
    
    def __init__(self, formula, order = None):
        self.formula = split(to_cnf(formula),And)
        self.order = order
    def __repr__(self):
        return f'Belief: {self.formula}, Order: {self.order}'


if __name__ == '__main__':
    
    formula = [Belief("p"), Belief("q"), Belief("p | q"), Belief("p & q"), Belief("p>>q>>r&t&p")]

    bb= Belief_Base()
    for f in formula:
        bb.add_belief(f)
    print(bb.beliefs)
