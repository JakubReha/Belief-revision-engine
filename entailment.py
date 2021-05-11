import itertools
from sympy.logic.boolalg import to_cnf, Or, And


def remove_elem(elem, clause):
    return [x for x in clause if x != elem]


def split(clause, op):
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


def resolution(p,q):

    clauses = []
    list_dp = split(p,Or)
    list_dq = split(q, Or)

    for dp in list_dp:
        for dq in list_dq:
            if dp == ~dq or ~dp == dq:
                res = remove_elem(dp, list_dp) + remove_elem(dq, list_dq)
                res = list(set(res))
                new_list = Or(*res)
                clauses.append(new_list)
    return clauses
    
    
def entails(KBb, formula):
    formula = to_cnf(formula)
    clauses = KBb + split(to_cnf(~formula), And)


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

