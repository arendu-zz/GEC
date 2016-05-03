#!/bin/bash
#$ -cwd
#$ -S /bin/bash
#$ -M adithya.renduchintala@jhu.edu
#$ -m eas
#$ -l mem_free=10G,ram_free=10G
#$ -V
#$ -j y -o /home/arenduc1/Projects/GEC/scripts/qsub.mix.factor.log
set -e
DATA_DIR=/home/arenduc1/Projects/GEC/data/gec
FULL_LM=$DATA_DIR/giga.lm.1.bigram.only.limited.vocab
TRAIN_LM=$DATA_DIR/train/conll14st-preprocessed.m2.mod.eps.arpa
DEV_TXT=$DATA_DIR/dev/alldev.m2.mod.eps
ngram -lm $TRAIN_LM -ppl $DEV_TXT -debug 2 > dev-train.ppl
ngram -lm $FULL_LM -ppl $DEV_TXT -debug 2 > dev-full.ppl
compute-best-mix dev-train.ppl dev-full.ppl > mix.lm.factor

