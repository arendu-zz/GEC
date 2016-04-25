#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import copy
import codecs
import numpy as np
from optparse import OptionParser
from scipy.optimize import minimize
reload(sys)
'''
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'
'''
import pdb
global A,b

def ls_obj(x):
    global A,b
    return np.sum((A.dot(x) - b) ** 2)

def ls_grad(x):
    global A,b
    x_r = np.reshape(x, (np.size(x),1))
    print A.shape, x.shape, x_r.shape, b.shape
    g_x = 2 * A.T.dot(A.dot(x_r) - b)
    print g_x.shape
    g_x = np.reshape(g_x, (np.size(x),))
    return g_x

def gradient_checking(theta, eps, val):
    f_approx = np.zeros(np.shape(theta))
    for i, t in enumerate(theta):
        theta_plus = copy.deepcopy(theta)
        theta_minus = copy.deepcopy(theta)
        theta_plus[i] = theta[i] + eps
        theta_minus[i] = theta[i] - eps
        f_approx[i] = (val(theta_plus) - val(theta_minus)) / (2 * eps)
        print i, len(theta)
    return f_approx

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
            for u in items[2].strip().split():
                b_i -= float(unigrams[u])
            b.append(b_i)
            if items[0].strip() == 'Prep':
                A.append([1.0, 1.0, 0.0, 0.0])
                pass
            elif items[0].strip() == 'ArtOrDet':
                A.append([0.0, 0.0, 1.0, 1.0])
                pass
            else:
                pass
    b = np.array(b)
    A = np.array(A)
    A = np.reshape(A, (np.size(b), 4))
    b = np.reshape(b, (np.size(b), 1))
    x = np.zeros((4,1)) 
    x_solution = minimize(ls_obj, x,method='L-BFGS-B', jac=ls_grad,tol=1e-5)
    print x_solution
    print 'check '
    gradient_checking(np.zeros((4,1)), 1e-4, ls_obj)
    g_x = ls_grad(np.zeros((4,1)))
    print 'check g', g_x
