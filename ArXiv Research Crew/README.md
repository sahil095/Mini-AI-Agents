# ArXiv Research Crew

A multi-agent AI system that finds the **top 10 research papers** published on ArXiv for a given date and compiles them into an HTML report. Built with [CrewAI](https://www.crewai.com/) and Groq.

## What This Project Does

1. **Researcher agent** — Uses a custom ArXiv tool to fetch papers from selected categories (e.g. `cs.CL`) submitted on a target date, then ranks and selects the top 10 based on title and abstract.
2. **Frontend engineer agent** — Takes the researcher’s list and generates a styled HTML report (`ai_research_report.html`) with clickable titles, authors, and short summaries.

The notebook walks through: environment setup, API checks (Groq + Serper), custom tool definition, agent and task configuration, crew assembly, and running the pipeline with a date input.

## Prerequisites

- **Python 3.10+**
- **API keys:**
  - **GROQ_API_KEY** — For the LLM (Groq). Get one at [console.groq.com](https://console.groq.com/).
  - **SERPER_API_KEY** — For web search (optional; used in the Serper test cell). Get one at [serper.dev](https://serper.dev/).

## How to Run Locally

### 1. Clone or open the project

```bash
cd "ArXiv Research Crew"
```

(Or open the `ArXiv Research Crew` folder in your editor.)

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD) / macOS / Linux:**

```bash
source venv/Scripts/activate   # Windows CMD
source venv/bin/activate       # macOS / Linux
```

### 3. Install dependencies

From the **project root** (parent of `ArXiv Research Crew`):

```bash
pip install -r requirements.txt
```

Or install from inside `ArXiv Research Crew` if you have a local `requirements.txt`:

```bash
pip install openai python-dotenv crewai crewai_tools arxiv groq
```

### 4. Set up environment variables

Create a `.env` file in the **project root** (or in `ArXiv Research Crew` if you run the notebook from there) with:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

Replace the placeholders with your real keys. The notebook loads them with `python-dotenv` and `os.getenv()`.

### 5. Run the notebook

1. Open `notebook.ipynb` in Jupyter Lab, Jupyter Notebook, or VS Code.
2. Run the cells **in order** from top to bottom.
3. The first few cells check Groq and Serper; then the crew is defined and run.
4. When you run the last cell (`arxiv_research_crew.kickoff(inputs=crew_inputs)`), you will be prompted for a **date** (or it will use the default in `crew_inputs`). Enter a date in `YYYY-MM-DD` format.
5. After the researcher and frontend engineer finish, the report is written to **`ai_research_report.html`** in the same folder. Open it in a browser to view the top 10 papers.

### Optional: Fix date handling in the ArXiv tool

If you see an error like `'str' object has no attribute 'strftime'`, the LLM is passing the date as a string. In the `FetchArxivPapersTool._run` method, convert the input to a date before use, for example:

```python
def _run(self, target_date) -> List[dict]:
    if isinstance(target_date, str):
        target_date = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
    # ... rest of the method
```

## Project Structure

```
ArXiv Research Crew/
├── README.md                 # This file
├── notebook.ipynb            # Step-by-step notebook with explanations
└── ai_research_report.html   # Generated report (after running the crew)
```

## Reference

- [Building Your First AI Agent](https://www.intoai.pub/p/building-your-first-ai-agent) — Substack walkthrough for the modules used in this notebook.
