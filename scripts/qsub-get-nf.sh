#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=10G,ram_free=10G
#$ -V
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.nf.log
set -e
. ~/.bashrc
source ~/.profile
GEC_HOME="/home/arenduc1/Projects/GEC"
$GEC_HOME/scripts/get_nform_candidates.py -f $GEC_HOME/data/gec/train/conll14st-preprocessed.m2.mod.raw -p $GEC_HOME/data/gec/train/conll14st-preprocessed.m2.mod.pos > $GEC_HOME/scripts/train.nf 
$GEC_HOME/scripts/get_nform_candidates.py -f $GEC_HOME/data/gec/dev/official-preprocessed.5types.m2.mod.raw -p $GEC_HOME/data/gec/dev/official-preprocessed.5types.m2.mod.pos > $GEC_HOME/scripts/dev.5types.nf 
$GEC_HOME/scripts/get_nform_candidates.py -f $GEC_HOME/data/gec/dev/official-preprocessed.m2.mod.raw -p $GEC_HOME/data/gec/dev/official-preprocessed.m2.mod.pos > $GEC_HOME/scripts/dev.nf 
$GEC_HOME/scripts/get_nform_candidates.py -f $GEC_HOME/data/gec/test/official-2014.combined.m2.mod.raw -p $GEC_HOME/data/gec/test/official-2014.combined.m2.mod.pos > $GEC_HOME/scripts/test.nf 
touch $GEC_HOME/scripts/all.nf
cat $GEC_HOME/scripts/train.nf >> $GEC_HOME/scripts/all.nf
cat $GEC_HOME/scripts/dev.5types.nf >> $GEC_HOME/scripts/all.nf
cat $GEC_HOME/scripts/dev.nf >> $GEC_HOME/scripts/all.nf
cat $GEC_HOME/scripts/test.nf >> $GEC_HOME/scripts/all.nf
cat $GEC_HOME/scripts/all.nf | sort | uniq > $GEC_HOME/data/candidates/nform_candidates

