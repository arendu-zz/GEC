#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=10G,ram_free=10G
#$ -V
#$ -N qsub-get-vf
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.vf.log
set -e
. ~/.bashrc
source ~/.profile
GEC_HOME="/home/arenduc1/Projects/GEC"
EXP="/home/arenduc1/export/agiga-deps"
SIZE='small'
$GEC_HOME/scripts/get_vform_candidates.py -f $EXP/agiga.$SIZE.raw -l $EXP/agiga.$SIZE.lemma -p $EXP/agiga.$SIZE.pos > $GEC_HOME/data/candidates/agiga.$SIZE.vform_candidates

