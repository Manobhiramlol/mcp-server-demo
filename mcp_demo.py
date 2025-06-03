from github import Github
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def list_mcp_resources():
    """List available MCP resources"""
    g = Github(os.getenv('GITHUB_TOKEN'))
    resources = g.get_resources()
    return resources

def create_mcp_resource(resource_type, data):
    """Create a new MCP resource"""
    g = Github(os.getenv('GITHUB_TOKEN'))
    return g.create_resource(resource_type, data)

if __name__ == "__main__":
    print("MCP Server Demo")
    print("Listing available resources...")
    resources = list_mcp_resources()
    for resource in resources:
        print(f"- {resource.name}")