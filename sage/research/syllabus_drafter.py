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
PROMPT_NAME = "syllabus-drafter-exp-level"
PROMPT_TEMPLATE = """Act as an expert curriculum designer. Create a 4-session personalized syllabus (90–120 minutes per session) tailored to the mentee's experience level: {{experience_level}}.

### INPUT VARIABLES
- **Intent:** {{intent}}
- **Interest:** {{interest}}
- **Hobby:** {{hobby}}
- **Driving Force:** {{driving_force}}

### SESSION REQUIREMENTS
For each of the 4 sessions, provide:
1. **Module Title & Objective:** Define a goal linking {{interest}} to the session theme.
2. **Timed Agenda:** A bulleted breakdown totaling 90–120 minutes. Adjust complexity and pacing based on {{experience_level}}. Include:
   - Duration (e.g., [20 min])
   - Brief justification for the topic.
3. **Hobby Integration Activity:** A practical exercise connecting the session topic to {{hobby}}.
4. **Strategic Alignment:** Explain how this session advances {{intent}} through the lens of {{driving_force}}.
5. **ELI5 Analogy:** A simple analogy explaining the session's core concept to the mentee.

### CONSTRAINTS
- Sequence sessions in a logical progression from foundational to advanced.
- Ensure all time allocations are realistic for the specified {{experience_level}}.
- Use professional, encouraging language and concise formatting."""

# 3. State Definition
class State(TypedDict):
    # Input variables
    intent: str
    interest: str
    hobby: str
    driving_force: str
    experience_level: str
    # Chat history
    messages: Annotated[list[BaseMessage], add_messages]

# 4. Nodes
llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
    model="ai.algo.fit/v/gemini-3-flash"
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
        driving_force=state["driving_force"],
        experience_level=state["experience_level"]
    )
    
    # Opik may return a string or a list of messages (if chat prompt)
    if isinstance(formatted_prompt, list):
        # Flatten the list if it's already structured as messages
        # Depending on Opik SDK, it might be [{'role': 'user', 'content': '...'}]
        # We need to convert these dicts to LangChain Message objects
        messages = []
        for msg in formatted_prompt:
            if isinstance(msg, dict):
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "system":
                    from langchain_core.messages import SystemMessage
                    messages.append(SystemMessage(content=content))
                elif role == "assistant":
                    from langchain_core.messages import AIMessage
                    messages.append(AIMessage(content=content))
                else:
                    # Fallback for unknown roles to HumanMessage or handle appropriately
                    messages.append(HumanMessage(content=str(content)))
            else:
                 # If it's already a component object or unknown
                 messages.append(HumanMessage(content=str(msg)))
    else:
        # It's a string, wrap it in a single HumanMessage
        messages = [HumanMessage(content=str(formatted_prompt))]
    
    print("--- Calling LLM ---")
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
        "experience_level": "Intermediate (Knows basic Python/JS, Docker basics)",
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
