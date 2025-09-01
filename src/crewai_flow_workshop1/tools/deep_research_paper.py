import json
import os
from typing import Optional, Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class DeepResearchPaperInput(BaseModel):
    """Input schema for DeepResearchPaper tool."""

    query: str = Field(
        ...,
        description="Research query to search for academic papers (e.g., 'machine learning transformers', 'agentic ai systems')",
    )
    limit: Optional[int] = Field(
        default=10,
        description="Maximum number of research papers to retrieve (default: 10, max: 50)",
    )
    max_age: Optional[int] = Field(
        default=172800000,
        description="Maximum age of cached content in milliseconds (default: 48 hours)",
    )


class DeepResearchPaper(BaseTool):
    name: str = "Deep Research Paper Search"
    description: str = (
        "Searches academic and research databases (arXiv, Nature, IEEE, PubMed, etc.) for scholarly papers "
        "related to your query. Returns paper titles, URLs, descriptions, and full markdown content when available. "
        "Perfect for literature reviews, research validation, and finding cutting-edge academic work."
    )
    args_schema: Type[BaseModel] = DeepResearchPaperInput

    def _run(
        self, query: str, limit: Optional[int] = 10, max_age: Optional[int] = 172800000
    ) -> str:
        """
        Search for academic papers using Firecrawl's research category search.

        Args:
            query: The research topic to search for
            limit: Maximum number of results to return (1-50)
            max_age: Maximum age of cached content in milliseconds

        Returns:
            Formatted string containing research paper results with titles, URLs, and content
        """
        try:
            # Validate and sanitize inputs
            limit = max(1, min(limit or 10, 50))  # Ensure limit is between 1-50
            max_age = max_age or 172800000

            url = "https://api.firecrawl.dev/v2/search"

            payload = {
                "query": query,
                "sources": ["web"],
                "categories": ["research"],
                "limit": limit,
                "scrapeOptions": {
                    "onlyMainContent": True,
                    "maxAge": max_age,
                    "parsers": [],
                    "formats": ["markdown"],
                },
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
