from typing import Annotated, Literal, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from foundation.config import settings
from integrations.opik_client import get_opik_tracer, configure_opik, get_or_create_prompt

# 1. Configuration
configure_opik()

# 2. Prompt Management (Opik)
PROMPT_NAME = "syllabus-drafter-4-sessions"
PROMPT_TEMPLATE = """You are an expert curriculum designer.
Create a personalized syllabus for a student with the following profile:
- Intent: {{intent}}
- Interest: {{interest}}
- Hobby: {{hobby}}
- Driving Force: {{driving_force}}

The syllabus should be structured, engaging, and directly relate their hobbies to the subject matter.
Provide a clear breakdown for exactly 4 sessions."""

# 3. State Definition
class State(TypedDict):
    # Input variables
    intent: str
    interest: str
    hobby: str
    driving_force: str
    # Chat history
    messages: Annotated[list[BaseMessage], add_messages]

# 4. Nodes
llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
    model="ai.algo.fit/grok-4-1-fast-reasoning"
)

def syllabus_generator(state: State):
    print("--- Fetching Prompt from Opik ---")
    prompt_obj = get_or_create_prompt(PROMPT_NAME, PROMPT_TEMPLATE)
    
    # Format the prompt using the inputs from the state
    # Note: Opik prompt.format() usually returns the string. 
    # If the SDK object has a specific format method, we use that. 
    # The `prompt` attribute typically holds the string template.
    
    # Simple formatting (assuming Jinja2 syntax supported by Opik or simple replace)
    # The Opik SDK `format` method handles {{variable}} replacement.
    formatted_prompt = prompt_obj.format(
        intent=state["intent"],
        interest=state["interest"],
        hobby=state["hobby"],
        driving_force=state["driving_force"]
    )
    
    print("--- Calling LLM ---")
    messages = [HumanMessage(content=formatted_prompt)]
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# 5. Graph Construction
graph_builder = StateGraph(State)
graph_builder.add_node("syllabus_generator", syllabus_generator)
graph_builder.set_entry_point("syllabus_generator")
graph_builder.add_edge("syllabus_generator", END)
graph = graph_builder.compile()

# 6. Execution
def run_demo():
    print("Starting Syllabus Drafter (Opik Managed Prompts)...")
    
    input_data = {
        "intent": "Learn Backend Development",
        "interest": "Distributed Systems",
        "hobby": "Playing Strategy Games (like Civilization)",
        "driving_force": "To build a scalable game server",
        "messages": []
    }
    
    tracer = get_opik_tracer()
    
    import os
    
    for event in graph.stream(input_data, config={"callbacks": [tracer]}):
        for key, value in event.items():
            content = value['messages'][-1].content
            print(f"\nNode '{key}':")
            print(f"Response:\n{content}")
            print("-" * 20)
            
            # Save to Markdown
            output_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(output_dir, "syllabus.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Saved output to: {output_path}")

if __name__ == "__main__":
    run_demo()
