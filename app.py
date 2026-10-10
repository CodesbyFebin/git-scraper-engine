"""
Git Search Command Center
ChatGPT-style dashboard for multi-platform Git repo search + AI descriptions.
Run: streamlit run app.py
"""

import streamlit as st
import os
from git_scraper_engine import GitSearchEngine

st.set_page_config(
    page_title="Git Search Command Center",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like dark terminal feel (CodesbyFebin style)
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stChatMessage { background-color: #161b22; border-radius: 8px; }
    h1, h2, h3 { color: #00ff00; font-family: 'Courier New', monospace; }
    .repo-card { background: #010409; border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin: 8px 0; }
    .star { color: #ffd700; }
    a { color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Git Search Command Center")
st.caption("Search GitHub • GitLab • Bitbucket • Query rewriting • Multi-model cascade • Caching • Free-tier optimized")

# Sidebar config
with st.sidebar:
    st.header("⚙️ Engine Config")
    github_token = st.text_input("GitHub Token (optional)", type="password", help="Raises rate limit to 5000/hr")
    gitlab_token = st.text_input("GitLab Token (optional)", type="password")
    groq_key = st.text_input("Groq API Key (free tier)", type="password",
                             help="Get free key at console.groq.com — enables multi-model cascade")
    model = st.selectbox("Preferred Model (cascade starts here)", 
                         ["openai/gpt-oss-20b", "llama-3.1-8b-instant", "qwen/qwen3-32b", "llama-3.3-70b-versatile"], 
                         index=0)
    max_results = st.slider("Max results", 3, 15, 6)
    platforms = st.multiselect("Platforms", ["github", "gitlab", "bitbucket"], default=["github"])
    deep_crawl = st.checkbox("Deep crawl file tree (top result)", value=False)
    st.divider()
    st.markdown("**Phase 1 Upgrades Active**\n- Language-aware query rewriting\n- Multi-model cascade fallback\n- Exact + semantic-style caching\n- Language filter detection")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "engine" not in st.session_state:
    st.session_state.engine = None

# Rebuild engine if config changes
if github_token or gitlab_token or groq_key:
    st.session_state.engine = GitSearchEngine(
        github_token=github_token or None,
        gitlab_token=gitlab_token or None,
        groq_api_key=groq_key or None,
        preferred_model=model
    )

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("What are you looking for? (e.g. kotlin android full stack, rust web framework, python scraper)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching Git platforms and generating descriptions..."):
            engine = st.session_state.engine or GitSearchEngine(preferred_model=model)
            raw = engine.search(prompt, max_results=max_results, platforms=platforms)
            enriched = []
            for repo in raw:
                if "error" not in repo and "note" not in repo:
                    enriched.append(engine.enrich_and_describe(repo))
                else:
                    enriched.append(repo)

            # Format reply
            reply = f"**Found {len(enriched)} repositories for:** `{prompt}`\n\n"
            for i, repo in enumerate(enriched, 1):
                if "error" in repo:
                    reply += f"**Error:** {repo['error']}\n\n"
                    continue
                if "note" in repo:
                    reply += f"**Note:** {repo['note']}\n\n"
                    continue
                stars = "⭐" * min(5, repo["stars"] // 1000 + 1)
                reply += f"""### {i}. [{repo['name']}]({repo['html_url']})
**{repo['platform']}** • {stars} {repo['stars']} stars • `{repo.get('language') or 'Multi'}` • Updated {repo['updated']}

{repo.get('ai_description', 'No description')}

---
"""
                if deep_crawl and i == 1:
                    tree = engine.crawl_file_tree(repo)
                    if tree:
                        reply += "**File tree (sample):**\n"
                        for f in tree[:15]:
                            reply += f"- `{f['path']}` ({f['type']})\n"
                        reply += "\n"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.sidebar.markdown("---")
st.sidebar.caption("Built by CodesbyFebin • systems that prove what happened")
