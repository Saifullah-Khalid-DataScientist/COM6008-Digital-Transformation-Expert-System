# 🚀 COM6008 Digital Transformation Expert System

A Knowledge-Based Expert System developed for the COM6008 Knowledge-Based 
Systems in AI module at Buckinghamshire New University. The system assesses 
small business digital maturity using 25 expert production rules across 6 
capability domains and delivers prioritised transformation recommendations.

## What the System Does

Small businesses often struggle with digital transformation because expert 
guidance is expensive and hard to access. This system fills that gap by acting 
as an intelligent consultant. A business owner answers 19 diagnostic questions 
about their current digital capabilities, and the inference engine evaluates 
their responses against 25 IF-THEN production rules using forward chaining 
logic. The system then produces a maturity score out of 100, a risk level, 
and a full set of prioritised recommendations, all presented through an 
interactive web dashboard with downloadable PDF report.

## Knowledge Domains Covered

The 25 rules are organised across 6 capability domains:

1. Infrastructure — cloud adoption, cybersecurity, backup, mobile access
2. Data and Intelligence — analytics, data management, performance tracking
3. Automation and AI — process automation, AI tools, agile methods
4. Customer and Market — CRM, digital platforms, digital marketing
5. Strategy and Governance — digital strategy, leadership, IT governance
6. People and Collaboration — training, collaboration tools, remote working

## Maturity Levels

The system classifies businesses into three maturity tiers based on their 
total score:

- Early Stage Digital Business — score below 42
- Developing Digital Business — score between 42 and 71
- Advanced Digital Business — score 72 and above

## Technologies Used

- Python 3
- Streamlit — web interface and user interaction
- Matplotlib and NumPy — data visualisation and charts
- ReportLab — PDF report generation

## How to Run the Application

Clone the repository to your local machine:

git clone https://github.com/Saifullah-Khalid-DataScientist/COM6008-Digital-Transformation-Expert-System.git

Navigate into the project folder:

cd COM6008-Digital-Transformation-Expert-System

Install the required dependencies:

pip install -r requirements.txt

Run the Streamlit application:

streamlit run app.py

The application will open automatically in your browser at localhost:8501.

## Project Files

- app.py — Streamlit frontend, user interface, charts, and PDF export
- advisor_engine.py — Rule engine, 25 production rules, inference logic, 
  risk assessment, and recommendation generator
- requirements.txt — Python dependencies
- README.md — Project documentation

## Knowledge Sources 🧠

The expert rules in this system were derived from two established digital 
maturity frameworks:

- McKinsey Digital Maturity Framework 2023
- Gartner IT Maturity Model 2024

These frameworks provided the evidence base for determining which digital 
capabilities matter most for small business performance and in what order 
they should be prioritised.

## Module Information

- Module: COM6008 Knowledge-Based Systems in AI
- Institution: Buckinghamshire New University
- Academic Year: 2025 to 2026
- Assessment: CW1 Expert System Implementation
