Run main.py

You are given a default belief base and you have the following options:

addition(a): Add a belief to the Belief base
check(ch): Check a formula for entailment
contract(c): Belief contraction
revise(r): Revise the Belief base with a formula
empty(e): Empty Belief base
print(p): Print Belief base
help(h): Print help
quit(q): Quit


You can choose an option by entering the corresponding letter. When adding a belief or revising the Belief base, you will be asked for an entrenchment value for the belief. This entrenchment value is later used during contractions and revisions of the belief base. If you don't provide an entrenchment value for the belief, it will be calculated automatically and also the entrenchment value of previous beliefs will be updated based on the complexity of their formulas (the more complex the less important). Older beliefs receive penalties to their entrenchment values when a new belief with at least one same element is added.