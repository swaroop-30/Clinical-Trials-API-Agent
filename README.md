# Clinical Trial Insights Agent 🧠🔍

An agentic system built using **LangChain** and **Databricks-hosted LLMs** to query **ClinicalTrials.gov** for study information and dynamically extract relevant clinical fields based on user queries.

---

## 🚀 Project Overview
- Dynamically searches **ClinicalTrials.gov** for studies related to any disease, condition, or keyword.
- Extracts **relevant study fields** like NCT ID, official title, phase, conditions, interventions, etc., using **LLM-based prompt engineering**.
- Integrates **LangChain agents** with **external API calls** to handle multi-step, context-aware user queries.
- Powered by **Databricks LLM endpoint** (`databricks-llama-4-maverick`).

---

## 🛠️ Tech Stack
- Python
- LangChain
- Databricks LangChain Integration
- ClinicalTrials.gov REST API
- Agentic Framework (Zero-Shot ReAct Agent)
- Requests Library
