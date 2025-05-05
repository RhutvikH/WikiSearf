from db_utils.populate_db import add_documents_to_db
from db_utils.utils import show_some_entries, find_word, show_document, get_doc_db_size, bm_get_word_idf, get_top_docs, get_avg_doc_length, get_docs
from db_utils.db_init import create_tables

import numpy as np
import os


def main(query: str) -> None:
    db_path: str = os.path.join(os.getcwd(), "db", "wikip_db.db")
    doc_path: str = "/home/marcusholloway/Documents/wiki/small_wikip.xml.gz"

    # print(os.path.exists("db/wikip_db.db"))
    # create_tables(db_path)
    # add_documents_to_db(db_path, doc_path)
    # show_some_entries(db_path)
    # doc_ids: list = find_word(db_path, "history")
    # print(db_len)
    # for doc_id in doc_ids:
    #     show_document(db_path, doc_id)
    # print(get_word_idf(db_path, "mechanics"))

    db_size: int = get_doc_db_size(db_path)
    avg_doc_length: float = get_avg_doc_length(db_path)
    # print(db_size)
    best_doc_ids, num_docs = get_top_docs(db_path, query, 10, db_size, avg_doc_length)

    # for id in best_doc_ids:
        # show_document(db_path, id)
        # print("\n")
    return get_docs(db_path, best_doc_ids), num_docs


if __name__ == "__main__":
    main()
