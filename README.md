# SmartStudy — Multi-Agent Study Planner

## Overview
SmartStudy is a multi-agent study-planning project built with Google's Agent Development Kit (ADK). It takes a student's exam-preparation constraints and coordinates specialist agents to produce a personalized day-by-day plan, then reviews and revises the plan.

## Required Student Inputs
Provide:
- Subject
- Number of days until the exam
- Current knowledge level
- Topics to cover
- Available study hours per day

The coordinator is instructed to identify missing inputs rather than inventing them.

## Agent Workflow
1. **Coordinator:** Extracts the student's requirements.
2. **Planning Agent:** Creates a planning brief for the specialist agents.
3. **Parallel study tasks:**
   - **Topic Agent:** Assigns High/Medium/Low priority, difficulty, and study focus to each supplied topic.
   - **Practice Agent:** Recommends practice activities and problem counts.
   - **Schedule Agent:** Creates a day-by-day timetable within the available time.
4. **Study Plan Writer:** Combines specialist results into a complete plan with study sessions, practice, revision, and final preparation.
5. **Review Loop:** The Review Agent checks coverage, time feasibility, practice, revision, and final-day workload. The Revision Agent updates the draft when needed. The loop is limited to two iterations.

## Project Structure
```text
smart_study/
├── agent.py
├── __init__.py              # Include if present in your project
├── requirements.txt         # Dependency list
├── .env.example             # Placeholder environment variables only
└── README.md
```

## Requirements
- Python
- Google ADK
- Access to the Gemini model configured in `agent.py`

Install dependencies if needed:
```bash
pip install google-adk
```

## Configuration
Configure credentials according to your local Google ADK / Gemini setup. If using an API key, create a local `.env` file and keep the real key private. Never include the real `.env` file or API key in a submission ZIP.

A `.env.example` may contain placeholders only. Use the exact environment variables required by your local setup.

## Run
From the parent directory containing the `smart_study` folder, activate your Python environment and run:

```bash
adk web
```

Open the ADK Web interface and select `smart_study`.

## Example Test Request
```text
Create a study plan for my Data Structures exam in 10 days.
My current level is Intermediate.
Topics: Arrays, Linked Lists, Trees, Graphs, Dynamic Programming.
I can study 3 hours per day.
```

## Expected Output
The plan should cover every supplied topic, provide topic priorities and study focus, assign realistic practice, schedule revision, include a mock test or suitable final preparation, and fit within the student's available time.

## Notes
- The configured model name is defined in `agent.py`; ensure it matches a model available to your API account.
- The project uses sequential, parallel, and loop workflows through ADK.
- Include all source files your actual project uses. Exclude `.env`, API keys, `.venv/`, `__pycache__/`, and generated files from the submission ZIP.
