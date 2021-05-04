import numpy as np
from sympy.logic.boolalg import to_cnf, Or, And


def removeall(item, seq):
    return [x for x in seq if x != item]

def unique(seq):
    return list(set(seq))

def disjuncts(clause):
    return dissociate(Or, [clause])

def conjuncts(clause):
    return dissociate(And, [clause])

def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)

def dissociate(op, args):
    result = []

    def collect(subargs):
        for arg in subargs:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result
    
    
def entails(KB, formula):
    formula = to_cnf(formula)
    clauses = []
    for f in KB:
        clauses.append(conjuncts(f))
    clauses.append(conjuncts(to_cnf(~formula)))


    if False in clauses:
        return True

    result = set() # use set to have unique results
    while True:
        n = len(clauses)
        pairs = [
            (clauses[i], clauses[j])
            for i in range(n) for j in range(i + 1, n)
        ]

        for ci, cj in pairs:
            resolvents = resolve(ci, cj)
            if False in resolvents:
                return True
            result = result.union(set(resolvents))

        if result.issubset(set(clauses)):
            return False
        for c in result:
            if c not in clauses:
                clauses.append(c)


def resolve(p,q):

    "Resolution algorithm for p and q"

    clauses = []
    list_dp = disjuncts(p)
    list_dq = disjuncts(q)

    for dp in list_dp:
        for dq in list_dq:
            # Check if dp and dq are complementary
            if dp == ~dq or ~dp == dq:
                # Remove dp and dq from the list of clauses if they are complementary of each other
                res = removeall(dp, list_dp) + removeall(dq, list_dq)
                # Remove duplicates
                res = unique(res)
                # Create a new list of clauses
                new_list = associate(Or, res)
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
