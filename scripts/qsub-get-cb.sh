#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=10G,ram_free=10G
#$ -V
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.cb.log
set -e
. ~/.bashrc
source ~/.profile
GEC_HOME="/home/arenduc1/Projects/GEC"
$GEC_HOME/scripts/get_candidate_bigrams.py -f $GEC_HOME/data/gec/train/conll14st-preprocessed.m2.mod.raw -p $GEC_HOME/data/gec/train/conll14st-preprocessed.m2.mod.pos --nf $GEC_HOME/data/candidates/nform_candidates --vf $GEC_HOME/data/candidates/vform_candidates --df $GEC_HOME/data/candidates/artordet_candidates --pf $GEC_HOME/data/candidates/prep_candidates > train.cb
$GEC_HOME/scripts/get_candidate_bigrams.py -f $GEC_HOME/data/gec/dev/official-preprocessed.m2.mod.raw -p $GEC_HOME/data/gec/dev/official-preprocessed.m2.mod.pos --nf $GEC_HOME/data/candidates/nform_candidates --vf $GEC_HOME/data/candidates/vform_candidates --df $GEC_HOME/data/candidates/artordet_candidates --pf $GEC_HOME/data/candidates/prep_candidates > dev.cb
$GEC_HOME/scripts/get_candidate_bigrams.py -f $GEC_HOME/data/gec/dev/official-preprocessed.5types.m2.mod.raw -p $GEC_HOME/data/gec/dev/official-preprocessed.5types.m2.mod.pos --nf $GEC_HOME/data/candidates/nform_candidates --vf $GEC_HOME/data/candidates/vform_candidates --df $GEC_HOME/data/candidates/artordet_candidates --pf $GEC_HOME/data/candidates/prep_candidates > dev.5types..cb
$GEC_HOME/scripts/get_candidate_bigrams.py -f $GEC_HOME/data/gec/test/official-2014.combined.m2.mod.raw -p $GEC_HOME/data/gec/test/official-2014.combined.m2.mod.pos --nf $GEC_HOME/data/candidates/nform_candidates --vf $GEC_HOME/data/candidates/vform_candidates --df $GEC_HOME/data/candidates/artordet_candidates --pf $GEC_HOME/data/candidates/prep_candidates > test.cb
touch $GEC_HOME/scripts/all.cb
cat $GEC_HOME/scripts/train.cb >> $GEC_HOME/scripts/all.cb
cat $GEC_HOME/scripts/dev.5types.cb >> $GEC_HOME/scripts/all.cb
cat $GEC_HOME/scripts/dev.cb >> $GEC_HOME/scripts/all.cb
cat $GEC_HOME/scripts/test.cb >> $GEC_HOME/scripts/all.cb
cat $GEC_HOME/scripts/all.cb | sort | uniq > $GEC_HOME/data/candidates/candidate_bigrams

