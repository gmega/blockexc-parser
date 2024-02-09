echo 'cid,tree_cid,blocks,dataset_size' > uploads.csv
grep 'Stored data' *.log | rev | cut -d' ' -f2-5 | rev | sed -r 's/ /,/g;s/[a-zA-Z]+=//g' >> uploads.csv

echo 'count,cid,blocks' > downloads.csv
grep "Reading from manifest" *.log | rev | cut -d " " -f2-3 | rev | sort | uniq -c | tr -s ' ' | sed -r 's/^ //;s/ /,/g;s/[a-zA-Z]+=//g' >> downloads.csv