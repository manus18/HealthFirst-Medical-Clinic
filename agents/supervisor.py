from pydantic import BaseModel, Field
from config.models import llm
from agents.state import AgentState

SYSTEM_PROMPT = """You are a supervisor routing requests at AyushLife Care Clinic.
 
Analyze the user's message and route to the appropriate agent:
 
- **faq_agent**: Questions about clinic hours, location, doctors, policies, services, insurance, what to bring, parking, telehealth, lab work.
- **booking_agent**: Requests to book, schedule, or make an appointment. Also if the user is in the middle of providing booking details (name, email, doctor, date, time, reason).
- **FINISH**: The user is saying goodbye, thanks, or the conversation is complete.
 
Rules:
- If booking is in progress (booking_complete is False and user seems to be providing details), route to booking_agent.
- If unsure, route to faq_agent.
- Only route to FINISH if the user clearly wants to end the conversation."""


class RouteDecision(BaseModel):
    next_agent: str = Field(
        description="The next agent to handle the conversation."
        "Must be one of: faq_agent, booking_agent, 'FINISH'"
    )

    reasoning: str = Field(
        description="The reasoning behind the routing decision. Be concise but informative."
    )

router_llm = llm.with_structured_output(RouteDecision)

def supervisor_node(state: AgentState):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]
    if state.get("booking_complete") == False and state.get("booking_details"):
        # If booking is in progress, route to booking_agent
        messages.append({"role": "system", "content": "Note: Booking is in progress based on the current state. Route to booking_agent to continue collecting details and finilize the booking or end the conversation."})

    decision = router_llm.invoke(messages)
    return {"next_agent": decision.next_agent}
            