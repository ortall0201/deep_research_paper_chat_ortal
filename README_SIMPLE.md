# CrewAI Research Flow

An intelligent AI research assistant that searches academic databases and provides cited summaries.

## Quick Start

1. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Research Query**
   ```bash
   python src/crewai_flow_workshop1/main.py "Your research question here"
   ```

## Examples

```bash
# Research AI trends
python src/crewai_flow_workshop1/main.py "What are the latest AI developments in 2024?"

# Research quantum computing
python src/crewai_flow_workshop1/main.py "Recent breakthroughs in quantum computing"

# Research any topic
python src/crewai_flow_workshop1/main.py "Climate change impact studies"
```

## Required API Keys

- **OpenAI API Key**: For LLM processing
- **Firecrawl API Key**: For academic paper search

Add these to your `.env` file.

## What It Does

1. Analyzes your question
2. Searches academic databases (arXiv, Nature, IEEE, PubMed)
3. Returns comprehensive research summary with citations
4. Displays source links and content previews

## Output

The system provides:
- Research summary with inline citations
- List of source papers with URLs
- Content previews for each source