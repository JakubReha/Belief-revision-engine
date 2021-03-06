from sympy.logic.boolalg import to_cnf, Or, And
from entailment import split
import math

def recurse_2(clause, c=0):
    for sub in clause:
        if isinstance(sub, Or):
            c = c + recurse_2(sub.args,c+1) + len(sub.atoms()) - 1
        elif isinstance(sub, And):
            c = c + recurse_2(sub.args,c-1)
    return c


class Belief_Base:
    
    def __init__(self): 
        self.beliefs = []
        self.base = []
        
    def add_belief(self, belief): 
        new_entrenchment = 1
        if belief.entrenchment is None:
            new_atoms = belief.formula.atoms()
            for b in self.beliefs:
                if new_atoms & b.formula.atoms():
                    b.entrenchment = b.entrenchment - 0.1*b.entrenchment
                    if recurse_2([belief.formula]) < recurse_2([b.formula]):
                        b.entrenchment = b.entrenchment - 0.1*b.entrenchment
                    else:
                        new_entrenchment = new_entrenchment - 0.1*new_entrenchment
            # belief with the same elements get their entrenchment updated to be lower (temporal effect)
            # if the belief with the same elements has more operators it also gets a penalty
        belief.entrenchment = new_entrenchment
        self.beliefs.append(belief)
        self.base += split(to_cnf(belief.formula), And)
        self.base = list(set(self.base))
        
    
    
class Belief:
    
    def __init__(self, formula, entrenchment = None):
        self.formula = to_cnf(formula)
        self.entrenchment = entrenchment
    def __repr__(self):
        return f'Belief: {self.formula} , entrenchment: {self.entrenchment}'
    
    def __eq__(self, other):
        if (isinstance(other, Belief)):
            return self.formula == other.formula
        return False

    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(f'Belief: {self.formula}')

    def __add__(self, other):
        if (isinstance(other, Belief)):
            return self.entrenchment + other.entrenchment

    def __radd__(self, other):
        if other == 0:
            return self.entrenchment
        else:
            return self.__add__(other)


if __name__ == '__main__':
    
    formula = [Belief("p"), Belief("q"), Belief("p | q"), Belief("p & q"), Belief("p>>q>>r&t&p")]

    bb= Belief_Base()
    for f in formula:
        bb.add_belief(f)
    print(bb.beliefs)
    print(bb.base)
