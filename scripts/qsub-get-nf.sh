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
EXP="/home/arenduc1/export/agiga-deps"
$GEC_HOME/scripts/get_nform_candidates.py -f $EXP/agiga.medium.raw -l $EXP/agiga.medium.lemma -p $EXP/agiga.medium.pos > $GEC_HOME/data/candidates/agiga.medium.nform_candidates

