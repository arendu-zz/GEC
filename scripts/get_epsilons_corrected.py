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
	opt.add_option('-f', dest='mod_file', default='')
	(options, _) = opt.parse_args()
	if options.mod_file == '':
		sys.stderr.write('Usage: python get_epsilon.py -f [mod file]\n')
		exit(1)
	else:
		pass
	edits = [e.strip() for e in codecs.open(options.mod_file, 'r', 'utf8').read().split('\n\n')]

	for e in edits:
		lines = e.split('\n')
		sentence = lines[0][1:].strip().split()
		new_sentence = [s for s in sentence]
		for l in lines[1:]:
			items = l.split('|||')
			t,s,e = items[0].split()
			s = int(s)
			e = int(e)
			c = items[1]
			replaced = items[2]
			if replaced == '' and c in ['ArtOrDet', 'Prep']:
				new_sentence[s] = '<eps>'
				#print c + '\t' +  ' '.join(sentence[s-1 : e+1]) + '\t' + ' '.join(sentence[s-1:s] + ['<eps>'] + sentence[e:e+1])
			elif replaced != '':
				pass
		print ' '.join(new_sentence) 


