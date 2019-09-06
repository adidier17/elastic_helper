"""
For local testing without docker only. This is a script I am using to test the individual components of mica that post to
elasticsearch before I containerize the solution.
"""


from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os
import logging
import sys
import json

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class ElasticHelper:
    def __init__(self, es_url=None, index_name=None, doc_type=None):
        if es_url == None:
            base_url = os.getenv("ES_BASE_URL")
            # if base_url == None:
            #     base_url = "localhost"
            es_url = "http://" + base_url + ":9200"
        logging.info("Setting elasticsearch url to %s", es_url)
        self.es = Elasticsearch(es_url)
        self.index_name = index_name
        if self.index_name == None:
            self.index_name = os.getenv("ES_INDEX_NAME")
        self.doc_type = doc_type
        if self.doc_type == None:
            self.doc_type = os.getenv("ES_DOC_TYPE")

    def create_index(self, mapping):
        res = self.es.indices.create(self.index_name, body=mapping)
        logging.info(json.dumps(res))

    def delete_index(self):
        res = self.es.indices.delete(index=self.index_name)
        logging.info(json.dumps(res))

    def index_doc(self, doc, id, **kwargs):
        res = self.es.index(index=self.index_name, doc_type=self.doc_type, body=doc, id=id, **kwargs)
        logging.info(json.dumps(res))

    def data_gen(self, data, op_type):
        for doc in data:
            doc2index = doc
            if op_type == "update":
                doc2index = {"doc": doc, "doc_as_upsert":True}
            yield {
                "_index": self.index_name,
                "_op_type": op_type,
                "_type": self.doc_type,
                "_id": doc["fpath"],
                "_source": doc2index
            }

    def bulk_index_data(self, data, **kwargs):
        bulk(self.es, self.data_gen(data, "index"), **kwargs)

    def bulk_update_docs(self, data, **kwargs):
        bulk(self.es, self.data_gen(data, "update"), **kwargs)

    def get_data(self, size=1):
        matchall_Query = {"query": {
            "match_all": {}
        },
            "size": size
        }
        res = self.es.search(index=self.index_name, body=matchall_Query)
        return res

    def get_doc_by_id(self, id, **kwargs):
        res = self.es.get(index=self.index_name, doc_type=self.doc_type, id=id, **kwargs)
        return res

    def get_doc_by_fpath(self, fpath, **kwargs):
        query = {"query": {
            "match": {"fpath": fpath
                      }}
        }
        res = self.es.search(index=self.index_name, body=query, **kwargs)
        return res

    def query(self, query, **kwargs):
        res = self.es.search(index=self.index_name, body=query, **kwargs)
        return res
