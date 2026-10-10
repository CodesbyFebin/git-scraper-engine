# Phase 2 & 3 Architecture Notes

## Phase 2: Hybrid Indexing (Tree-sitter)
- Integrate `tree-sitter` + language grammars for AST/CST parsing
- AST-aware chunking (functions, classes) instead of naive splits
- Three retrievers:
  1. Keyword / trigram inverted index (Zoekt/Tantivy style)
  2. Embedding index (CodeBERT / UniXcoder → vector DB)
  3. Graph-based (dependency / call graph via Tree-sitter queries)
- Merge + re-rank results
- "Chat with repo" mode using retrieved chunks as context

## Phase 3: Clone-and-Analyze
- Secure ephemeral sandbox (Modal / E2B / Runloop / Firecracker / gVisor)
- Workflow: clone → mount restricted FS → run tests/linters/Semgrep → capture output → sanitize → terminate
- Static analysis: dependency graphs, anti-pattern queries, security scans
- Dynamic analysis: pytest / npm test / etc. (when test suite exists)
- Structured report generation

## Current Status
Phase 1 (query rewrite, multi-model cascade, caching) is implemented in `git_scraper_engine.py`.
Phase 2/3 are architected and ready for incremental implementation.
The static `index.html` powers the GitHub Pages demo using the public GitHub Search API.
