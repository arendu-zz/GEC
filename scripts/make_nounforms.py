#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
from pattern.en import pluralize, singularize

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'

if __name__ == '__main__':
    opt = OptionParser()
    # insert options here
    opt.add_option('-f', dest='m2_mod', default='')
    opt.add_option('-p', dest='pos', default='')
    (options, _) = opt.parse_args()
    if options.m2_mod == '' or options.pos == '':
        sys.stderr.write("Usage: python make_nounforms.py -f [gec file] -p [pos file] > [output file]\n")
        exit(1)
    else:
        pass
    pos_lines = codecs.open(options.pos, 'r', 'utf8').readlines()
    sent_lines = [' '.join(line.split()[1:]) for line in codecs.open(options.m2_mod, 'r', 'utf8').readlines() if
                  line.strip() != '' and line[0] == 'S']
    nounforms = {}
    for pos_line, sent_line in zip(pos_lines, sent_lines):
        for pos, word in zip(pos_line.split(), sent_line.split()):
            if pos == 'NN' or pos == 'NNS':
                if pos == 'NN':
                    word_s = word
                    word_pl = pluralize(word_s)
                else:
                    pass
                if pos == 'NNS':
                    word_pl = word
                    word_s = singularize(word_pl)
                else:
                    pass

                nounforms[word_s] = [word_s, word_pl]
                nounforms[word_pl] = [word_s, word_pl]
            else:
                pass  # not a noun or noun_pl

    for k, v in nounforms.iteritems():
        print k, ' '.join(v)
