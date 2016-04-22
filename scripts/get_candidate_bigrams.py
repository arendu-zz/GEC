#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
import itertools
import enchant
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'
#import pdb
BOS = '<s>'
EOS = '</s>'

if __name__ == '__main__':
    opt = OptionParser()
    # insert options here
    opt.add_option('-f', dest='gec_raw_file', default='')
    opt.add_option('-p', dest='gec_pos_file', default='')
    opt.add_option('--nf', dest='nf_file', default='')
    opt.add_option('--vf', dest='vf_file', default='')
    opt.add_option('--df', dest='df_file', default='')
    opt.add_option('--pf', dest='pf_file', default='')
    opt.add_option('--prof', dest='prof_file', default='')
    opt.add_option('--bf', dest='bigram_file', default='')
    opt.add_option('--uf', dest='unigram_file', default='')

    (options, _) = opt.parse_args()
    if options.gec_raw_file == '' or options.gec_pos_file == '' or options.nf_file == '' or options.vf_file == '' or options.df_file == '' or options.pf_file == '' or options.prof_file == '' or options.bigram_file == '':
        sys.stderr.write('Usage: '
                'python get_candidate_bigrams.py '
                '-f [gec raw file] '
                '-p [pos file] '
                '--nf [nf file] '
                '--df [df file] '
                '--pf [preposition file] '
                '--prof [pronuon file] '
                '--bf [bigram file](bigrams from gigaword) '
                '--uf [unigram file](unigrams from gigaword) '
                '--vf [vf file]\n')
        exit(1)
    else:
        pass
    d = enchant.Dict('en_US')
    sys.stderr.write('loading bigrams...')
    giga_bigrams = dict((items.split('\t')[1].lower(),float(items.split('\t')[0])) for items in codecs.open(options.bigram_file, 'r', 'utf8').readlines()) 
    giga_unigrams = dict((items.split('\t')[1].lower(),float(items.split('\t')[0])) for items in codecs.open(options.unigram_file, 'r', 'utf8').readlines()) 
    seen = {}
    sent_list = codecs.open(options.gec_raw_file, 'r', 'utf8').readlines()
    pos_list = codecs.open(options.gec_pos_file, 'r', 'utf8').readlines()
    nf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.nf_file, 'r', 'utf8').readlines())
    vf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.vf_file, 'r', 'utf8').readlines())
    df = [item.strip() for item in codecs.open(options.df_file, 'r', 'utf8').readlines()  if item.strip() != '']
    pf = [item.strip() for item in codecs.open(options.pf_file, 'r', 'utf8').readlines() if item.strip() != '']
    prof = [item.strip() for item in codecs.open(options.prof_file, 'r', 'utf8').readlines() if item.strip() != '']
    for sent, pos_sent in zip(sent_list, pos_list):
        sys.stderr.write('sent:' + sent)
        sys.stderr.write('pos:' + pos_sent)
        trellis = []
        trellis.append([BOS])
        words = sent.strip().split()
        pos = pos_sent.strip().split()
        for i, (w, p) in enumerate(zip(words, pos)):
            #sys.stderr.write('word:' + w + ' pos:' + p + '\n')
            if p.startswith('VB') and d.check(w) and w in vf:
                #sys.stderr.write('in vf\n')
              
                trellis.append(vf[w])
            elif p.startswith('DT') or p.startswith('RB'):
                #sys.stderr.write('in dt or rb\n')
                trellis.append(df)
            elif p.startswith('NN') and d.check(w) and w in nf:
                #sys.stderr.write('in nn\n')
                #sys.stderr.write('len(nf[w]) ' + str(len(nf[w])) + '\n')
                detxnf = [' '.join(item).strip() for item in itertools.product(df, nf[w])]
                if w.lower() in giga_unigrams:
                    detxnf = [dbigram for dbigram in detxnf if dbigram.lower() in giga_bigrams] 
                else:
                    pass
                detxnf+= nf[w]
                #sys.stderr.write(str(len(detxnf)) +',')
                assert len(detxnf) > 0
                trellis.append(detxnf)
            elif p.startswith('JJ'):
                #sys.stderr.write('in jj\n')
                detxjj = [' '.join(item).strip() for item in itertools.product(df, [w])]
                if w.lower() in giga_unigrams:
                    detxjj = [dbigram for dbigram in detxjj if dbigram.lower() in giga_bigrams]
                else:
                    pass
                detxjj += [w]
                #sys.stderr.write(str(len(detxjj)) +',')
                assert len(detxjj) > 0
                trellis.append(detxjj)
            elif p.startswith('PRP'):
                #sys.stderr.write('in prp\n')
                trellis.append(prof)
            else:
                #sys.stderr.write(w + ' is not in any pos tag...\n')
                trellis.append([w])
            if len(trellis[-1]) >= 1:
                pass
            else:
                sys.stderr.write(w + ' is the w\n')
                sys.stderr.write('\n' + str(trellis) + '\n')
                exit(1)
        trellis.append([EOS])
        for idx,current_candidates  in enumerate(trellis[1:]):
            i = idx+1
            assert type(current_candidates) == type([])
            prev_candidates = trellis[i - 1]
            assert type(prev_candidates) == type([])
            for pc in prev_candidates:
                assert pc != EOS
                for cc in current_candidates:
                    assert cc != BOS
                    print_line = pc + ' ||| '+ cc
                    if print_line in seen:
                        pass
                    else:
                        seen[print_line] = 1
                        print print_line
    sys.stderr.write('done\n')
