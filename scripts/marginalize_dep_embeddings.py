#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'

if __name__ == '__main__':
    opt = OptionParser()
    #insert options here
    opt.add_option('-c', dest='dep_context_embeddings', default='')
    (options, _) = opt.parse_args()
    if options.dep_context_embeddings == '':
        sys.stderr.write('Usage: python marginalize_dep_context.py -c [dep context embedding file]\n')
        exit(1)
    else:
        pass
    w2em = {}
    for line in codecs.open(options.dep_context_embeddings, 'r', 'utf8').readlines()[1:]:
        items = line.strip().split()
        if len(items) > 101:
            continue

        dep_word = items[0].split('_')
        if len(dep_word) == 1:
            word = dep_word[-1]
            dep = '_'.join(dep_word[:1])
        elif len(dep_word) > 1:
            word = dep_word[-1]
            dep = '_'.join(dep_word[:1])
        else:
            pass
        '''
        if dep_word.count('_') == 1:
            s_position = dep_word.find('_')
            if s_position == -1:
                dep = ''
                word = dep_word.strip()
            else:
                dep = dep_word[:s_position]
                word = dep_word[s_position+1:]
        else:
            sys.stderr.write('warn:' + dep_word + '\n')
        '''
        word = word.strip() if word.strip() != '' else '_'
        embedding = [float(i) for i in items[1:]]
        n_s, n_c = w2em.get(word, ([0.0] * 100, 0.0)) 
        n_s = [i+j for i,j in zip(n_s, embedding)] 
        n_c += 1.0
        w2em[word] = (n_s, n_c)
        sys.stderr.write('.\n')

    for word, (n_s, n_c) in w2em.iteritems():
        print word.strip() + ' '+  ' '.join(['%.6f' %(i/n_c) for i in n_s])

