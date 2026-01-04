# Django API Tutorial App: From Basics to Performance

## Objective

This tutorial walks you through building a **Django REST API** step by step, evolving it across **five versions**. Each version improves **robustness, security, and performance**, while teaching **how to measure and compare metrics** like latency, throughput, and concurrency.

By the end, you’ll understand not just *how* to build APIs, but *why* certain design choices matter for performance and reliability.

---

## Prerequisites

* Python 3.10+
* Basic Python & HTTP knowledge
* Virtual environments (`venv`)
* PostgreSQL

---

## Tech Stack

* Django
* Django REST Framework (DRF)
* PostgreSQL
* Gunicorn Web Server
* Locust / JMeter
* Postman

---

## Project Overview

We’ll build a simple **Notes API**:

* Create notes
* List notes
* Secure endpoints
* Optimize queries
* Handle high concurrency

```
notes_api/
├── notes/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── management/commands/
│       └── seed_notes.py
├── notes_api/
│   ├── settings.py
│   └── urls.py
```

---

# Version 1 – Basic API (Baseline)

* This version only has a simple model, serializer, and `ViewSet` endpoints with router
* No pagination, indexes
* Datebase rows: 10K
* see the git commit with tag `V1.0`

## Version 1 Performance Results

### Test Setup

* **Server**: Gunicorn (2 workers, 1 thread each)
* **Database**: Default relational DB (no indexes added manually)
* **Dataset size**: 10,000 notes
* **Endpoint tested**: `GET /notes/`
* **Payload size**: ~11 MB JSON response
* **Concurrency**: 1 (sequential requests)
* **Tool**: ApacheBench (`ab`)

Command used:

```bash
ab -n 1000 -c 1 http://127.0.0.1:8000/notes/
```

---

### Measured Metrics

| Metric               | Value             |
| -------------------- | ----------------- |
| Average latency      | ~476 ms           |
| Median latency (P50) | ~446 ms           |
| P95 latency          | ~621 ms           |
| Max latency          | ~1079 ms          |
| Throughput           | ~2.1 requests/sec |
| Failed requests      | 0                 |
| Response size        | ~11 MB            |

---

### Interpretation of Results

These results represent a **true baseline** for the API.

Key characteristics of Version 1:

* ❌ **No pagination**: every request loads and serializes all 10,000 rows
* ❌ **No indexing**: database performs a full table scan
* ❌ **No filtering or search**: no query narrowing
* ❌ **No authentication**: no security overhead
* ❌ **No caching**: every request hits the database and serializer
* ❌ **No data validation**: no limit of length of note (title / content), any value is accepted

As a result:

* Latency is dominated by **serialization cost and response size**, not database speed
* Throughput is very low because each request transfers a large payload
* Tail latency (P95 / max) grows due to CPU and memory pressure during JSON serialization

---

### Why This Is an Intentional Design

Version 1 is intentionally **unoptimized**.

This allows us to:

* Quantify the real cost of returning large datasets
* Establish a stable performance baseline
* Objectively measure improvements introduced in later versions

Every future optimization (pagination, indexing, search, caching, concurrency tuning) will be evaluated **against these exact numbers**.

---

| Metric      | Result     |
| ----------- | ---------- |
| Avg Latency | ~50ms      |
| Throughput  | ~100 req/s |
| Error Rate  | ~0%        |

---

# Version 2 – Validation & Error Handling

### Goals

- Ensure API is safe and predictable

- Validate input data and return meaningful HTTP errors

- Prevent invalid data from entering the database

#### Changes from V1

- Field-level validation added for title and content

- Proper HTTP status codes for invalid input

- Predictable error responses

- Still no pagination, indexing, authentication, or caching

---

### Example Error Response

- POSTing empty data:
- 
```json
{
    "title": ["Title cannot be empty."],
    "content": ["Content cannot be empty."]
}
```

- Status code: `400 Bad Request`

- Generated automatically by DRF based on field definitions

### Summary

- Version 2 improves reliability and correctness without changing performance significantly:
  - Prevents empty or invalid notes
  - Provides clear, consistent error messages
  - Sets foundation for further improvements (authentication, pagination, search)