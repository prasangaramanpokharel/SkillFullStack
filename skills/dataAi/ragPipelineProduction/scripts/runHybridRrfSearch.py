#!/usr/bin/env python3
"""
runHybridRrfSearch.py
Self-contained Reciprocal Rank Fusion (RRF) ranker utility for merging search results.
"""

import json
import argparse

def rrf(bm25_list, vector_list, k=60, top_n=5):
    scores = {}
    docs = {}

    for rank, doc in enumerate(bm25_list, 1):
        doc_id = doc["id"]
        docs[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    for rank, doc in enumerate(vector_list, 1):
        doc_id = doc["id"]
        docs[doc_id] = doc
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    ranked = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [{"id": d_id, "score": scores[d_id], "text": docs[d_id].get("text", "")} for d_id in ranked[:top_n]]

if __name__ == "__main__":
    # Quick self-test
    bm25_mock = [{"id": "doc1", "text": "Error ERR-901 in database"}, {"id": "doc2", "text": "Setup configuration"}]
    vector_mock = [{"id": "doc3", "text": "Connection troubleshooting"}, {"id": "doc1", "text": "Error ERR-901 in database"}]

    fused = rrf(bm25_mock, vector_mock, k=60, top_n=2)
    print(f"Fused RRF Top Result: {fused[0]['id']} with score {fused[0]['score']:.4f}")
