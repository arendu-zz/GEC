#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=50G,ram_free=50G
#$ -V
set -e
. ~/.bashrc
source ~/.profile
GEC_HOME="/home/arenduc1/Projects/GEC"
INP_FILE=$1
OUT_FILE=$2
$GEC_HOME/scripts/get_candidate_bigrams.py -f $INP_FILE.raw -p $INP_FILE.pos --nf $GEC_HOME/data/candidates/nform_candidates --vf $GEC_HOME/data/candidates/vform_candidates --df $GEC_HOME/data/candidates/artordet_candidates --pf $GEC_HOME/data/candidates/prep_candidates --prof $GEC_HOME/data/candidates/pronoun_candidates 2> $OUT_FILE.log > $OUT_FILE.cb

