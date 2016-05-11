#!/bin/sh
set -e
GD='/home/arenduc1/Projects/GEC/data/gec'
TRAIN='conll14st-preprocessed.m2.mod'
TEST='official-2014.combined.m2.mod'
CAN='/home/arenduc1/Projects/GEC/data/candidates'
jython tagger-gec.py --train $GD/train/$TRAIN.raw --corr $GD/train/$TRAIN.raw.correct --test $GD/test/$TEST.raw --pos $GD/train/$TRAIN.pos --pos-test $GD/test/$TEST.pos --nf $CAN/nform_candidates --vf $CAN/vform_candidates --df $CAN/artordet_candidates --prof $CAN/pronoun_candidates --pf $CAN/prep_candidates --lm-feats $GD/all.data.lmf --sparse-feats $GD/all.data.sf

