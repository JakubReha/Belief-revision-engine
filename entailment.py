import numpy as np
import itertools
from sympy.logic.boolalg import to_cnf, Or, And


def remove_elem(elem, clause):
    return [x for x in clause if x != elem]

def disjunction(clause):
    return split(clause, Or)

def conjunction(clause):
    return split(clause, And)


def split(clause), op:
    result = []

    def recurse(clause):
        for sub in clause:
            if isinstance(sub, op):
                recurse(sub.args)
            else:
                result.append(sub)
    clause = [clause]
    recurse(clause)
    return result
    
    
def entails(KB, formula):
    formula = to_cnf(formula)
    clauses = []
    for f in KB:
        clauses += conjunction(f)
    clauses += conjunction(to_cnf(~formula))


    if False in clauses:
        return True

    result = set() 
    n = len(clauses)
    while True:
        comb = itertools.combinations(clauses, 2)
        for ci, cj in comb:
            resolved = resolution(ci, cj)
            if False in resolved:
                return True
            result = result.union(set(resolved))

        if result.issubset(set(clauses)):
            return False
        for c in result:
            if c not in clauses:
                clauses.append(c)


def resolution(p,q):

    clauses = []
    list_dp = disjunction(p)
    list_dq = disjunction(q)

    for dp in list_dp:
        for dq in list_dq:
            if dp == ~dq or ~dp == dq:
                res = remove_elem(dp, list_dp) + remove_elem(dq, list_dq)
                res = list(set(res))
                new_list = Or(*res)
                clauses.append(new_list)
    return clauses

if __name__ == '__main__':
    formula1 = "~a >> b"
    formula2 = "b >> a"
    formula3 = "a >> c & d"
    KB = [to_cnf(formula1), to_cnf(formula2),to_cnf(formula3)]
    formula4 = "a & c & d"

    print(KB)
    print(entails(KB,formula4))
