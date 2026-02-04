import opik
from foundation.config import settings

import os

def configure_opik():
    # Opik reads configuration from environment variables or a local config file.
    # We can set the project name in the environment for the SDK to pick it up.
    if settings.opik_project_name:
        os.environ["OPIK_PROJECT_NAME"] = settings.opik_project_name
    
    # If using a custom URL (e.g. self-hosted), set it here too if not in .env
    if settings.opik_url:
        os.environ["OPIK_URL_OVERRIDE"] = settings.opik_url
        
    print(f"Opik configured for project: {settings.opik_project_name}")

def get_openai_client():
    """
    Returns an Opik-wrapped OpenAI client properly configured.
    """
    from opik.integrations.openai import track_openai
    from openai import OpenAI

    client = OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url
    )
    
    # Wrap the client to automatically log traces to Opik
    return track_openai(client)

def get_opik_tracer():
    """
    Returns an OpikTracer for use with LangGraph/LangChain callbacks.
    """
    from opik.integrations.langchain import OpikTracer
    from opik.integrations.langchain import OpikTracer
    return OpikTracer()

def get_or_create_prompt(name: str, template: str) -> opik.Prompt:
    """
    Fetches a prompt from Opik by name. If it doesn't exist, create it.
    """
    client = opik.Opik()
    prompt = client.get_prompt(name)
    
    if prompt is None:
        print(f"Prompt '{name}' not found. Creating new prompt.")
        prompt = client.create_prompt(name=name, prompt=template)
    
    return prompt
