import itertools
from sympy.logic.boolalg import to_cnf, Or, And
from entailment import entails
import numpy as np



# 1) implement the order (based on the complexity of the predicate, when it was added to the KB)
# 2) transform the KB  from  [a & b, c, c| b] to [a , b, c, c| b] (remove the contractions)
# 3) create some user interface

def contraction(KB, formula):
        formula = to_cnf(formula)
        comb = []
        for i in range(1,len(KB)+1):
            comb += list(itertools.combinations(KB, i))

        new_KB = []
        for c in comb:
            if not entails(list(c), formula):
                new_KB.append(c)
        max_l = max([len(c) for c in new_KB ])
        max_c = []
        for c in new_KB:
            if len(c) == max_l:
                max_c.append(c)
        result = set(KB).intersection(*set(max_c))
        if len(result) == 0: 
            # TO DO !!!!!! if the intersection is None, return one of the remainder sets based on the order
            # for now returning UNION which is wrong
            return set(max_c[0]).union(*set(max_c[1:]))
        return result
        
def revision(KB, formula):
    KB = contraction(KB, ~formula)
    KB += to_cnf(formula)
    return KB

        
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

