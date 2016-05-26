#/bin/sh
set -e
GD='/home/arenduc1/Projects/GEC/data/gec'
SIZE='medium'
TRAIN='agiga.'$SIZE
TEST='official-2014.combined.m2.mod'
jython tagger-unsup-gec.py --train $GD/$TRAIN.raw  --test $GD/test/$TEST.raw --pos $GD/$TRAIN.pos --pos-test $GD/test/$TEST.pos --cl $GD/$TRAIN.cl --lm-feats $GD/$TRAIN.lmf --sparse-feats $GD/$TRAIN.sf 

