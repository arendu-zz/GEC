#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
import numpy as np
from optparse import OptionParser
reload(sys)
'''
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'
'''
import pdb

if __name__ == '__main__':
    opt = OptionParser()
    #insert options here
    opt.add_option('-d', dest='deletion_file', default='')
    opt.add_option('-u', dest='unigrams_file', default='')
    opt.add_option('-b', dest='bigrams_file', default='')
    (options, _) = opt.parse_args()
    if options.deletion_file == '' or options.unigrams_file == '' or options.bigrams_file =='':
        sys.stderr.write('Useage: python compute_eps.py -d [deletion file] -u [unigrams file] -b [bigrams file]\n')
        exit(1)
    else:
        pass
    sys.stderr.write('reading unigrams...\n')
    unigrams = dict((items.strip().split('\t')[1], items.strip().split('\t')[0]) for items in codecs.open(options.unigrams_file, 'r', 'utf8').readlines())
    sys.stderr.write('reading bigrams...\n')
    bigrams =  dict((items.strip().split('\t')[1], items.strip().split('\t')[0]) for items in codecs.open(options.bigrams_file, 'r', 'utf8').readlines())
    deletions = {}
    deletion_content = [i.strip() for i in codecs.open(options.deletion_file, 'r', 'utf8').readlines()]
    b  = []
    A = []
    x = ['x1', 'x2']
    for line in deletion_content:
        items = line.strip().split('\t') 
        deletions[items[2].strip()] = (items[0].strip(), items[1].strip())
        if items[2].strip() in bigrams:
            b_i = float(bigrams[items[2].strip()])
            #for u in items[2].strip().split():
            #    b_i -= float(unigrams[u])
            b.append(b_i)
            if items[0].strip() == 'Prep':
                A.append([1.0, 1.0,0.0,0.0])
                pass
            elif items[0].strip() == 'ArtOrDet':
                A.append([0.0,0.0,1.0, 1.0])
                pass
            else:
                pass
    b = np.array(b)
    A = np.ones((np.size(b),4))
    b = np.reshape(b, (np.size(b), 1))
    x = np.linalg.lstsq(A, b)
    print x
