#!/usr/bin/env bash
set -e
jython tagger-of.py --test data/entest --train data/entrain1k --feats data/enfeats1k > output
