#!/usr/bin/env python

"""
Implements a simple framework for defining grammars of the sort given
in table 1 of the paper. Use

python grammar.py

to run the demo, which creates the training and testing data used in
`synthesis.py`.

To see how the implementation works, it's probably easiest to study
gold_lexicon, rules, and functions below. Together, these implement
the example in table 1.

The only real difference from the paper is that this implementation
creates only binary branching structures, so that we can use the
familiar CYK parsing algorithm (in `Grammar.gen`). Thus, the
structures are like this:

three plus minus two

[('N', 'add(3)(neg(2))'), 
    [('B', 'add(3)'), 
        [('N', '3'), 'three'], 
        [('R', 'add'), 'plus']], 
    [('N', 'neg(2)'), 
        [('U', 'neg'), 'minus'], 
        [('N', '2'), 'two']]]

To create new grammars, you just need to define the following:

* A lexicon mapping strings to arrays of tuples, where the tuples
  are (category, logical form) pairs.

* A set of rules, each a list [X, Y, Z, (a,b)], where X is the left
  daughter category, Y is the right daughter category, Z is the 
  mother category, and (a,b) says which order of application to
  use in the semantics: (0,1) means apply X to Y, and (1,0)
  means apply Y to X.

* A set of Python functions that will interpret the logical forms
  (second members of all the nonterminal node labels).  If your
  logical forms can be intepreted in native Python this can be 
  empty.
"""


__author__ = "Christopher Potts and Percy Liang"
__credits__ = []
__license__ = "GNU general public license, version 2"
__version__ = "2.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the authors' websites"


import sys
from collections import defaultdict
from itertools import product
from world import *


# allblocks are the the blocks from world.py and world.jpg that get used as an example here
# all_blocks_grid is needed later to create the Picture Object corresponding to the picutre in world.jpg
all_blocks_grid = allblocks.copy()

# a list of all blocks that is used for evaluating the truth of the descriptions (doesn't include None anymore)
allblocks2 = []
for row in allblocks:
    for blo in row:
        if blo:
            allblocks2.append(blo)
allblocks=allblocks2
guessed_blocks = set()


def positiontest(blocks,blocklocations,position):
    """
    finds all pairs of blocks b1 form blocks and b2 from blocklocations that stand in relation position to eachother
    e.g. blocks is a list of all blue rectangles and blocklocations a list of all red circles and position is 'u' then the function returns
    all blocks that are blue rectangles and are below red circles
    blocks and blocklocations: two lists of blocks  
    position: 'u' for under or 'o' for over
    """
    fulfill = []
    fulfill2 = []
    if position == "u":
        for b1 in blocks:
            for b2 in blocklocations:
                if b1.y > b2.y:
                    fulfill.append(b1)
                    fulfill2.append(b1)
                    fulfill2.append(b2)
        
    elif position == "o":
        for b1 in blocks:
            for b2 in blocklocations:
                if b1.y < b2.y:
                    fulfill.append(b2)
                    fulfill2.append(b1)
                    fulfill2.append(b2)

    current_guesses = guessed_blocks.copy()
    for bl in current_guesses:
        if bl not in fulfill2:
            guessed_blocks.remove(bl)
    return fulfill
    

def blockfilter(conditions,blocks):
    """
    returns a list of all blocks that match the specific conditions
    conditions: list of conditions, e.g. shape == rectangle or color == 
    """
    fulfill = []
    for b in blocks:
        test = True
        for c in conditions:
            test = test and c(b)
        if test:
            fulfill.append(b)
            guessed_blocks.add(b)
        
    return fulfill


class Grammar:
    def __init__(self, lexicon, rules, functions):
        """For examples of these arguments, see below."""
        self.lexicon = lexicon
        self.rules = rules
        self.functions = functions

    def gen(self, s):
        """CYK parsing, but we just keep the full derivations. The input
        s should be a string that can be parsed with this grammar."""
        words = s.split()
        n = len(words)+1
        trace = defaultdict(list)
        for i in range(1,n):
            word = words[i-1]
            trace[(i-1,i)] = [[(syntax, semantics), word]
                              for syntax, semantics in self.lexicon[word]]
        for j in range(2, n):
            for i in range(j-1, -1, -1):
                for k in range(i+1, j):
                    for c1, c2 in product(trace[(i,k)], trace[(k,j)]):
                        for lfnode in self.allcombos(c1[0], c2[0]):                                                                                                          
                            trace[(i,j)].append([lfnode, c1, c2])
        # Return only full parses, from the upper right of the chart:
        return trace[(0,n-1)] 

    def allcombos(self, c1, c2):
        """Given any two nonterminal node labels, find all the ways
        they can be combined given self.rules."""
        results = []
        for left, right, mother, app_order in self.rules:
            if left == c1[0] and right == c2[0]:
                sem = [c1[1], c2[1]]
                results.append((mother, "{}({})".format(
                    sem[app_order[0]], sem[app_order[1]])))
        return results

    def sem(self, lf):
        """Interpret, as Python code, the root of a logical form
        generated by this grammar."""
        # Import all of the user's functions into the namespace to
        # help with the interpretation of the logical forms.
        grammar = sys.modules[__name__]
        for key, val in list(self.functions.items()):
            setattr(grammar, key, val)
        return eval(lf[0][1]) # Interpret just the root node's semantics. 

# The lexicon for our pictures 
gold_lexicon = {
    'form':[('B','[]')],
    'forms':[('B','[]')],
    'square': [('B','[(lambda b: b.shape == "rectangle")]')],
    'squares': [('B','[(lambda b: b.shape == "rectangle")]')],
    'triangle': [('B','[(lambda b: b.shape == "triangle")]')],
    'triangles': [('B','[(lambda b: b.shape == "triangle")]')],
    'circle': [('B','[(lambda b: b.shape == "circle")]')],
    'circles': [('B','[(lambda b: b.shape == "circles")]')],
    'green':[('C','green')],
    'yellow':[('C','yellow')],
    'blue':[('C','blue')],
    'red':[('C','red')],
    'there':[('E','exist')],
    'is':[('I','identy')],
    'are':[('I','identy')],
    'a':[('N','range(1,int(sys.float_info.max))')],
    'one':[('N','[1]')],
    'two':[('N','[2]')],
    'three':[('N','[3]')],
    'under':[('U','under')],
    'over':[('U','over')],
    'and':[('AND','und')],
    #'of':[('O','ofl'),('O','ofr')],
    #'left':[('L','left')],
    #'right':[('R','right')]
}

# The binarized rule set for our pictures
# The second rule corresponds to:
# EN -> E N  semantics: apply E(N)
rules = [
    ['C', 'B', 'B', (0,1)],
    ['E','N','EN',(0,1)],
    ['E','I','E',(1,0)],
    ['EN','B','V',(0,1)],
    ['U','N','UN',(0,1)],
    ['UN','B','L',(0,1)],
    ['B','L','B',(1,0)],
    ['V','AND','VAND',(1,0)],
    ['VAND','V','V',(0,1)],
    #['LEFT','O','LO',(1,0)],
    #['RIGHT','O','RO'],(1,0),
    #['LO','N','LON',(0,1)],
    #['LON','BC','L',(0,1)],
    #['RO','N','RON',(0,1)],
    #['RON','BC','L',(0,1)]
    
]

# These are needed to interpret our logical forms with eval. They are
# imported into the namespace Grammar.sem to achieve that.
# so far only above and under are working, we are going to add left and right also
functions = {
    'block': (lambda conditions: (lambda number_requirement: (number_requirement,conditions))),
    'identy': (lambda x: x),
    'exist': (lambda n : (lambda b: len(blockfilter(b,allblocks)) in n)),
    'und':(lambda v1:(lambda v2: v1 and v2)),
    'blue': (lambda x: x+[(lambda b:b.colour=="blue")]),
    'red': (lambda x: x+[(lambda b:b.colour=="red")]),
    'green': (lambda x: x+[(lambda b:b.colour=="green")]),
    'yellow':(lambda x: x+[(lambda b:b.colour=="yellow")]),
    'under':(lambda n: (lambda x:(lambda y: y+[(lambda b: len(positiontest(blockfilter(y,allblocks),blockfilter(x,allblocks),"u")) in n)]))),
    'over':(lambda n: (lambda x:(lambda y: y+[(lambda b: len(positiontest(blockfilter(y,allblocks),blockfilter(x,allblocks),"o")) in n)]))),
    #'left':(lambda n: (lambda x:(lambda y: y+[(lambda b: len(filter(lambda: b.x==1)) in n)]))),
    #'right':(lambda n: (lambda x:(lambda y: y+[(lambda b: len(filter(lambda: b.x==4)) in n)]))),
    #'ofl':(lambda f:(lambda n: (lambda x:(lambda y: y+[(lambda b: len(positiontest(blockfilter(y,allblocks),blockfilter(x,allblocks),"l")) in n)])))),
    #'ofr':(lambda f:(lambda n: (lambda x:(lambda y: y+[(lambda b: len(positiontest(blockfilter(y,allblocks),blockfilter(x,allblocks),"r")) in n)]))))    
}




if __name__ == '__main__':

    # Simple demo with the test data:
    from semdata import test_utterances

    # creates the grammar 
    gram = Grammar(gold_lexicon, rules, functions)

    # parses all test sentences from semdata.py
    # prints the derived logical forms for each test sentence and whether the test sentence is true with respect to the example pictuer world.png
    for u in test_utterances:

        # creates the global variable for keeping track of which block is / blocks are the described one(s)
        guessed_blocks = set()
        
        lfs = gram.gen(u)
        print("======================================================================")
        print('Utterance: {}'.format(u))
        for lf in lfs:
            print("\tLF: {}".format(lf))
            print('\tDenotation: {}'.format(gram.sem(lf)))

            # visualization of how the computer gives feedback about what it "understood"
            # for the example test sentence 'there is a red triangle under a blue square' the picture object corresponding to world.png is created
            # and a png file is created and saved where the blocks that are in all_blocks_grid are marked, e.g. all blocks that are red and have shape
            # triangle and are positioned below a blue square in the grid are marked
            if u == 'there is a blue square over a red triangle':
                from BlockPictureGenerator import * 
                test_pic = Picture(name="test_guessing")
                test_pic.blocks = allblocks.copy()
                test_pic.block_n = len(test_pic.blocks)
                test_pic.grid = all_blocks_grid

                test_pic.draw()
                guess = []
                for b in guessed_blocks:
                    guess.append((b.y, b.x))
                test_pic.mark(guess)


                

    


