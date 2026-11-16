---
name: ragPipelineProduction
description: Production-grade RAG pipeline implementing BM25 and dense vector hybrid search, Reciprocal Rank Fusion (RRF), cross-encoder reranking (Cohere/BGE), and semantic caching. Use when building reliable, hallucination-resistant retrieval systems.
version: 2.x
last-verified: 2026-11-15
compatibility: Python 3.10+, LangChain, LlamaIndex, Qdrant/pgvector, Cohere API
---

# Production RAG Pipeline Engineering Guide

## 1. The Production Architecture (Why Naive RAG Fails)
Naive RAG (vector search alone) fails in 30–40% of production queries because embedding models compress exact keywords (SKUs, IDs, error codes). The industry standard is a 3-stage pipeline:

```
┌─────────────────┐       ┌─────────────────┐
│   BM25 Lexical  │       │  Dense Vector   │
│  Exact keywords │       │ Semantic intent │
└────────┬────────┘       └────────┬────────┘
         │                         │
         └───────────┬─────────────┘
                     ▼
       ┌───────────────────────────┐
       │ Reciprocal Rank Fusion    │  Merges top-100 candidates
       │ RRF_score = Σ 1/(60 + r)  │  (Zero tuning, sub-millisecond)
       └─────────────┬─────────────┘
                     ▼
       ┌───────────────────────────┐
       │   Cross-Encoder Rerank    │  Evaluates [Query + Document] together
       │ (Cohere v3 / BGE-reranker)│  Shrinks top-100 to top-3/5
       └─────────────┬─────────────┘
                     ▼
       ┌───────────────────────────┐
       │   LLM Context Window      │  Clean, ultra-high relevancy chunks
       └───────────────────────────┘
```

---

## 2. Canonical Hybrid + RRF Implementation Pattern

```python
from typing import List, Dict

def reciprocal_rank_fusion(
    bm25_results: List[Dict], 
    vector_results: List[Dict], 
    k: int = 60, 
    top_n: int = 50
) -> List[Dict]:
    """
    Fuses two disparate ranked lists using Reciprocal Rank Fusion.
    Score = sum(1 / (k + rank))
    """
    rrf_scores = {}
    doc_lookup = {}

    # 1. Score BM25 results
    for rank, doc in enumerate(bm25_results, start=1):
        doc_id = doc["id"]
        doc_lookup[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # 2. Score Dense Vector results
    for rank, doc in enumerate(vector_results, start=1):
        doc_id = doc["id"]
        doc_lookup[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # 3. Sort by aggregated RRF score
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    return [doc_lookup[doc_id] for doc_id in sorted_ids[:top_n]]
```

---

## 3. Reranker Integration (Cohere v3)

```python
import cohere

co = cohere.ClientV2(api_key="COHERE_API_KEY")

def rerank_documents(query: str, candidate_chunks: List[Dict], top_k: int = 5):
    docs = [chunk["text"] for chunk in candidate_chunks]
    response = co.rerank(
        model="rerank-v3.5",
        query=query,
        documents=docs,
        top_n=top_k
    )
    
    top_chunks = []
    for item in response.results:
        selected = candidate_chunks[item.index]
        selected["relevance_score"] = item.relevance_score
        top_chunks.append(selected)
    return top_chunks
```

---

## 4. Anti-Patterns & Pitfalls
- ❌ **Vector-Only Search**: Never rely strictly on cosine similarity for catalog, medical, or legal queries containing exact IDs or product codes. Always pair with BM25.
- ❌ **Score Addition without Normalization**: Never directly add raw BM25 scores (0–100+) to cosine distances (-1 to 1). Always use **RRF** (ordinal ranking).
- ❌ **Stuffing 20+ Unranked Chunks**: Dumping massive unranked contexts into the LLM causes the "Lost in the Middle" problem and explodes latency. Rerank down to top 3–5 chunks.
- ❌ **Arbitrary Fixed Chunking**: Chopping text at fixed 500 characters breaks sentences mid-thought. Use semantic markdown headers or sentence splitters.

---

## 5. References & Bundled Utilities
- RRF mathematics and parameter tuning: [references/rrfAlgorithm.md](references/rrfAlgorithm.md)
- Advanced chunking strategies (Parent-Child, Contextual Retrieval): [references/chunkingStrategies.md](references/chunkingStrategies.md)
- Standalone hybrid fusion script: [scripts/runHybridRrfSearch.py](scripts/runHybridRrfSearch.py)
