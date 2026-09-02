import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

import clinic_mcp_server as srv

load_dotenv()

# 1. Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

# 2. String-safe MCP Tools
@tool
def get_available_doctors(specialization: str = "") -> str:
    """Fetch list of doctors, their specialization, available days, hours, and fee."""
    res = srv.get_available_doctors(specialization)
    if not res:
        return "No doctors found for the specified specialization."
    return json.dumps(res)

@tool
def check_doctor_booked_slots(doctor_id: int, appointment_date: str) -> str:
    """Check all booked time slots for a specific doctor on a given date (YYYY-MM-DD)."""
    res = srv.check_doctor_booked_slots(doctor_id, appointment_date)
    if not res:
        return "All time slots are currently available for this date (No prior bookings)."
    return json.dumps(res)

@tool
def book_appointment(patient_name: str, phone_number: str, doctor_id: int, appointment_date: str, time_slot: str) -> str:
    """Book a new clinic appointment for a patient after confirming availability."""
    res = srv.book_appointment(patient_name, phone_number, doctor_id, appointment_date, time_slot)
    return json.dumps(res)

tools = [get_available_doctors, check_doctor_booked_slots, book_appointment]
llm_with_tools = llm.bind_tools(tools)

# 3. System Prompt
system_prompt = SystemMessage(
    content="""You are Sara, the front desk coordinator and appointment manager at CarePulse Medical Center.

PERSONALITY & TONE:
- Act like a real, helpful human receptionist—warm, quick, and professional.
- DO NOT say "Salam" or greet in every message. Only greet once at the start.
- Match user language (Roman Urdu / English).
- Never mention "I am an AI bot/model".

WORKFLOW:
1. When asked about doctors, fetch details using `get_available_doctors`.
2. When patient wants to book:
   - Collect name, phone number, doctor ID/name, preferred date (YYYY-MM-DD), and time slot.
   - Run `check_doctor_booked_slots` to ensure slot is free.
   - Run `book_appointment` and provide the Reference ID clearly.
3. Keep replies clear and concise."""
)

# 4. Define Graph Nodes
def call_model(state: MessagesState):
    messages = [system_prompt] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# 5. Build Graph
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

carepulse_app = workflow.compile()