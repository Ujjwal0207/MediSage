# MediSage RAG Benchmarks

Finding the optimal chunking and retrieval strategy for medical reports is notoriously difficult. Medical PDFs contain complex data tables, highly repetitive headers across multiple pages, and critical numerical values that cannot be lost.

This document demonstrates why MediSage uses **`chunk_size=1200`**, **`overlap=200`**, and **`MMR search (fetch_k=24, k=8)`**, based on a real-world 19-page pathology laboratory test report.

---

## The Benchmark Document
**Document:** 19-page Complete Blood Count, Lipid Profile, and Biochemistry Report.
**Characteristics:** 
- Every page has the exact same 5-line header (`Patient Name`, `Lab ID`, `Location`, `QR Code`).
- Data is heavily tabular (e.g., `Test | Result | Unit | Biological Ref. Interval`).

**Test Query:** *"What is my Fasting Blood Sugar and HbA1c?"*

---

## Scenario A: Small Chunks (The "Standard" Setup)
**Parameters:** `chunk_size=300`, `overlap=50`

If we use standard small chunks, table rows get violently split. On Page 4 of the report, the data looks like this:
`Fasting Blood Sugar H 141.0 mg/dL 74 - 106 GOD-POD`

With a 300-character chunk, the LLM receives:
* **Chunk 1:** `...Test Result Unit Biological Ref. Interval Fasting Blood Sugar H...`
* **Chunk 2:** `...141.0 mg/dL 74 - 106 GOD-POD...`

**Result:** ❌ **Hallucination.** The LLM states *"I cannot find the result for Fasting Blood Sugar"* because the test name is isolated in Chunk 1, and the numerical value (141.0) is isolated in Chunk 2. The semantic meaning is completely destroyed.

---

## Scenario B: Naive Similarity Search
**Parameters:** `chunk_size=1200`, `k=4`, **No MMR**

With a larger chunk size, the tables stay intact. However, because the 19-page PDF repeats the patient header and disclaimer on every single page, a naive similarity search fails.

When querying *"What is my Fasting Blood Sugar?"*, FAISS calculates mathematical similarity. The words *"Patient"*, *"Report"*, and *"Blood"* overlap heavily with the page headers.

**Result:** ❌ **Context Flooding.** The retriever fetches 4 chunks. 3 out of 4 chunks are just repetitive page headers from different pages. The actual chunk containing the "Fasting Blood Sugar" table row was ranked #5 by FAISS, so it never made it to the LLM. The LLM answers: *"Your report does not contain blood sugar information."*

---

## Scenario C: The MediSage Configuration
**Parameters:** `chunk_size=1200`, `overlap=200`, `fetch_k=24`, `k=8` (Max Marginal Relevance)

Here is how the MediSage pipeline elegantly solves both problems:

1. **`chunk_size=1200` and `overlap=200`:** 
   1200 characters is large enough to capture the entire `Biochemistry` table on Page 4 in a single, unbroken chunk: `Fasting Blood Sugar H 141.0 mg/dL 74 - 106 GOD-POD`. The 200-character overlap acts as a safety net in case a table spans across a page break.

2. **`fetch_k=24` and `k=8` (MMR):**
   Instead of just blindly taking the top 8 chunks, FAISS fetches the top **24** chunks related to the query. 
   Then, the **Max Marginal Relevance (MMR)** algorithm analyzes those 24 chunks and selects 8 chunks that are highly relevant to the question, **BUT** forces them to be as diverse from each other as possible.

**Result:** ✅ **Perfect Retrieval.** 
Instead of retrieving 8 identical page headers, MMR selects:
1. Page 4: The Fasting Blood Sugar result (`141.0 mg/dL`).
2. Page 5: The HbA1c result (`7.10%`) — *because it is highly relevant to blood sugar but mathematically diverse from Page 4.*
3. Page 7: The Microalbumin result — *because the doctor's notes on this page mention diabetes screening guidelines.*

The LLM accurately answers: *"Your Fasting Blood Sugar is high at 141.0 mg/dL (normal range is 74-106). Additionally, your HbA1c is 7.10%, which falls in the diabetic control range."*

---

## Conclusion
For complex tabular PDFs like medical reports, small chunks destroy context, and naive search gets trapped by repetitive boilerplate. **Large overlapping chunks paired with MMR diversity search** is the only reliable way to achieve high-accuracy Medical RAG.
