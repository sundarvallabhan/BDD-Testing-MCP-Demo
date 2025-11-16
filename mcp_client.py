"""
MCP Client for Streamlit Integration
Connects Franklin Templeton demo to BDD Testing MCP Server
"""

import requests
import json
from typing import Dict, Any, Optional

class MCPClient:
    """Client for BDD Testing MCP Server"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self._check_connection()
    
    def _check_connection(self):
        """Check if MCP server is accessible"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print(f"✅ Connected to MCP server at {self.base_url}")
                return True
        except:
            print(f"⚠️  Warning: Cannot connect to MCP server at {self.base_url}")
            print(f"   Make sure server is running: python3 bdd-testing-mcp/src/bdd_mcp/server.py")
            return False
    
    def call_tool(self, tool_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call an MCP tool"""
        url = f"{self.base_url}/tools/{tool_name}"
        
        try:
            response = requests.post(url, json=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('result')
            else:
                print(f"❌ MCP Error: {response.status_code}")
                print(response.text)
                return None
        except requests.exceptions.Timeout:
            print(f"⏰ MCP Request timed out (tool: {tool_name})")
            return None
        except Exception as e:
            print(f"❌ MCP Error calling {tool_name}: {str(e)}")
            return None
    
    def refine_story(self, user_story: str, additional_context: str = "", priority: str = "High") -> Optional[Dict[str, Any]]:
        """Refine user story using MCP"""
        return self.call_tool("bdd_refine_story", {
            "user_story": user_story,
            "additional_context": additional_context,
            "priority": priority
        })
    
    def generate_gherkin(self, refined_story: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate Gherkin scenarios using MCP"""
        return self.call_tool("bdd_generate_gherkin", {
            "refined_story": refined_story
        })
    
    def generate_code(self, gherkin_scenarios: Dict[str, Any], language: str = "Python (Playwright)", website_url: str = "") -> Optional[Dict[str, Any]]:
        """Generate test code using MCP"""
        return self.call_tool("bdd_generate_code", {
            "gherkin_scenarios": gherkin_scenarios,
            "language": language,
            "website_url": website_url
        })
    
    def execute_tests(self, test_code: Dict[str, Any], gherkin_scenarios: Dict[str, Any], headless: bool = True) -> Optional[Dict[str, Any]]:
        """Execute tests using MCP"""
        return self.call_tool("bdd_execute_tests", {
            "test_code": test_code,
            "gherkin_scenarios": gherkin_scenarios,
            "headless": headless
        })
    
    def full_workflow(
        self,
        user_story: str,
        website_url: str = "",
        additional_context: str = "",
        priority: str = "High",
        language: str = "Python (Playwright)",
        execute_tests: bool = True,
        headless: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Run complete BDD workflow using MCP"""
        return self.call_tool("bdd_full_workflow", {
            "user_story": user_story,
            "website_url": website_url,
            "additional_context": additional_context,
            "priority": priority,
            "language": language,
            "execute_tests": execute_tests,
            "headless": headless
        })
