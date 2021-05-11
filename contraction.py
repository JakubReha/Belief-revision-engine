import itertools
from sympy.logic.boolalg import to_cnf, Or, And
from entailment import entails
import numpy as np



# 1) implement the order (based on the complexity of the predicate, when it was added to the KB)

def contraction(KBb, formula):
        formula = to_cnf(formula)
        comb = []
        for i in range(1,len(KBb)+1):
            comb += list(itertools.combinations(KBb, i))

        new_KBb = []
        for c in comb:
            if not entails(list(c), formula):
                new_KBb.append(c)
        max_l = max([len(c) for c in new_KBb ])
        max_c = []
        for c in new_KBb:
            if len(c) == max_l:
                max_c.append(c)
        result = list(set(KBb).intersection(*set(max_c)))
        if len(result) == 0: 
            # TO DO !!!!!! if the intersection is None, return one of the remainder sets based on the order
            # for now returning UNION which is wrong
            return list(set(max_c[0]).union(*set(max_c[1:])))
        return result
        
def revision(KBb, formula):
    KBb = contraction(KBb, ~formula)
    KBb += to_cnf(formula)
    return KBb

        
def bi_imp(p,q):
    return p + ">>" + q + "&" + q + ">>" + p 

if __name__ == '__main__':
    
    formula1 = "p"
    formula2 = "q"
    formula3 = "p | q"
    formula4 = "p & q" 
    formula5 = "p>>q"
    KB = [to_cnf(formula1), to_cnf(formula2),to_cnf(formula3),to_cnf(formula4),to_cnf(formula5)]
    print("OLD KB: ", KB)
    formula6 = "q"
    KB = contraction(KB, formula6)
    print("NEW CONTRACTED KB 1: ", KB)
    

    print("\n sentence 2: \n")

    formula1 = "p"
    formula3 = "p | q"
    formula4 = "p & q" 
    formula2 = bi_imp("p","q")
    KB = [to_cnf(formula1), to_cnf(formula2),to_cnf(formula3),to_cnf(formula4)]
    print("OLD KB: ", KB)
    formula6 = "p"
    KB = contraction(KB, formula6)
    print("NEW CONTRACTED KB 2: ", KB)

