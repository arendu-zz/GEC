#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
import itertools
import enchant
'''
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'
'''
import pdb
BOS = '<s>'
EOS = '</s>'
NA = 'NO_ASPECT'

def check_dictionary(w):
    return d.check(w) or d.check(w.lower()) or d.check(w.capitalize()) or d.check(w.upper())


def lm_score(lm, w1, w2):
    return 1.0
    w = w1 + ' ' + w2
    if w in lm:
        t = lm[w.lower()]
        if isinstance(t, tuple):
            return t[0]
        else:
            return t
    else:
        return lm.get(w2.lower(), lm["<unk>"])[0] + lm.get(w1.lower(), lm["<unk>"])[1]

def lm_features(lm, pc,  pc_a, cc, cc_a):
    '''
    pc_list_items = [tuple(c.strip().split('|||')) for c in pc.split()]
    pc_list = [i[0] for i in pc_list_items]
    pc_list_aspect = [(i[1] if len(i) == 2 else 'NO_ASPECT') for i in pc_list_items]
    cc_list_items = [tuple(c.strip().split('|||')) for c in cc.split()]
    cc_list = [i[0] for i in cc_list_items]
    cc_list_aspect = [(i[1]  if len(i) == 2 else NA) for i in cc_list_items]
    '''
    cc_list = cc.split()
    cc_list_aspect = cc_a.split()
    pc_list = pc.split()
    pc_list_aspect = pc_a.split()

    w_list = [pc_list[-1]] + cc_list

    lms = 0.0
    features = []
    # compute aspect based features...
    a_list = [a + '_i-1' for a in pc_list_aspect if a != NA] + [a + '_i' for a in cc_list_aspect if a != NA]
    a_list.reverse()
    aspect_feature = []
    for a_idx, a in enumerate(a_list):
        if a.endswith('_i-1') and len(aspect_feature) == 0:
            break
        aspect_feature.append(a)
        if a.split('_')[0] in df_no_eps:
            break
        else:
            pass
    aspect_feature.reverse()
    # compute lm based features...
    for w_idx, w in enumerate(w_list[1:]):
        w2 = w
        w1 = w_list[w_idx]
        s = lm_score(lm, w1, w2)
        features.append(('LMF-'+ w1 + '-' + w2, s))
        #sys.stderr.write(w1 + '|' + w2 + '-' + str(s) + " \n")
        lms += s
    features.append(('LM-', lms))

    if len(aspect_feature) > 1:
        aspect_feature = '-'.join(aspect_feature)
        features.append((aspect_feature, 1.0))
    return '\t'.join([f + '\t' + str(f_val) for f,f_val in features  ])


def load_lm(lm_file):
    lm  = {}
    return lm
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
                'python get_lm_features.py '
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
    sys.stderr.write('loading lm...')
    giga_lm = load_lm(options.lm_file)
    deletions = {}
    seen = {}
    sent_list = codecs.open(options.gec_raw_file, 'r', 'utf8').readlines()
    pos_list = codecs.open(options.gec_pos_file, 'r', 'utf8').readlines()
    nf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.nf_file, 'r', 'utf8').readlines())
    vf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.vf_file, 'r', 'utf8').readlines())
    df = [item.strip() for item in codecs.open(options.df_file, 'r', 'utf8').readlines()  if item.strip() != '']
    df_no_eps = [_ for _ in df if _ != '<eps>']
    pf = [item.strip() for item in codecs.open(options.pf_file, 'r', 'utf8').readlines() if item.strip() != '']
    prof = [item.strip() for item in codecs.open(options.prof_file, 'r', 'utf8').readlines() if item.strip() != '']
    all_candidates = []
    for sent, pos_sent in zip(sent_list, pos_list)[:1]:
        sys.stderr.write('sent:' + sent)
        #sys.stderr.write('pos:' + pos_sent)
        trellis = []
        trellis_aspect = []
        trellis.append([BOS])
        trellis_aspect.append([NA])
        words = sent.strip().split()
        pos = pos_sent.strip().split()
        for i, (w, p) in enumerate(zip(words, pos)):
            #sys.stderr.write('word:' + w + ' pos:' + p + '\n')
            if p.startswith('VB') and check_dictionary(w) and w in vf:
                #sys.stderr.write('in vf\n')
                vf_words = [_.split('|||')[0] for _ in vf[w]]
                vf_aspect = [_.split('|||')[1] for _ in vf[w]]
                trellis.append(vf_words) #TODO:correct the treatment of the vf tags...
                trellis_aspect.append(vf_aspect)
            elif p.startswith('DT') and w.lower() in df:
                #sys.stderr.write('in dt or rb\n')
                trellis.append(df)
                trellis_aspect.append(df)
            elif p in ["NN" , "NNS"]  and check_dictionary(w) and w in nf:
                #sys.stderr.write('in nn\n')
                #sys.stderr.write('len(nf[w]) ' + str(len(nf[w])) + '\n')
                nf_words = [_.split('|||')[0] for _ in  nf[w]]
                nf_aspect = [_.split('|||')[1] for _ in  nf[w]]
                detxnf_words = [' '.join(item).strip() for item in itertools.product(df_no_eps, nf_words)]
                detxnf_aspect = [' '.join(item).strip() for item in itertools.product(df_no_eps, nf_aspect)]
                #if w.lower().strip() in giga_lm:
                #    detxnf = [dbigram for dbigram in detxnf if dbigram.lower() in giga_lm] 
                #else:
                #    pass
                detxnf_words += nf_words
                detxnf_aspect += nf_aspect
                #sys.stderr.write(str(len(detxnf)) +',')
                assert len(detxnf_words) > 0
                trellis.append(detxnf_words)
                trellis_aspect.append(detxnf_aspect)
            elif p.startswith('JJ') or p.startswith('RB'):
                #sys.stderr.write('in jj\n')
                detxjj_words = [' '.join(item).strip() for item in itertools.product(df_no_eps, [w])]
                detxjj_aspect = [' '.join(item).strip() for item in itertools.product(df_no_eps, [NA])]
                #if w.lower().strip()  in giga_lm:
                #    detxjj = [dbigram for dbigram in detxjj if dbigram.lower() in giga_lm]
                #else:
                #    pass
                detxjj_words += [w]
                detxjj_aspect += [NA]
                #sys.stderr.write(str(len(detxjj)) +',')
                assert len(detxjj_words) > 0
                trellis.append(detxjj_words)
                trellis_aspect.append(detxjj_aspect)
            elif p.startswith('PRP') and w.lower() in prof:
                #Pronouns
                #sys.stderr.write('in prp\n')
                if w not in prof:
                    prof += [w]
                trellis.append(prof)
                trellis_aspect.append([NA for _ in prof])
            elif p.startswith('IN') and w.lower() in pf:
                #Prepositions
                trellis.append(pf) 
                trellis_aspect.append([NA for _ in pf])
            else:
                #sys.stderr.write(w + ' is not in any pos tag...\n')
                trellis.append([w])
                trellis_aspect.append([NA])
            if len(trellis[-1]) >= 1:
                pass
            else:
                sys.stderr.write(w + ' is the w\n')
                sys.stderr.write('\n' + str(trellis) + '\n')
                exit(1)
        trellis.append([EOS])
        trellis_aspect.append([NA])
        for idx,(current_candidates, current_aspects)  in enumerate(zip(trellis[1:], trellis_aspect[1:])):
            #pdb.set_trace()
            i = idx+1
            assert type(current_candidates) == type([])
            assert type(current_aspects) == type([])
            prev_candidates = trellis[i - 1]
            prev_aspects =  trellis_aspect[i - 1]
            assert type(prev_candidates) == type([])
            assert type(prev_aspects) == type([])
            for pc, pc_a in zip(prev_candidates, prev_aspects):
                assert pc != EOS
                pc = pc.strip()
                pc_a = pc_a.strip()
                for cc, cc_a in zip(current_candidates, current_aspects):
                    assert cc != BOS
                    cc = cc.strip()
                    cc_a = cc_a.strip()
                    state_pc = ' '.join([_w+'|||'+ _a if _w != _a and _a != NA else _w for _w, _a in  zip(pc.split(), pc_a.split())])
                    state_cc = ' '.join([_w+'|||'+ _a if _w != _a and _a != NA else _w for _w, _a in  zip(cc.split(), cc_a.split())]) 
                    # ask keisuke how this works...
                    bigram_state = 'BIGRAM ### ' + state_pc + ' ### ' + state_cc
                    if not bigram_state in seen:
                        seen[bigram_state] = 1
                        print bigram_state + ' ### ' + lm_features(giga_lm, pc, pc_a, cc, cc_a)
    sys.stderr.write('done\n')
