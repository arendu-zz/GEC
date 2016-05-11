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
$GEC_HOME/scripts/get_nform_candidates.py -f $GEC_HOME/data/gec/all.data.raw -p $GEC_HOME/data/gec/all.data.pos > $GEC_HOME/data/candidates/nform_candicates_lower

