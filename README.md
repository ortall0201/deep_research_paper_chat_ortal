# CrewAI Flow Workshop - Intelligent Research & Conversation System

This project demonstrates an advanced AI system built with [CrewAI Flow](https://crewai.com) that intelligently routes between research and conversation modes. The system can conduct comprehensive academic research using multiple databases and maintain natural conversations with users.

## Project Overview

This is an **intelligent routing system** that:

1. **Analyzes user intent** - Determines whether a message needs research or conversation
2. **Conducts deep research** - Searches academic databases (arXiv, Nature, IEEE, PubMed) for scholarly papers
3. **Maintains conversations** - Provides natural, contextual responses for non-research queries
4. **Preserves context** - Tracks conversation history across interactions

### Key Features

- **Smart Intent Routing**: Automatically classifies user messages as research or conversation
- **Academic Research**: Searches multiple scholarly databases with proper citations
- **Conversation Memory**: Maintains message history throughout the session
- **Custom Tools**: Integrated deep research capabilities via Firecrawl API
- **Flow Orchestration**: Uses CrewAI Flow for complex multi-agent workflows

## Getting Started from Scratch

### 1. Install CrewAI

First, install CrewAI globally:

```bash
pip install crewai[tools]
```

### 2. Create a New Flow Project

Generate a new CrewAI flow project:

```bash
crewai create flow your_flow_name
cd your_flow_name
```

### 3. Setup Environment

Ensure you have Python >=3.10 <3.14 installed. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

Install UV if you haven't already:

```bash
pip install uv
```

Install project dependencies:

```bash
crewai install
```

### 4. Configure API Keys

Create a `.env` file in your project root and add your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

**Required API Keys:**
- **OpenAI API Key**: For LLM functionality and intent routing
- **Firecrawl API Key**: For academic research and paper searching

## Understanding the System Architecture

### Flow Structure

The main flow (`PoemFlow`) orchestrates three key components:

1. **Intent Router** (`routing_intent`)
   - Analyzes user messages using GPT-4 mini
   - Classifies intent as "research" or "conversation"
   - Generates optimized research queries when needed

2. **Research Handler** (`handle_research`)
   - Creates specialized research agent
   - Uses `DeepResearchPaper` tool for academic searches
   - Returns structured results with citations

3. **Conversation Handler** (`follow_up_conversation`)
   - Provides natural conversational responses
   - Maintains context from message history
   - Guides users toward research opportunities when appropriate

### Custom Tools

- **DeepResearchPaper**: Searches academic databases and returns exactly 5 research papers with full content and proper citations

## Installation & Setup

Ensure you have Python >=3.10 <3.14 installed on your system.

1. Clone this repository or use it as a template
2. Install dependencies:

```bash
crewai install
```

3. Configure your `.env` file with required API keys
4. Run the system:

```bash
crewai run
```

## Customization Guide

### Modifying from the Base Template

Starting from a fresh CrewAI flow, here's how to adapt it for this research system:

1. **Update Flow State** (`FlowState` class):
   - Add message history tracking
   - Include research query handling
   - Add intent classification fields

2. **Implement Intent Routing**:
   - Create router method with LLM classification
   - Define research vs conversation criteria
   - Add proper prompt engineering

3. **Add Research Capabilities**:
   - Integrate research tools (Firecrawl API)
   - Create specialized research agent
   - Implement structured output formatting

4. **Build Conversation System**:
   - Add conversation handler
   - Implement context awareness
   - Include message history management

### Configuration Files

- **`src/crewai_flow_workshop1/main.py`**: Main flow logic and orchestration
- **`src/crewai_flow_workshop1/tools/deep_research_paper.py`**: Research tool implementation
- **`pyproject.toml`**: Project configuration and dependencies

## Running the Project

Execute the flow from the project root:

```bash
crewai run
```

The system will:
1. Start with a default research query about AI trends
2. Route the message through intent classification
3. Conduct research or provide conversation response
4. Maintain message history for context

## Example Usage

### Research Query Example
```
User: "What are the latest studies on transformer architectures in 2024?"
System: → Routes to research → Returns academic papers with citations
```

### Conversation Example
```
User: "Hello, how does this system work?"
System: → Routes to conversation → Provides explanation and guidance
```

### Follow-up Research Example
```
Previous: Discussion about AI ethics
User: "Can you find more studies about bias in machine learning?"
System: → Routes to research with context → Returns relevant bias studies
```

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure both `OPENAI_API_KEY` and `FIRECRAWL_API_KEY` are set in your `.env` file
2. **Python Version**: Verify you're using Python >=3.10 <3.14
3. **Dependencies**: Run `crewai install` to ensure all packages are properly installed
4. **Research Timeout**: If research queries timeout, try more specific search terms

### Development Tips

- Use `crewai run` for full execution
- Check logs for detailed flow execution information
- Modify the default query in `FlowState` for different starting points
- Adjust research limits and timeouts in the tool configuration

## Support & Resources

For support, questions, or feedback:

- **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
- **CrewAI GitHub**: [github.com/joaomdmoura/crewai](https://github.com/joaomdmoura/crewai)
- **CrewAI Discord**: [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- **CrewAI Chat**: [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create intelligent systems together with the power and simplicity of CrewAI Flow!
