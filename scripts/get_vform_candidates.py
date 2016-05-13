#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
from pattern.en import pluralize, singularize, suggest
from pattern.en import lexeme
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
        sys.stderr.write("Usage: python make_verbforms.py -l [gec lemma file] -f [gec raw file] -p [pos file] > [output file]\n")
        exit(1)
    else:
        pass
    pos_lines = codecs.open(options.pos, 'r', 'utf8').readlines()
    sent_lines = codecs.open(options.m2_raw, 'r', 'utf8').readlines()
    lemma_lines = codecs.open(options.lemma_file, 'r', 'utf8').readlines()
    verbforms = {}
    for lemma_line, pos_line, sent_line in zip(lemma_lines, pos_lines, sent_lines):
        for lem, pos, word in zip(lemma_line.strip().split(),pos_line.strip().split(), sent_line.strip().split()):
            word = word.lower()
            word_caps_all = word.upper()
            word_caps = word.capitalize()
            if word in verbforms:
                continue
            if pos.startswith('VB'):
                vforms = []
                lem = lem.lower()
                vforms = lexeme(lem)
                if word in vforms:
                    for v in vforms:
                        verbforms[v] = vforms
                else:
                    sys.stderr.write('word not in vforms ' + str(lem)  + ' ' + str(word)+ '\n')
            else:
                sys.stderr.write('skipping:' + str(word) + ',' + str(pos) +  '\n')
                pass  # not a noun or noun_pl

    for k, v in sorted(verbforms.iteritems()):
        print k, ' '.join(v)
