#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=50G,ram_free=50G
#$ -V
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.lm.log
set -e
. ~/.bashrc
source ~/.profile
GEC_HOME="/home/arenduc1/Projects/GEC"
INP_FILE=$GEC_HOME/data/gec/all.data
OUT_FILE=$GEC_HOME/data/gec/all.data
$GEC_HOME/scripts/get_lm_features.py -f $INP_FILE.raw -p $INP_FILE.pos --nf $GEC_HOME/data/candidates/nform_candidates --vf $GEC_HOME/data/candidates/vform_candidates --df $GEC_HOME/data/candidates/artordet_candidates --pf $GEC_HOME/data/candidates/prep_candidates --prof $GEC_HOME/data/candidates/pronoun_candidates --lm $GEC_HOME/data/gec/giga.train.interpolated.lm.limited.vocab.lower   > $OUT_FILE.lmf
