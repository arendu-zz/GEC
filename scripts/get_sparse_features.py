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

def emission_features(p, w, cc):
    features = []
    cc_list = [c.strip() for c in cc.strip().split()]
    if cc_list == 2:
        features.append(w + '-' + cc_list[0] + '-inserted')
        features.append(cc_list[0] + '-inserted')
        features.append(w + '-' + cc_list[0])
        features.append(w + '-' + cc_list[1])
    if cc_list == 1:
        features.append(w +'-' + cc_list[0])
    return ' '.join([f + ' ' + '1.0' for f in features])

def bigram_features(prev_p, p, pc, cc, w):
    features = []
    pc_list = [c.strip() for c in pc.strip().split()]
    cc_list = [c.strip() for c in cc.strip().split()]

    if len(cc_list) == 1 and cc_list[0] == '<eps>':
        features.append('-'.join(['DEL','LC', 'W' , pc_list[0], w , '<eps>']))
        features.append('-'.join(['DEL','LC', pc_list[0], '<eps>']))
        features.append('-'.join(['DEL','W', w, '<eps>']))

    if len(cc_list) == 2:
        inserted = cc_list[0]
        features.append('-'.join(['INS','LC', 'W' , pc_list[0], w , inserted]))
        features.append('-'.join(['INS','LC', pc_list[0], inserted]))
        features.append('-'.join(['INS','W', w, inserted]))

    if len(pc_list) == 1 and pc_list[0] == '<eps>':
        features.append('-'.join(['DEL','RC', cc_list[0], '<eps>']))

    return ' '.join([f + ' ' + '1.0' for f in features])


def load_lm(lm_file):
    lm  = {}
    for line in codecs.open(lm_file, 'r', 'utf8').readlines():
        if line.strip() == '' or line.strip().startswith('\\') or line.strip().startswith('ngram'):
            pass
        else:
            items = line.strip().split('\t')
            if len(items) == 3:
                prob, token , bow = items[0], items[1], items[2]
                lm[token] = (float(prob), float(bow))
            elif len(items) == 2:
                prob, tokens = items[0], items[1]
                lm[tokens] = float(prob)
    return lm

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
    opt.add_option('--lm', dest='lm_file', default='')

    (options, _) = opt.parse_args()
    if options.gec_raw_file == '' or options.gec_pos_file == '' or options.nf_file == '' or options.vf_file == '' or options.df_file == '' or options.pf_file == '' or options.prof_file == '' or options.lm_file == '':
        sys.stderr.write('Usage: '
                'python get_sparse_features.py '
                '-f [gec raw file] '
                '-p [pos file] '
                '--nf [nf file] '
                '--df [df file] '
                '--pf [preposition file] '
                '--prof [pronuon file] '
                '--lm [lm file] '
                '--vf [vf file]\n')
        exit(1)
    else:
        pass
    d = enchant.Dict('en_US')
    sys.stderr.write('loading unigrams...')
    giga_lm = load_lm(options.lm_file)
    #giga_unigrams = dict((items.strip().split('\t')[1], float(items.strip().split('\t')[0])) for items in codecs.open(options.unigram_file, 'r', 'utf8').readlines())
    #sys.stderr.write('reading bigrams...\n')
    #giga_bigrams =  dict((items.strip().split('\t')[1], float(items.strip().split('\t')[0])) for items in codecs.open(options.bigram_file, 'r', 'utf8').readlines())
    deletions = {}
    seen = {}
    sent_list = codecs.open(options.gec_raw_file, 'r', 'utf8').readlines()
    pos_list = codecs.open(options.gec_pos_file, 'r', 'utf8').readlines()
    nf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.nf_file, 'r', 'utf8').readlines())
    vf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.vf_file, 'r', 'utf8').readlines())
    df = [item.strip() for item in codecs.open(options.df_file, 'r', 'utf8').readlines()  if item.strip() != '']
    pf = [item.strip() for item in codecs.open(options.pf_file, 'r', 'utf8').readlines() if item.strip() != '']
    prof = [item.strip() for item in codecs.open(options.prof_file, 'r', 'utf8').readlines() if item.strip() != '']
    all_candidates = []
    for sent, pos_sent in zip(sent_list, pos_list):
        sys.stderr.write('sent:' + sent)
        #sys.stderr.write('pos:' + pos_sent)
        trellis = []
        trellis.append([BOS])
        words = sent.strip().split()
        pos = pos_sent.strip().split()
        for i, (w, p) in enumerate(zip(words, pos)):
            prev_p = pos[i-1] if i > 0 else None
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
                detxnf = [' '.join(item).strip() for item in itertools.product([_ for _ in df if _ != '<eps>'], nf[w])]
                if w.lower() in giga_lm:
                    detxnf = [dbigram for dbigram in detxnf if dbigram.lower() in giga_lm] 
                else:
                    pass
                detxnf+= nf[w]
                #sys.stderr.write(str(len(detxnf)) +',')
                assert len(detxnf) > 0
                trellis.append(detxnf)
            elif p.startswith('JJ'):
                #sys.stderr.write('in jj\n')
                detxjj = [' '.join(item).strip() for item in itertools.product([_ for _ in df if _ != '<eps>'], [w])]
                if w.lower() in giga_lm:
                    detxjj = [dbigram for dbigram in detxjj if dbigram.lower() in giga_lm]
                else:
                    pass
                detxjj += [w]
                #sys.stderr.write(str(len(detxjj)) +',')
                assert len(detxjj) > 0
                trellis.append(detxjj)
            elif p.startswith('PRP'):
                #sys.stderr.write('in prp\n')
                trellis.append(prof)
            elif p.startswith('IN') and w in pf:
                trellis.append(pf)
                pass
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
                    #lm_score = get_lm_score(pc, cc)
                    #emission_state = 'EMISSION ### ' + w + ' ### ' + cc
                    bigram_state = 'BIGRAM ### ' + pc + ' ### ' + cc 
                    #if not emission_state in seen:
                    #    seen[emission_state] = 1
                    #    print emission_state +' ### '+ emission_features(p, w,cc) 
                    if not bigram_state in seen:
                        seen[bigram_state] = 1
                        print bigram_state + ' ### ' + bigram_features(prev_p, p, pc, cc, w)
    sys.stderr.write('done\n')
