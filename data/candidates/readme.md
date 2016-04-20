
# artordet
cat train/wsj02-21.conll |grep DT |cut -f 2 |tr "[A-Z]" "[a-z]" |sort |uniq -c |sort -nr > /home/ksakagu1/projects/gec_factor_graph/GEC/data/candidates/artordet

# prep


