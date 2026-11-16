# Reciprocal Rank Fusion (RRF) Reference

## Mathematical Definition
For a set of documents $D$ and a set of rankings $R$, the RRF score is:

$$RRF(d \in D) = \sum_{r \in R} \frac{1}{k + r(d)}$$

Where:
- $r(d)$ is the 1-based rank position of document $d$ in the current retriever.
- $k$ is the smoothing constant (canonical value is `60`).

## Why $k = 60$?
$k = 60$ prevents top-ranked documents in one retriever from completely overpowering documents that appear moderately high (e.g. position 2 to 5) across both retrievers.
