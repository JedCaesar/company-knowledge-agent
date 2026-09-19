# Company Knowledge Agent

A small, transparent AI assistant pattern for answering employee questions from trusted company data. It retrieves relevant policy documents, classifies the requested task, and returns citations instead of inventing an answer.

## Why this project

Useful enterprise agents need more than a chat interface. They need grounded context, explicit task routing, confidence signals, and an honest refusal path. This repository implements those foundations without hiding the behavior behind an external model.

## Features

- Local TF-IDF retrieval with no external API key
- Intent routing for leave, expenses, and security requests
- Source citations and confidence scores
- Refusal when the knowledge base cannot support an answer
- CLI entry point and automated tests

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
company-agent "How do I submit an expense claim?"
python -m unittest discover -s tests
```

Example response:

```json
{
  "answer": "Expense claims require an itemized receipt and manager approval.",
  "intent": "expense_claim",
  "confidence": 0.28,
  "citations": ["handbook/expense-policy"]
}
```

## Architecture

`KnowledgeBase` builds a lightweight searchable index. `CompanyAgent` classifies the request, retrieves evidence, creates a concise response, and exposes its sources. The components are deliberately separate so a production vector database or LLM can replace either layer without rewriting the workflow.

## Production roadmap

- Add role-based document access
- Replace local retrieval with hybrid vector and keyword search
- Add tool approval policies and audit events
- Evaluate retrieval quality against a labeled question set

## Responsible use

The included policies and company are fictional. This is a portfolio demonstration, not a production HR or security system.
