# raglens (Python SDK)

Python SDK for RagLens. Instruments your RAG pipeline with 3 lines of code.

**Status**: v0.0.1 skeleton. Real implementation lands Week 2.

## Install (once published)

```bash
pip install raglens
# or
uv add raglens
```

## Usage (target API)

```python
from raglens import RAGTrace

tracer = RAGTrace(api_key="rl_...", project="my-rag-app")

with tracer.trace(query="what is RAG?") as t:
    chunks = retriever.get_relevant_documents("what is RAG?")
    t.log_retrieval(chunks)
    answer = llm.invoke(build_prompt(chunks))
    t.log_generation(answer)
```

## Design principles

- **Zero-blocking**: main thread only appends to an in-memory buffer; HTTP happens on a background flush task.
- **Silent failure**: no SDK exception ever propagates to user code.
- **Minimal deps**: only `httpx` and `pydantic`.
- **Strict semver**: any public-API break bumps major; deprecation warnings live for 2 minor versions.
