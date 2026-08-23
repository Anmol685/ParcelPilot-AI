import streamlit as st
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_documents
from excel_tools import get_order, get_account, get_ticket

load_dotenv()

st.set_page_config(
    page_title="ParcelPilot AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ParcelPilot AI Support Agent")
st.caption("Internal Operations Support Chatbot")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

# ---------- Session ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Hello! Ask me about orders, tickets, policies or agreements."
    }]

if "pending_ticket" not in st.session_state:
    st.session_state.pending_ticket = None

# ---------- Chat History ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Escalation UI ----------
if st.session_state.pending_ticket:

    ticket = st.session_state.pending_ticket

    st.warning(f"Create escalation for **{ticket}** ?")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Confirm Escalation", use_container_width=True):
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"## ✅ Escalation Created\n\nTicket **{ticket}** has been successfully escalated to Tier-2 Support."
            })
            st.session_state.pending_ticket = None
            st.rerun()

    with c2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Escalation cancelled."
            })
            st.session_state.pending_ticket = None
            st.rerun()

# ---------- User Input ----------
prompt = st.chat_input("Ask your question...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    upper = prompt.upper()

    try:

        # Order
        if upper.startswith("ORD-"):
            reply = get_order(upper.strip())

        # Account
        elif upper.startswith("ACCT-"):
            reply = get_account(upper.strip())

        # Ticket
        elif upper.startswith("TKT-"):
            reply = get_ticket(upper.strip())

        # Escalation
        elif upper.startswith("ESCALATE"):

            ticket = upper.replace("ESCALATE", "").strip().upper()

            if not ticket.startswith("TKT-"):
                reply = "❌ Invalid Ticket ID. Example: TKT-501"

            else:
                st.session_state.pending_ticket = ticket
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Escalation prepared for **{ticket}**.\n\nClick **✅ Confirm Escalation** above."
                })
                st.rerun()

        # PDF + Gemini
        else:

            context = search_documents(prompt)

            final_prompt = f"""
You are ParcelPilot AI.

Answer ONLY from the supplied context.

Context:
{context}

Question:
{prompt}
"""

            response = llm.invoke(final_prompt)

            if isinstance(response.content, list):
                reply = ""
                for part in response.content:
                    if hasattr(part, "text"):
                        reply += part.text
                    elif isinstance(part, dict) and part.get("type") == "text":
                        reply += part.get("text", "")
            else:
                reply = str(response.content)

        if not upper.startswith("ESCALATE"):
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })
            st.rerun()

    except Exception as e:

        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
            reply = "⚠️ Daily Gemini free quota exceeded. Please try again later."

        else:
            reply = f"❌ Error: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })
        st.rerun()