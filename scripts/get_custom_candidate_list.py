#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdout.encoding = 'utf-8'

if __name__ == '__main__':
    opt = OptionParser()
    #insert options here
    opt.add_option('-t', dest='train_mod', default='')
    opt.add_option('--cl', dest='cl_file', default='')
    (options, _) = opt.parse_args()
    if options.cl_file == '' or options.train_mod == '':
        sys.stderr.write('Usage: python get_custom_candiate_list.py -t [train mod file] --cl [rule based candidates]\n')
        exit(1)
    else:
        pass
    cl = dict((items.split('###')[0].strip(), [i.strip() for i in items.split('###')[1].split('|||')]) for items in codecs.open(options.cl_file, 'r', 'utf8').readlines())
    edits = [e.strip() for e in codecs.open(options.train_mod, 'r', 'utf8').read().split('\n\n')]
    wrong_sent = [e.split('\n')[0][1:] for e in edits]
    changes = [ '\n'.join(e.split('\n')[1:])  for e in edits]
    er = 0
    assert len(changes) == len(wrong_sent)
    for c,ws in zip(changes, wrong_sent):
        has_issue = False
        if c.strip() is not '':
            items = c.split('|||')
            st, end = items[0].split()[1:]
            st = int(st)
            end = int(end)
            error_type = items[1].strip()
            correction = items[2].strip()
            if end - st > 1:
                er += 1
                has_issue = True
                pass
            elif end == st and error_type != 'ArtOrDet':
                er += 1
                has_issue = True
                pass
            else:
                pass

        if has_issue:
            #print ws.strip()
            #print c.strip()
            #print '\twrong:', ws.split()[st:end]
            #print '\tcorrection', correction
            pass
        else:
            print 'S ' + ws.strip()
            print c.strip()
            print ''



