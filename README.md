# AccessGuard AI

An AI-ready accessibility auditing assistant that helps developers identify, understand, and fix common web accessibility issues.

AccessGuard AI analyzes websites against WCAG accessibility principles, detects violations, groups repeated problems, calculates an accessibility score, and provides clear developer-focused recommendations.

---

## Problem

Web accessibility is often overlooked during development.

Existing accessibility tools usually produce long technical reports containing hundreds of violations, making it difficult for developers to understand:

- What is wrong?
- Who is affected?
- Why does it matter?
- How can it be fixed?

AccessGuard AI bridges this gap by transforming accessibility testing into an understandable developer workflow.

---

## Solution

AccessGuard AI provides:

- Automated website accessibility scanning
- WCAG-based issue detection
- Severity classification
- Smart issue grouping to reduce duplicate errors
- Accessibility scoring dashboard
- Developer-friendly explanations
- Suggested implementation fixes

Instead of only reporting errors, AccessGuard AI explains the impact behind them.

---

# Features

## Accessibility Audit Engine

Analyzes websites for common WCAG issues including:

- Missing alternative text for images
- Incorrect heading hierarchy
- Unlabeled form inputs
- Empty or unclear links
- Button accessibility issues

---

## WCAG Mapping

Each detected issue includes:

- WCAG success criterion
- Conformance level
- Severity
- Affected elements

Example:

```
WCAG 1.1.1
Level A
Missing alternative text
```

---

## Smart Issue Grouping

Large websites can contain hundreds of similar accessibility problems.

AccessGuard AI groups identical violations together.

Example:

```
Missing alt text

Occurrences: 25
First seen: Image element
```

This keeps reports readable and actionable.

---

## Accessibility Scoring

The system calculates:

- Overall accessibility score
- Category-level scores
- Passed checks
- Failed checks

Example:

```
Accessibility Score: 95%

Images: 79%
Forms: 100%
Headings: 90%
Buttons: 100%
Links: 96%
```

---

## AI-Ready Explanation Engine

The explanation layer converts technical violations into developer guidance:

### Problem
Explains what is wrong.

### User Impact
Describes how accessibility users are affected.

### Recommended Solution
Provides a practical fix.

### Corrected Implementation
Shows an example implementation.

The architecture is designed to support future LLM integration.

---

# Architecture

```
              Website URL
                  |
                  v
        Playwright Web Crawler
                  |
                  v
        HTML Accessibility Parser
                  |
                  v
          WCAG Rules Engine
                  |
                  v
          Issue Deduplication
                  |
                  v
          Accessibility Scorer
                  |
                  v
       AI Explanation Generation
                  |
                  v
          React Dashboard
```

---

# Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS

## Backend

- Python
- FastAPI
- Uvicorn

## Analysis Engine

- Playwright
- BeautifulSoup
- Custom WCAG rule engine

## Testing

- Pytest

## Deployment

- Docker

---

# Project Structure

```
AI-Accessibility-Auditor/

├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── docs/
└── README.md
```

---

# Installation

## Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

playwright install chromium
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```
http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# Testing

Run backend tests:

```bash
cd backend

pytest tests/ -v
```

Current test coverage includes:

- Accessibility rules
- Issue grouping
- Scoring calculations
- Report structure validation

---

# Current Limitations

This is an MVP prototype.

Currently:

- Audits a provided URL only
- Does not crawl an entire website
- Does not simulate screen readers
- Does not perform advanced visual contrast analysis
- Uses template-based explanations instead of a connected LLM

---

# Future Improvements

Planned improvements:

- GPT-powered accessibility explanations
- Multi-page website crawling
- Automated contrast analysis
- Keyboard navigation testing
- Accessibility trend tracking
- Persistent scan history

---

# Screenshots

## Accessibility Dashboard

<img width="1280" height="711" alt="Screen Shot 2026-07-15 at 1 28 14 PM" src="https://github.com/user-attachments/assets/8a8f9a43-6d45-4555-8453-0aae29b6448d" />


## Issue Detection And AI Insight Engine

<img width="1277" height="652" alt="Screen Shot 2026-07-15 at 1 19 19 PM" src="https://github.com/user-attachments/assets/adccf43a-10f0-4666-af26-f5d70fd18dd2" />

<img width="1277" height="712" alt="Screen Shot 2026-07-15 at 1 19 57 PM" src="https://github.com/user-attachments/assets/d82d2c76-e6f5-456b-923d-f92e1c296220" />

---

# Why AccessGuard AI?

Accessibility tools should not only tell developers what is broken.

They should help developers understand why it matters and how to fix it.

AccessGuard AI transforms accessibility auditing from a checklist into an actionable development assistant.
