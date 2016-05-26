#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
from pattern.en import pluralize, singularize, suggest, conjugate
from pattern.en import lexeme, lemma
import enchant

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'
d = enchant.Dict("en_US")
TENSE_ASPECTS = ['inf', '1sg', '3sg', 'part', 'p', 'ppart']
EXCEPTIONS = "am|||1sg are|||2sg is|||3sg are|||pl being|||part were|||p was|||1sgp were|||2sgp was|||3gp were|||ppl been|||ppart".split()

def get_conjugations(lem):
    vforms = []
    if lemma(lem) == 'be':
        vforms = [i for i in EXCEPTIONS]
    else:
        for ta in TENSE_ASPECTS:
            c = conjugate(lemma(lem), ta)
            vforms.append( c +'|||'+ ta)
    return vforms


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
                vforms = get_conjugations(lem)
                #vforms = [c for c in vforms if (("n't" not in c) and (len(c.split())==1) and d.check(c))]
                for v_aspect in vforms:
                    v,aspect = v_aspect.split('|||')
                    verbforms[v] = vforms
            else:
                pass  # not a noun or noun_pl

    for k, v in sorted(verbforms.iteritems()):
        print k, ' '.join(v)
