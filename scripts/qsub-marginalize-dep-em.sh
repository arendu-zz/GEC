#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=5G,ram_free=5G
#$ -V
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.marginalize.dep.em.log
set -e
. ~/.bashrc
source ~/.profile
DEP_EM='/home/arenduc1/export/agiga-deps'
GEC_HOME='/home/arenduc1/Projects/GEC'
$GEC_HOME/scripts/marginalize_dep_embeddings.py -c $DEP_EM/agiga.dep.context.embeddings > $DEP_EM/agiga.context.embeddings
