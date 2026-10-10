# Git Search Command Center

**Next-generation AI-powered multi-platform Git search engine.**

- **Live demo**: [GitHub Pages](https://codesbyfebin.github.io/git-scraper-engine/) (static UI, public GitHub API)
- **Full engine**: Python package with Phase 1–3 architecture

## Features

### Phase 1 (Implemented)
- Language-aware query rewriting (preserves identifiers)
- Multi-model cascade fallback (free-tier optimized)
- Two-tier caching (exact + description)
- Language filter detection
- Streamlit ChatGPT-style dashboard

### Phase 2 (Architected)
- Hybrid indexing with Tree-sitter ASTs
- Keyword + embedding + graph retrievers
- Chat-with-repo mode

### Phase 3 (Architected)
- Clone-and-Analyze sandbox mode
- Dynamic test execution + static analysis
- Secure ephemeral environments

## Quick Start (full engine)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional keys: `GROQ_API_KEY`, `GITHUB_TOKEN`, `GITLAB_TOKEN`.

## Static Demo
The `index.html` powers the GitHub Pages site. Enable Pages in repo Settings → Pages → Deploy from branch → `main` / `/ (root)`.

Built by **CodesbyFebin** — systems that prove what happened.
