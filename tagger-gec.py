__author__ = 'arenduchintala'
import sys
import codecs
from optparse import OptionParser

import edu.jhu.hlt.optimize.AdaGradComidL2.AdaGradComidL2Prm as AdaGradComidL2Prm
import edu.jhu.pacaya.gm.decode.MbrDecoder.MbrDecoderPrm as MbrDecoderPrm
import edu.jhu.pacaya.gm.inf.BeliefPropagation.BeliefPropagationPrm as BeliefPropagationPrm
import edu.jhu.pacaya.gm.inf.BeliefPropagation.BpScheduleType as BpScheduleType
import edu.jhu.pacaya.gm.inf.BeliefPropagation.BpUpdateOrder as BpUpdateOrder
import edu.jhu.pacaya.gm.train.CrfTrainer.CrfTrainerPrm as CrfTrainerPrm
import edu.jhu.pacaya.util.semiring.LogSemiring as LogSemiring
from edu.jhu.hlt.optimize import AdaGradComidL2
from edu.jhu.pacaya.gm.data import FgExampleMemoryStore, LabeledFgExample
from edu.jhu.pacaya.gm.decode import MbrDecoder
from edu.jhu.pacaya.gm.feat import FeatureVector
from edu.jhu.pacaya.gm.model import FactorGraph, FgModel, Var, VarSet, ExplicitExpFamFactor, VarConfig, \
		ClampFactor
from edu.jhu.pacaya.gm.train import CrfTrainer

# features fired key: configuration of var set
# value list of tuples, (feature_label, feature_value)
factor_cell_to_features = {}
feature_label2id = {}
DET = 'the a an another no the a an no another some any my our their her his its another no each every certain its another no this that'.split()
PP = 'of in to for with on at from by about as into like through after over between out against during without before under around among'.split()
global fl2id, id2fl, id2fval, event2fl
global nf, vf, df,pf, prof 
BOS = '<s>'
EOS = '</s>'


class ObservedFactor(ExplicitExpFamFactor):
	def __init__(self, varset, var_list, factor_type, observed_state):
		ExplicitExpFamFactor.__init__(self, varset)
		self.var_list = var_list
		self.factor_type = factor_type
		self.observed_state = observed_state

	def getFeatures(self, configuration_id):
		vs = self.getVars()
		configuration = vs.getVarConfig(configuration_id)
		state1 = configuration.getStateName(self.var_list[0])
		# print 'vs:' , vs.calcNumConfigs()
		# print 'config_id:', configuration_id, 'config:' , state1, self.factor_type
		# print 'vars:' , self.var_list[0].name, self.observed_state
		feats_fired = factor_cell_to_features[(self.factor_type, state1, self.observed_state)]
		feat_idxs = [(feature_label2id[f_label], f_val) for f_label, f_val in feats_fired]
		feats = zip(*feat_idxs)
		return FeatureVector(list(feats[0]), list(feats[1]))

		
class CRFFactor(ExplicitExpFamFactor):
	def __init__(self, varset, var_list, factor_type):
		ExplicitExpFamFactor.__init__(self, varset)
		self.var_list = var_list
		self.factor_type = factor_type

	def getFeatures(self, configuration_id):
		global fl2id, id2fl, id2fval, event2fl
		vs = self.getVars()
		configuration = vs.getVarConfig(configuration_id)
		state1 = configuration.getStateName(self.var_list[0])
		state2 = configuration.getStateName(self.var_list[1])
		# print 'vs:' , vs.calcNumConfigs()
		# print 'config_id:', configuration_id, 'config:' , state1, state2, self.factor_type
		# print 'vars:' , self.var_list[0].name, self.var_list[1].name
		feats_fired = event2fl[(self.factor_type, state1, state2)]
		feat_ids = [fl2id[fl] for fl in feats_fired]
		feat_vals = [id2val[f_idx] for f_idx in feat_ids]
		return FeatureVector(feat_ids, feat_vals)



# This method tweaks a few defaults on the CrfTrainer, but isn't
# strictly necessary.
def get_trainer_prm():
	tr_prm = CrfTrainerPrm()
	ad_prm = AdaGradComidL2Prm()
	ad_prm.numPasses = 2  # Number of passes through the data
	ad_prm.l2Lambda = 1. / 2000.  # L2 regularizer weight
	tr_prm.batchOptimizer = AdaGradComidL2(ad_prm)
	# We can use brute force inference because the factor graph
	# consists of only a single variable and factor.
	# tr_prm.infFactory = BruteForceInferencerPrm(LogSemiring.getInstance())
	tr_prm.infFactory = BeliefPropagationPrm()
	tr_prm.infFactory.s = LogSemiring.getInstance()
	tr_prm.infFactory.schedule = BpScheduleType.TREE_LIKE
	tr_prm.infFactory.updateOrder = BpUpdateOrder.SEQUENTIAL
	tr_prm.infFactory.normalizeMessages = True
	tr_prm.infFactory.maxIterations = 1;
	tr_prm.infFactory.convergenceThreshold = 1e-3;
	tr_prm.infFactory.keepTape = True
	return tr_prm


def generate_correction_candidates(p, w, c = None):
	global nf, vf, df, prof, pf
	candidates = []
	if w == EOS:
		candidates = [EOS]
	elif w == BOS:
		candidates = [BOS]
	elif p.startswith('JJ'):
		detxjj = [' '.join(item).strip() for item in itertools.product([_ for _ in df if _ != '<eps>'], [w])]
		if w.lower().strip()  in giga_lm:
			detxjj = [dbigram for dbigram in detxjj if dbigram.lower() in giga_lm]
		else:
			pass
		detxjj += [w]
		candidates = detxjj
		pass
	elif p.startswith('PRP'):
		candidates = prof
		pass
	elif p.startswith('IN') and w in pf:
		candidates = pf
		pass
	elif p.startswith('DT') or p.startswith('RB'):
		candidates = df
		pass
	elif p.startswith('NN') and w in nf:
		detxnf = [' '.join(item).strip() for item in itertools.product([_ for _ in df if _ != '<eps>'], nf[w])]
		if w.lower().strip() in giga_lm:
			detxnf = [dbigram for dbigram in detxnf if dbigram.lower() in giga_lm] 
		else:
			pass
		detxnf+= nf[w]
		#sys.stderr.write(str(len(detxnf)) +',')
		assert len(detxnf) > 0
		candidate = detxnf
	elif p.startswith('VB') and w in vf:
		candidates = vf[w]
	else:
		pass
	if c is not None:
		assert c in candidates
	return candidates


def make_gec_instances(raw_file, pos_file, correct_file=None):
	global nf, vf, df, pf, prof
	instances = FgExampleMemoryStore()
	raw_lines = [[BOS] + rl.strip().split() + [EOS] for rl in codecs.open(raw_file, 'r', 'utf8').readlines()]
	pos_lines = [[BOS] + pl.strip().split() + [EOS] for pl in codecs.open(pos_file, 'r', 'utf8').readlines()]
	if correct_file is not None:
		correct_lines = [[BOS] + cl.strip().split() + [EOS]  for cl in codecs.open(correct_file, 'r', 'utf8').readlines()]
		pass
	else:
		correct_lines = [None] * len(raw_lines)
		pass
	for line_idx in range(len(raw_lines)):
		factor_graph = FactorGraph()
		vc = VarConfig()
		prev_hc = None
		for w_idx, (w,p,c) in enumerate(zip(raw_lines[line_idx], pos_lines[line_idx], correct_lines[line_idx])):
			candidates = generate_correction_candidates(p,w)	
			print w, p, c
			print 'can', candidates
			hc = Var(Var.VarType.PREDICTED, len(candidates), "TAG_" + str(w_idx) , candidates)
			vc.put(hc, c)
			if prev_hc:
				t_varset = VarSet(hc)
				t_varset.add(prev_hc)
				t_factor = CRFFactor(t_varset, [prev_hc, hc], "BIGRAM")
				factor_graph.addFactor(t_factor)
			else:
				pass
			prev_hc = hc
			pass
		instances.add(LabeledFgExample(factor_graph, vc))
	return instances


def make_instances(txt_file, tag_list, obs_list):
	instances = FgExampleMemoryStore()
	text_train = [t.strip() for t in open(txt_file).read().split('###/###') if t.strip() != '']
	for x in range(len(text_train)):
		factor_graph = FactorGraph()
		vc = VarConfig()
		prev_hc = None
		for i, line in enumerate(text_train[x].split('\n')):
			hidden_state = line.split('/')[1].strip()
			observed_state = line.split('/')[0].strip()
			# print 'h', hidden_state, 'o', observed_state
			# make variables with their configurations
			hc = Var(Var.VarType.PREDICTED, len(tag_list), "TAG_" + str(i), tag_list)
			vc.put(hc, hidden_state)
			# o = Var(Var.VarType.PREDICTED , len(obs_list), "OBS_" + str(i), obs_list)
			# vc.put(o, observed_state)
			# make transition factor
			if prev_hc:
				t_varset = VarSet(hc)
				t_varset.add(prev_hc)
				t_factor = CRFFactor(t_varset, [prev_hc, hc], 'TAG-TAG')
				factor_graph.addFactor(t_factor)
			else:
				pass
			prev_hc = hc
			# make emission factor
			e_varset = VarSet(hc)
			# e_varset.add(o)
			# e_factor = CRFFactor(e_varset, [hc, o], 'TAG-OBS')
			e_factor = ObservedFactor(e_varset, [hc], 'TAG-OBS', observed_state)
			factor_graph.addFactor(e_factor)
			# make clamp factor
			# c_factor = Clamper(o, obs_list.index(observed_state))
			# factor_graph.addFactor(c_factor)
		instances.add(LabeledFgExample(factor_graph, vc))
	return instances


def load_features(sparse_feats_file, lm_feats_file):
	global fl2id, id2fval, id2fl, event2fl
	fl2id = {}
	id2fl = {}
	id2fval = {}
	event2fl = {}
	return fl2id, id2fl, id2fval, event2fl
	with codecs.open(sparse_feats_file, 'r', 'utf8') as f:
		for line in f:
			factor_type, c1, c2, sf = line.strip().split('###')
			f_labels = [f_name.strip() for idx, f_name in enumerate(sf.split()) if idx % 2 == 0]
			f_vals = [float(f_val.strip()) for idx, f_val in enumerate(sf.split()) if idx % 2 == 1]
			event = (factor_type.strip(), c1.strip(), c2.strip())
			for fl, fv in zip(f_labels, f_vals):
				fl2id[fl] = fl2id.get(fl, len(fl2id))
				id2fl[fl2id[fl]] = fl
				id2fval[fl2id[fl]] = fv
			f_fired = event2fl.get(event, set([])) # will never use DefaultDict!
			f_fired.update(f_labels)
			event2fl[event] = f_fired
	with codecs.open(lm_feats_file, 'r', 'utf8') as f:
		for line in f:
			factor_type, c1, c2, lmf = line.strip().split('###')
			f_labels = [f_name.strip() for idx, f_name in enumerate(lmf.split()) if idx % 2 == 0]
			f_vals = [float(f_val.strip()) for idx, f_val in enumerate(lmf.split()) if idx % 2 == 1]
			event = (factor_type.strip, c1.strip(), c2.strip())
			for fl, fv in zip(f_labels, f_vals):
				fl2id[fl] = fl2id.get(fl, len(fl2id))
				id2fl[fl2id[fl]] = fl
				id2fval[fl2id[fl]] = fv
			f_fired = event2fl.get(event, set([]))
			f_fired.update(f_labels)
			event2fl[event] = f_fired
	return fl2id, id2fl, id2fval, event2fl


if __name__ == '__main__':
	opt = OptionParser()
	# insert options here
	opt.add_option('--test', dest='test_file', default='')
	opt.add_option('--train', dest='train_file', default='')
	opt.add_option('--pos', dest='pos_train_file', default='')
	opt.add_option('--pos-test', dest='pos_test_file', default='')
	opt.add_option('--corr', dest='correct_train_file', default='')
	opt.add_option('--nf', dest='nf_file', default='')
	opt.add_option('--vf', dest='vf_file', default='')
	opt.add_option('--prof', dest='prof_file', default='')
	opt.add_option('--df', dest='df_file', default='')
	opt.add_option('--pf', dest='pf_file', default='')
	opt.add_option('--lm-feats', dest='lm_feats_file', default='')
	opt.add_option('--sparse-feats', dest='sparse_feats_file', default='')
	(options, _) = opt.parse_args()
	if options.sparse_feats_file == '' or \
			options.lm_feats_file == '' or \
			options.correct_train_file == '' or\
			options.pos_test_file == '' or\
			options.pos_train_file == '' or\
			options.nf_file == '' or\
			options.vf_file == '' or\
			options.prof_file == '' or\
			options.df_file == '' or\
			options.pf_file == '' or\
			options.train_file == '' or\
			options.test_file == '':
				sys.stderr.write("Usage: jython tagger-gec.py "
						"--train [raw train file]\n"
						"--corr [corrected train file]\n"
						"--test [test file]\n"
						"--pos [pos for train file]\n"
						"--pos-test [pos for test file]\n"
						"--nf [noun candidates]\n"
						"--vf [verb candidates]\n"
						"--df [artordet candidates]\n"
						"--prof [pronoun candidates]\n"
						"--pf [prep candidates]\n"
						" --sparse-feats [sparse feats file]\n"
						" --lm-feats [lm feats file]\n")
				exit(1)
	else:
		pass

	nf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.nf_file, 'r', 'utf8').readlines())
	vf = dict((items.split()[0], items.split()[1:]) for items in codecs.open(options.vf_file, 'r', 'utf8').readlines())
	df = [item.strip() for item in codecs.open(options.df_file, 'r', 'utf8').readlines()  if item.strip() != '']
	pf = [item.strip() for item in codecs.open(options.pf_file, 'r', 'utf8').readlines() if item.strip() != '']
	prof = [item.strip() for item in codecs.open(options.prof_file, 'r', 'utf8').readlines() if item.strip() != '']

	sys.stderr.write("loading features... \n")
	fl2id, id2fl, id2fval, event2fl = load_features(options.sparse_feats_file, options.lm_feats_file)
	sys.stderr.write("prepare training instances... \n")
	training_instances = make_gec_instances(options.train_file, options.pos_train_file, options.correct_train_file)
	trainer = CrfTrainer(get_trainer_prm())
	factor_graph_model = FgModel(len(feature_label2id))
	sys.stderr.write("training... \n")
	trainer.train(factor_graph_model, training_instances)
	exit(1)
	sys.stderr.write("testing... \n")
	testing_instances = make_instances(options.test_file, options.pos_test_file, None)
	correct_label_count = 0
	total_lable_count = 0
	for test_idx in range(testing_instances.size()):
		test_instance = testing_instances.get(test_idx)
		gold_config = test_instance.getGoldConfig()
		decoder = MbrDecoder(MbrDecoderPrm())
		decoder.decode(factor_graph_model, test_instance)
		predicted_config = decoder.getMbrVarConfig()
		predictions = dict((v.getName(), predicted_config.getStateName(v)) for v in predicted_config.getVars() if
				v.getName().startswith('TAG'))
		gold = dict((v.getName(), gold_config.getStateName(v)) for v in gold_config.getVars() if
				v.getName().startswith('TAG'))
		assert len(gold) == len(predictions)
		for k in sorted(gold.keys()):
			print k, gold[k], predictions[k]
			if gold[k] == predictions[k]:
				correct_label_count += 1.0
			total_lable_count += 1.0
	print 'acc', float(correct_label_count / total_lable_count)
