from typing import Optional
from typing_extensions import TypedDict, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class BookingDetails(TypedDict, total=False):
    patient_name: str
    doctor_name: str
    appointment_time: str
    appointment_date: str
    reason: Optional[str]    
    patient_email: Optional[str]

    class AgentState(TypedDict):
        booking_details: Optional[BookingDetails]
        messages: Annotated[list[BaseMessage], add_messages]
        next_agent: Optional[str]
        booking_complete: bool
        confirmation_sent: bool

