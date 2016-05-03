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

def make_mat(tokens, lp):
		t_mat = np.zeros((len(tokens), len(tokens)))
		for i, tok_i in enumerate(tokens):
				for j, tok_j in enumerate(tokens):
						t_mat[i,j] = lp.get((tok_i, tok_j), 0.008)

		np.fill_diagonal(t_mat, 0.0)
		return t_mat

if __name__ == '__main__':
    opt = OptionParser()
    #insert options here
    opt.add_option('-c', dest='corpus', default='')
    (options, _) = opt.parse_args()
		if option.corpus == '':
				sys.stderr.write('Usage: python -c [corpus file] -o [output lexical file]\n')
				exit(1)
		else:
				pass

		lex_probs = {}
		for iter in range(4):
				lex_counts = {}
				with codecs.open(options.corpus, 'r', 'utf8') as f:
						for line in f:
								tokens = line.strip().split()
								t_mat = make_mat(tokens, lex_probs)
								t_sum = np.sum(t_mat, 1)
								t_mat = t_mat / t_sum
								for i, tok_i in enumerate(tokens):
										for j, tok_j in enumerate(tokens):
												lex_counts[tok_i, tok_j] = lex_counts.get((tok_i, tok_j),0.0) + t_mat[i,j]
												lex_counts[tok_j] = lex_counts.get(tok_j, 0.0) + t_mat[i,j]



		



