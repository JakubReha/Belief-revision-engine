import argparse
import logging

from sympy import to_cnf, SympifyError, And, Or

from beliefbase import Belief_Base, Belief
from entailment import entails,split
from contraction import contraction, revision

def possible_actions():
    print(
    """Possible actions:
    addition(a): Add a belief to the Belief base
    check(ch): Check a formula for entailment
    contract(c): Belief contraction
    revise(r): Revise the Belief base with a formula
    empty(e): Empty Belief base
    print(p): Print Belief base
    help(h): Print this help dialog
    quit(q): Quit"""
    )
    print("Please use sympy notation")


def user_input(KB):

    print("Default Belief base: ",KB.base)

    print("Please choose an action from action list: ")
    action = input().lower()

    while True:
        if action == "quit" or action == "q":
            break
        
        elif action == 'add' or action == 'a':
            print()
            print('--- Addition ---')
            print('Enter a belief to add to the Belief base:')
            belief = input()
            try:
                print('(Optional) Please enter the entrenchment of your belief (from 0 to 1):')
                print('If None the entrenchment will be calcualted automatically')
                entrenchment = input()
                if entails(KB.base, belief):
                    print('Belief is already entailed by the the Belief base')
                elif entails(KB.base, "~("+belief+")"):
                    print('Belief is in contradicition with the Belief base')
                else:
                    if entrenchment:
                        KB.add_belief(Belief(belief,float(entrenchment)))
                    else:
                        KB.add_belief(Belief(belief,None))
                print("The new Belief base: ", KB.base)
            except SympifyError:
                print('Invalid formula')
            except ValueError:
                print('entrenchment has to be between 0 to 1')
            print()
        

        elif action == 'check' or action == 'ch':
            print()
            print('--- Checking entailment ---')
            print('Enter a formula to check:')
            formula = input()
            try:
                print(entails(KB.base, formula))
            except SympifyError:
                print('Invalid formula')
            print()
        
        elif action == 'contract' or action == 'c':
            print()
            print('--- Contraction ---')
            print('Enter a formula to contract from the Belief base:')
            formula = input()
            try:
                new_KBb = contraction(KB, formula)
                KB= Belief_Base()
                for f in new_KBb:
                    KB.add_belief(f)
                print("The new contracted Belief base: ", KB.base)
            except SympifyError:
                print('Invalid formula')
            print()

        elif action == 'empty' or action == 'e':
            KB = Belief_Base()
            print()
            print('--- Belief base is now empty ---')
            print()


        elif action == 'revision' or action == 'r':
            print()
            print('Enter a formula to revise the Belief base:')
            formula = input()
            print('(Optional) Please enter the entrenchment of your belief (from 0 to 1):')
            print('If None the entrenchment will be calculated automatically')
            entrenchment = input()
            try:
                if entrenchment:
                    belief = Belief(formula,float(entrenchment))
                else:
                    belief = Belief(formula,None)
                KBb = contraction(KB, "~"+formula)
                KB.beliefs = KBb
                KB.add_belief(belief)

                KB.base = []
                for b in KB.beliefs:
                    KB.base += split(to_cnf(b.formula), And)
                    KB.base = list(set(KB.base))


                print("The new revised Belief base: ", KB.base)
            except SympifyError:
                print('Invalid formula')
            print()

        elif action == 'print' or action == 'p':
            print()
            print('--- Print belief base together with the entrenchment of beliefs---')
            print(KB.beliefs)
            print()

        elif action == 'help' or action == 'h':
            possible_actions()
        
        else:
            print('Wrong command. Please try again.')
            print()

        possible_actions()
        print("Which other action do you want to execute?")
        action = input().lower()


if __name__ == '__main__':
    KB = Belief_Base()
    default = ["p", "q", "p | q", "p & q","p>>q"]
    for f in default:
        KB.add_belief(Belief(f,1))
    possible_actions()
    user_input(KB)