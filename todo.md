### TODO

1. Remove stop words like a, an, the etc. Issue a warning to the user if a search for a stop word has been made. - done
2. Could include positions of occurences within a document.. low priority, since it is a little tougher. - not implementing
3. Will have a table where (document, frequency) will be serialized and stored for every unique word. good to sort by document ids for some reason. - done. not sorted by doc_ids
4. encoding - delta encoding - first digit as it is, remaining just difference, after sorting. - not implementing
5. sort by document id, dont need by frequency. doesnt affect BM25 - no
6. use messagepack for serialization - not serializing. takes too much time to serialize and deserialize
7. tf - idf - will try


- tf -> term frequency -> frequency of a term in a particular document -> frequency of word / doc_length
- idf -> inverse document frequency -> frequency of documents containing term -> loge(num_docs / num_docs with word)
- tf * idf => importance value  