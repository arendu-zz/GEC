#!/usr/bin/env python
#encoding: utf-8

import sys
import os
import subprocess

CANDIDATES_PATH = "/home/arenduc1/Projects/GEC/data/gec/candidate_bigrams"
#CANDIDATES_PATH = "./test_candidates"
UNIGRAM_PATH = "/home/arenduc1/Projects/GEC/data/gec/giga.lm.1.unigram.only.100k"
BIGRAM_PATH = "/home/arenduc1/Projects/GEC/data/gec/giga.lm.1.bigram.only.100k"

#load unigram and bigram
unigram = {}
bigram = {}

cmd = subprocess.Popen(['wc', '-l', UNIGRAM_PATH], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
wcl_unigram = int(cmd.communicate()[0].rstrip().split()[0])
cmd = subprocess.Popen(['wc', '-l', BIGRAM_PATH], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
wcl_bigram = int(cmd.communicate()[0].rstrip().split()[0])
cmd = subprocess.Popen(['wc', '-l', CANDIDATES_PATH], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
wcl_candidates = int(cmd.communicate()[0].rstrip().split()[0])


with open(UNIGRAM_PATH, 'r') as f:
    sys.stderr.write("unigram loading\n")
    p = 0
    for i, l in enumerate(f.readlines()):
        prob, token, extra = l.rstrip().split('\t')
        unigram[token] = float(prob)
        if (i+1) % (wcl_unigram//100) == 0:
            p += 1
            sys.stderr.write("\r%d%%" % p)
            sys.stderr.flush()
    sys.stderr.write("\nunigram load complete\n")

with open(BIGRAM_PATH, 'r') as f:
    sys.stderr.write("bigram loading\n")
    p = 0
    for i, l in enumerate(f.readlines()):
        prob, token, extra = l.rstrip().split('\t')
        bigram[token] = float(prob)
        if (i+1) % (wcl_bigram//100) == 0:
            p += 1
            sys.stderr.write("\r%d%%" % p)
            sys.stderr.flush()
    sys.stderr.write("\nbigram load complete\n")

f = open(CANDIDATES_PATH, 'r')
li = f.readline()

exists = 0
noexists = 0
p = 0
i = 0
sys.stderr.write("add bigram scores for candidates\n")
while li:
    tokens = li.rstrip().split(' ')
    tokens.remove('|||')
    scores = []
    for n in range(1, len(tokens)):
        bi = tokens[n-1] + " " + tokens[n]
        if bi in bigram:
            scores.append(bigram[bi])
            exists += 1
        else:
            scores.append(float('-inf'))
            noexists += 1
        #sys.stderr.write("\r%d\t%d" % (exists, noexists))
        #sys.stderr.flush()
    score = sum(scores)/float(len(tokens))
    if score == float('-inf'):
        pass
    else:
        print "BIGRAM ### LM ### {} ### {} ### {}".format(" ".join(tokens), li.rstrip(), str(score))
        #li.rstrip() + " ||| " + str(score)

    if (i+1) % (wcl_candidates//100) == 0:
        p += 1
        sys.stderr.write("\r%d%%" % p)
        sys.stderr.flush()

    i += 1
    li = f.readline()
    
sys.stderr.write("\nexists: %d" % exists)
sys.stderr.write("\nnoexists: %d\n" % noexists)
