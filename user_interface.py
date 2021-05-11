import argparse
import logging

from sympy import to_cnf, SympifyError

from beliefbase import Belief_Base, Belief
from entailment import entails
from contraction import contraction

def possible_actions():
    print(
    """Possible actions:
    addition(a): Add a belief to the Belief base
    check(ch): Check a formula for entailment
    contract(c): Belief contraction
    empty(e): Empty Belief base
    print(p): Print Belief base
    help(h): Print this help dialog
    quit(q): Quit"""
    )
    print("Please use sympy notation")


def user_input(KB):
    print("Please choose an action from action list: ")
    action = input().lower()

    while action != "quit":
        
        if action == 'add' or action == 'a':
            print()
            print('--- Addition ---')
            print('Enter a belief to add to the Belief base:')
            belief = input()
            try:
                print('(Optional) Please choose the order of your belief (real number from 0 to 1):')
                print('If None the order will be calcualted automatically')
                order = input()
                if not entails(KB.beliefs, belief):
                    KB.add_belief(Belief(belief,float(order)))
                else:
                    print('Belief is already entailed by the the Belief base')
            except SympifyError:
                print('Invalid formula')
            except ValueError:
                print('Order has to be a real number from 0 to 1')
            print()
        

        elif action == 'check' or action == 'ch':
            print()
            print('--- Checking entailment ---')
            print('Enter a formula to check:')
            formula = input()
            try:
                print(entails(KB.beliefs, formula))
            except SympifyError:
                print('Invalid formula')
            print()
        
        elif action == 'contract' or action == 'c':
            print()
            print('--- Contraction ---')
            print('Enter a formula to contract from the Belief base:')
            formula = input()
            try:
                new_KBb = contraction(KB.beliefs, formula)
                print("The new contracted Belief base: ", new_KBb)
                KB.beliefs = new_KBb
            except SympifyError:
                print('Invalid formula')
            print()

        elif action == 'empty' or action == 'e':
            KB.beliefs = []
            print()
            print('--- Belief base is now empty ---')
            print()

        elif action == 'print' or action == 'p':
            print()
            print('--- Print belief base ---')
            print(KB.beliefs)
            print()

        elif action == 'help' or action == 'h':
            possible_actions()
        
        else:
            print('Sorry, the command was not recognized.')
            print()

        possible_actions()
        print("Which other action do you want to execute?")
        action = input().lower()


if __name__ == '__main__':
    KB = Belief_Base()
    possible_actions()
    user_input(KB)