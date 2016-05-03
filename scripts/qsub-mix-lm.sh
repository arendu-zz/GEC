#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=10G,ram_free=10G
#$ -V
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.mix.log
set -e
. ~/.bashrc
source ~/.profile
DATA_DIR=/home/arenduc1/Projects/GEC/data/gec
ngram -lm $DATA_DIR/train/conll14st-preprocessed.m2.mod.eps.arpa -mix-lm $DATA_DIR/giga.lm.1.bigram.only.limited.vocab -lambda 0.871233 -write-lm $DATA_DIR/giga.train.interpolated.lm.limited.vocab -order 2

