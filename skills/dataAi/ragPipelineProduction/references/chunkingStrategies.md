# Advanced Chunking Strategies for Production RAG

1. **Parent-Child Document Chunking**:
   - Embed small chunks (e.g., 200 tokens) for precise vector matching.
   - Return the larger parent document (e.g., 1000 tokens) to the LLM for full contextual understanding.
2. **Contextual Retrieval (Anthropic Pattern)**:
   - Prepend a short LLM-generated document-level context summary (50–100 tokens) to every chunk before embedding.
   - Slashes failed retrievals by keeping isolated paragraphs grounded in the parent subject.
3. **Markdown / Structural Chunking**:
   - Split along Markdown headings (`#`, `##`, `###`) to preserve logical tables, lists, and sections intact.
