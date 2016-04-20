__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
import itertools

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'
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

    (options, _) = opt.parse_args()
    if options.gec_raw_file == '' or options.gec_pos == '' or options.nf_file == '' or options.vf_file == '':
        sys.stderr.write('Usage: '
                         'python get_candidate_bigrams.py '
                         '-f [gec raw file] '
                         '-p [pos file] '
                         '--nf [nf file] '
                         '--df [df file] '
                         '--pf [pf file] '
                         '--vf [vf file]\n')
        exit(1)
    else:
        pass

    sent_list = codecs.open(options.gec_raw_file, 'r', 'utf8').readlines()
    pos_list = codecs.open(options.gec_pos, 'r', 'utf8').readlines()
    nf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.nf_file, 'r', 'utf8').readlines())
    vf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.vf_file, 'r', 'utf8').readlines())
    df = [item.strip() for item in codecs.open(options.df_file, 'r', 'utf8').readlines()]
    pf = [item.strip() for item in codecs.open(options.pf_file, 'r', 'utf8').readlines()]

    for sent, pos_sent in zip(sent_list, pos_list):
        trellis = []
        trellis.append([BOS])
        words = sent.strip().split()
        pos = pos_sent.strip().split()
        for i, (w, p) in enumerate(zip(words, pos)):
            if p.startswith('VB'):
                trellis.append(vf[w])
            elif p.startswith('DT') or p.startswith('RB'):
                trellis.append(df)
            elif p.startswith('NN'):
                detxnf = list(itertools.product(df + [' '], nf[w]))
                trellis.append(detxnf)
            elif p.startswith('JJ'):
                detxjj = list(itertools.product(df + [' '], [w]))
                trellis.append(detxjj)
            else:
                trellis.append([w])
        trellis.append([EOS])
        for i in range(1, len(trellis) - 1):
            prev_candidates = trellis[i - 1]
            current_candidates = trellis[i]
            for pc in prev_candidates:
                for cc in current_candidates:
                    print pc, '|||', cc
