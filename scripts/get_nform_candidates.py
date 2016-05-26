#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
from pattern.en import pluralize, singularize, suggest
import enchant

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'
d = enchant.Dict("en_US")
if __name__ == '__main__':
    opt = OptionParser()
    # insert options here
    opt.add_option('-f', dest='m2_raw', default='')
    opt.add_option('-l', dest='lemma_file', default='')
    opt.add_option('-p', dest='pos', default='')
    (options, _) = opt.parse_args()
    if options.m2_raw == '' or options.pos == '':
        sys.stderr.write("Usage: python make_nounforms.py -f [gec raw file] -p [pos file] -l [gec lemma file] > [output file]\n")
        exit(1)
    else:
        pass
    pos_lines = codecs.open(options.pos, 'r', 'utf8').readlines()
    sent_lines = codecs.open(options.m2_raw, 'r', 'utf8').readlines()
    lemma_lines = codecs.open(options.lemma_file, 'r', 'utf8').readlines()
    nounforms = {}
    for lemma_line, pos_line, sent_line in zip(lemma_lines, pos_lines, sent_lines):
        for lem, pos, word in zip(lemma_line.strip().split(),pos_line.strip().split(), sent_line.strip().split()):
            if pos == 'NN' or pos == 'NNS':
                lem = lem.lower()
                if lem in nounforms:
                    continue
                nforms = [lem+'|||nsg',pluralize(lem)+'|||npl'] 
                for n_number in nforms:
                    n, number = n_number.split('|||')
                    nounforms[n] = nforms
            else:
                pass  # not a noun or noun_pl

    for k, v in sorted(nounforms.iteritems()):
        print k, ' '.join(v)
