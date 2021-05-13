import itertools

from numpy.core.numerictypes import maximum_sctype
from sympy.logic.boolalg import to_cnf, Or, And
from entailment import entails, split
from beliefbase import Belief_Base, Belief
import numpy as np



# 1) implement the order (based on the complexity of the predicate, when it was added to the KB)

def contraction(KB, formula):
        KBb = KB.base
        comb = []
        for i in range(1,len(KB.beliefs)+1):
            comb += list(itertools.combinations(KB.beliefs, i))
        comb = [ list(c) for c in comb]
        new_KB = []
        for c in comb:
            comb_beliefs_f = []
            for b in c:
                comb_beliefs_f += split(b.formula, And)
            if not entails(comb_beliefs_f, formula):
                new_KB.append(c)
        max_l = max([len(c) for c in new_KB ])
        max_c = []
        for c in new_KB:
            if len(c) == max_l:
                max_c.append(c)
        result = list(set.intersection(*[set(c) for c in max_c]))
        if len(result) == 0:
            maximum = 0
            out = None
            for c in max_c:
                if sum(c) >= maximum:
                    out = c
                    maximum = sum(c)
            return out   #list(set(max_c[0]).union(*set(max_c[1:])))
        return result #list of beliefs
        
def revision(KB,belief):
    formula = belief.formula
    KBb = contraction(KB, ~formula)
    #KBb.append(belief)
    return KBb

        
def bi_imp(p,q):
    return p + ">>" + q + "&" + q + ">>" + p 

if __name__ == '__main__':
    KB = Belief_Base()
    default = ["p", "q", "p | q", "p & q","p>>q"]
    for f in default:
        KB.add_belief(Belief(f,1))
    KB = contraction(KB, "q")
    print("NEW CONTRACTED KB 1: ", KB)
    
    print("\n sentence 2: \n")
    KB = Belief_Base()
    default =  ["p", "p | q", "p & q" , bi_imp("p","q")]
    for f in default:
        KB.add_belief(Belief(f,1))
    KB = contraction(KB, "p")
    print("NEW CONTRACTED KB 2: ", KB)

