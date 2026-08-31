# PetroSense — Intelligent Fuel Station Management Assistant

<p align="center">
  <strong>AI-powered assistant for monitoring, analyzing, and managing a fuel station network</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python">
  <img src="https://img.shields.io/badge/Streamlit-Framework-red?logo=streamlit">
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite">
  <img src="https://img.shields.io/badge/RAG-Enabled-purple">
  <img src="https://img.shields.io/badge/LLM-Powered-green">
</p>

---

## Overview

**PetroSense** is an intelligent assistant designed to support the management and analysis of a network of fuel stations.

The system combines structured operational data, internal documents, RAG, natural-language SQL generation, LLM-based reasoning, data visualization, and hybrid analysis.

It allows users to interact with the station network using natural language.

## Features

- Natural-language interaction with the station network
- SQL-based analysis of structured data
- Retrieval-Augmented Generation (RAG)
- Hybrid analysis combining SQL and documents
- Conversational context handling
- Data visualization
- Maintenance and stock analysis
- Anomaly detection
- Data-driven recommendations

## Architecture

PetroSense follows a modular architecture composed of:

- **Simulation** — generates station, pump, inventory, transaction, complaint, and maintenance data
- **ETL** — validates, transforms, and loads data into SQLite
- **RAG** — processes documents, creates embeddings, stores vectors, and retrieves relevant context
- **SQL Agent** — generates and executes SQLite queries from natural-language questions
- **Hybrid Agent** — combines structured SQL data with retrieved documents
- **Chart Agent** — generates data visualizations
- **Router** — determines the appropriate processing path
- **Streamlit** — provides the user interface
- **Evaluation** — measures the assistant's performance

```text
                         ┌──────────────────────┐
                         │         User         │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │   Context Resolver   │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │        Router        │
                         └──────────┬───────────┘
      ┌─────────────────────────────┬─────────────────────────────────┐
   general                       hybrid                             chart
      │                             │                                 │
      │                             ▼                                 ▼
      │                      ┌──────────────┐                   ┌────────────┐    
      │                      │ Hybrid Agent │                   │ Chart Agent│    
      │                      └──────┬───────┘                   └─────┬──────┘   
      │                     ┌────────────────┐                        │           
      │                     ▼                ▼                        │
      │              ┌────────────┐     ┌────────────┐                │
      │              │ RAG Agent  │     │ SQL Agent  │◄───────────────┘     
      │              └─────┬──────┘     └─────┬──────┘     
      │                    ▼                  ▼                  
      │              ┌────────────┐     ┌────────────┐           
      │              │ Documents  │     │   SQLite   │           
      │              │ Vector DB  │     │  Database  │           
      │              └────────────┘     └────────────┘           
      │                    │                  │                  
      │                    └────────┬─────────┘                  
      │                             ▼                            
      │                      ┌──────────────┐                    
      └─────────────────────►│     LLM      │
                             │   Response   │
                             └──────┬───────┘
                                    ▼
                             ┌──────────────┐
                             │ Final Answer │
                             └──────────────┘
```

## Technologies

Python · Streamlit · SQLite · Groq · LLM · RAG · Vector Search · Embeddings · Matplotlib · Pandas · LangChain

## Project Structure

```text
smart-fuel-station-assistant/
│
├── simulator/
│   ├── LLM/
│   ├── stations.py
│   ├── pumps.py
│   ├── inventory.py
│   └── simulation_engine.py
│
├── data/
│
├── ETL/
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── RAG/
│   ├── chunker.py
│   ├── embedder.py
│   ├── retriever.py
│   ├── vector_store.py
│   └── rag_pipeline.py
│
├── vectore_store/
│
├── agent/
│   ├── assistant.py
│   ├── chart_agent.py
│   ├── context_resolver.py
│   ├── conversation.py
│   ├── database.py
│   ├── hybrid_agent.py
│   ├── prompts.py
│   ├── rag_agent.py
│   ├── router.py
│   └── sql_agent.py
│
├── database/
│   └── station.db
│
├── evaluation/
│   ├── evaluation_dataset.json
│   ├── evaluator.py
│   └── generate_ground_truth.py
│
├── interface/
│   └── streamlit_app.py
│
├── main.py
├── requirements.txt
├── config.py
├── .gitignore
└── .env
```

## Installation
```bash
git clone https://github.com/userKk1/smart-fuel-station-assistant.git
cd smart-fuel-station-assistant
pip install -r requirements.txt
```
## Configuration
Create a .env file in the project root:
 
`GROQ_API_KEY=your_api_key`

## Usage
First initialize the project:

`python main.py`

Then start the Streamlit application:

`streamlit run streamlit_app.py`

## Contributors

Developed as a final-year internship project by :

[Khadija Alhyane](https://github.com/userKk1) and [Oumaima L'brek](https://github.com/Oumaima-lb)
