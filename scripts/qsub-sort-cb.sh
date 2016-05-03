#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=10G,ram_free=10G
#$ -V
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.sort.cb.log
set -e
. ~/.bashrc
source ~/.profile
GEC_HOME="/home/arenduc1/Projects/GEC"
touch $GEC_HOME/scripts/all.cb
echo "train"
cat $GEC_HOME/scripts/train.cb  | sort >> $GEC_HOME/scripts/all.cb
echo "dev 5 types"
cat $GEC_HOME/scripts/dev.5types.cb | sort  >> $GEC_HOME/scripts/all.cb
echo "dev"
cat $GEC_HOME/scripts/dev.cb | sort  >> $GEC_HOME/scripts/all.cb
echo "test"
cat $GEC_HOME/scripts/test.cb | sort  >> $GEC_HOME/scripts/all.cb
echo "all"
cat $GEC_HOME/scripts/all.cb | sort  > $GEC_HOME/data/candidates/candidate_bigrams

