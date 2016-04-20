#!/usr/bin/env python
#encoding: utf-8

import sys
import os
import linecache
import enchant
from pattern.en import conjugate, lemma, lexeme

d = enchant.Dict("en_US")
def main():
    m2_mod = open(sys.argv[1]+'.mod', 'r')
    pos_file = sys.argv[1]+'.mod.pos'
    l = 1
    token_dict = {}
    for li in m2_mod.readlines():
        if li[0] == 'S':
            tokens = li.split()[1:]
            postags = linecache.getline(pos_file, l).rstrip().split()
            assert len(tokens) == len(postags)

            for pos_i, token_i in zip(postags, tokens):
                #if not lemma(token_i) in token_dict and pos_i[0:2]=='VB': 
                if not token_i in token_dict and pos_i[0:2]=='VB': 
                    candidates = lexeme(token_i)
                    filtered = [c for c in candidates if (("n't" not in c) and (len(c.split())==1) and d.check(c))]
                    if len(filtered) >0:
                        print token_i, " ".join(filtered)
                    token_dict[lemma(token_i)] = 1
            l += 1

if __name__ == '__main__':
    main()

