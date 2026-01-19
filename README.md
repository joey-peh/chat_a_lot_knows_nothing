# Chat-a-Lot Knows Nothing

## The Problem

<<<<<<< HEAD
As a software engineer working with UCS documentation, I waste **hours** every week doing this:

- Reading 200+ page PDFs  
- Searching through badly OCR’d legacy documents  
- Trying to remember what “provable debt” actually means in this specific regulatory context  
- Cross-referencing five different documents that slightly contradict each other  

All this just to answer very basic domain questions like:

> “What exactly **is** a provable debt?”  
> “What counts as a contingent liability here?”  
> “Is this still the current treatment under the latest circular?”

The volume is overwhelming, the signal-to-noise ratio is terrible, and most importantly:  
**I’m supposed to be writing code, not becoming an amateur lawyer/accountant.**

## What I Actually Want

A brutally simple, zero-friction way to ask domain-expert-level questions and get answers **grounded only in the documents I give it**, without:

- Sending sensitive docs to third-party APIs  
- Waiting 30 seconds for a 400-page context window to process  
- Getting hallucinated “best practices” from internet training data  
- Needing to write perfect prompts every time

## My Desired Solution (2025–2026 version)

A **local-first / self-hosted chatbot** that:

- Lets me drag-and-drop the 8–25 most important PDFs / Word docs / circulars  
- Builds a compact, accurate knowledge base **only** from those files  
- Answers short, direct questions in < 5–8 seconds  
- Shows the **exact paragraph(s)** + document name + page number it used  
- Has **zero privacy leakage** — everything stays on my machine / company VPC  
- Doesn’t try to be clever or “chatty” when I just want a definition

Example interaction I want:

**Me:** What is a provable debt?  
**Bot:**  
In the context of the MAS Notice 1114 and the Companies (Winding Up) Rules:

A **provable debt** is any debt or liability (present or future, certain or contingent) to which the company was subject at the commencement of winding up, or to which it becomes subject before dissolution by reason of an obligation incurred before commencement.

Key exclusions:  
- debts whose value is unascertainable at the relevant date  
- certain foreign currency obligations after cut-off (see s. 327)

**Source:**  
- Companies Act 1967 s 327(1) & s 327(3) [p. 184–185]  
- MAS Notice 1114 para 6.2.1 [p. 22]  
- winding-up-rules-reg-84.pdf [p. 41]

Just that. Fast. Precise. No fluff. No made-up examples.
=======
## My Solution
A chatbot that lets me upload documents for the model to understand and prioritise knowledge directly from them, 
raises no privacy concerns, and answers simple questions like “What is provable debt?” in just seconds.

## Architecture
UI: Streamlit
Orchestration Layer: Django + LangGraph
Data & Knowledge Base: Postgres SQL/ChromaDB(Vector)/Pinecone(Vector)
Model & Integration Layer:
Deployment:
Hosting:
>>>>>>> 794a3974913ab11808ac939d202d6a478a939239
