#!/usr/bin/env python3
"""
Test script for the DeepResearchPaper tool.
Tests the tool functionality and displays results.
"""

import os
import json
from src.crewai_flow_workshop1.tools.deep_research_paper import DeepResearchPaper

def test_tool():
    """Test the DeepResearchPaper tool with various scenarios."""
    print("🔬 Testing DeepResearchPaper Tool")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("❌ FIRECRAWL_API_KEY environment variable not set!")
        print("Please set it with: export FIRECRAWL_API_KEY='your-api-key'")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    print()
    
    # Initialize the tool
    research_tool = DeepResearchPaper()
    
    # Test cases
    test_cases = [
        {
            "name": "Small Query Test",
            "query": "machine learning transformers",
            "limit": 2,
            "max_age": 172800000
        },
        {
            "name": "AI Agents Research",
            "query": "agentic ai systems",
            "limit": 3,
            "max_age": 172800000
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Query: '{test_case['query']}'")
        print(f"Limit: {test_case['limit']}")
        print("-" * 30)
        
        try:
            result = research_tool._run(
                query=test_case['query'],
                limit=test_case['limit'],
                max_age=test_case['max_age']
            )
            
            # Check if result is a string (error) or dict (success)
            if isinstance(result, str):
                print(f"❌ Error or formatted response: {result[:200]}...")
            elif isinstance(result, dict):
                print("✅ Received JSON response!")
                
                # Display summary of results
                if result.get("success"):
                    data = result.get("data", {})
                    web_results = data.get("web", [])
                    print(f"📊 Found {len(web_results)} research papers")
                    
                    # Show first result details
                    if web_results:
                        first_paper = web_results[0]
                        print(f"📝 First paper: {first_paper.get('title', 'No title')[:80]}...")
                        print(f"🔗 URL: {first_paper.get('url', 'No URL')}")
                        print(f"📄 Has content: {'Yes' if first_paper.get('markdown') else 'No'}")
                else:
                    print(f"❌ API returned error: {result.get('error', 'Unknown error')}")
            else:
                print(f"❓ Unexpected response type: {type(result)}")
                
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            
        print("\n" + "=" * 50 + "\n")
    
    print("🎯 Testing complete!")
    return True

def display_tool_info():
    """Display tool information."""
    tool = DeepResearchPaper()
    print("🛠️  Tool Information:")
    print(f"Name: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Input Schema: {tool.args_schema.__name__}")
    print()

if __name__ == "__main__":
    display_tool_info()
    test_tool()



