import json
import os
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class DeepResearchPaperInput(BaseModel):
    """Input schema for DeepResearchPaper tool."""

    query: str = Field(
        default="",
        description="Research query to search for academic papers (e.g., 'machine learning transformers', 'agentic ai systems')",
    )
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
    
    def __init__(self, **data):
        # Handle case where agent passes description instead of query
        if 'description' in data and 'query' not in data:
            data['query'] = data.pop('description')
        elif not data.get('query') and len(data) == 1:
            # If only one field is passed, use it as query
            data['query'] = list(data.values())[0]
        super().__init__(**data)


class DeepResearchPaper(BaseTool):
    name: str = "Deep Research Paper Search"
    description: str = (
        "Searches academic and research databases (arXiv, Nature, IEEE, PubMed, etc.) for scholarly papers "
        "related to your query. Returns exactly 5 research papers from the last year with titles, URLs, and descriptions. "
        "Perfect for literature reviews, research validation, and finding cutting-edge academic work."
    )
    args_schema: Type[BaseModel] = DeepResearchPaperInput

    def _run(self, query: str = None, **kwargs) -> str:
        """
        Search for academic papers using Firecrawl's research category search.

        Args:
            query: The research topic to search for

        Returns:
            JSON response containing exactly 5 research paper results from the last year
        """
        try:
            # Handle different input formats the agent might pass
            if query is None and kwargs:
                # Try to extract query from kwargs
                if 'description' in kwargs:
                    query = kwargs['description']
                elif len(kwargs) == 1:
                    query = list(kwargs.values())[0]
            
            if not query:
                return "Error: No search query provided. Please provide a research query string."
                
            # Fixed limit of 5 research papers
            limit = 5

            url = "https://api.firecrawl.dev/v2/search"

            payload = {
                "query": query,
                "sources": ["web"],
                "categories": ["research"],
                "tbs": "qdr:y",  # Search within last year
                "limit": limit,
            }

            # Get API key from environment variable
            api_key = os.getenv("FIRECRAWL_API_KEY")
            if not api_key:
                return "Error: FIRECRAWL_API_KEY environment variable is not set. Please set your Firecrawl API key."

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()

            if not data.get("success", False):
                return f"Search failed: {data.get('error', 'Unknown error occurred')}"

            else:
                return data

        except requests.exceptions.Timeout:
            return f"Search timeout for query '{query}'. Please try again with a more specific query."

        except requests.exceptions.RequestException as e:
            return f"Network error while searching for '{query}': {str(e)}"

        except json.JSONDecodeError:
            return f"Invalid response format from search API for query '{query}'. Please try again."

        except Exception as e:
            return f"Unexpected error during research search for '{query}': {str(e)}"
