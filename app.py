import streamlit as st
from tools import (
    search_documents,
    get_excel_info,
    get_order,
    get_ticket,
    ai_reply,
    create_escalation
)

st.set_page_config(
    page_title="ParcelPilot AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ParcelPilot AI Support Agent")
st.write("Ask me about orders, tickets, policies or escalations.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_ticket" not in st.session_state:
    st.session_state.pending_ticket = None

# Show history
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

# Chat input
q = st.chat_input("Type your question...")

if q:

    st.session_state.messages.append(("user", q))

    # Excel info
    if q.lower() == "excel":
        answer = get_excel_info()

    # Order lookup
    elif q.upper().startswith("ORD-"):
        answer = get_order(q)

    # Ticket lookup
    elif q.upper().startswith("TKT-"):
        answer = get_ticket(q)

    # Escalation
    elif q.lower().startswith("escalate"):
        ticket = q.split()[-1].upper()
        st.session_state.pending_ticket = ticket
        answer = create_escalation(ticket)

    # Confirmation
    elif q.upper() == "CONFIRM":
        if st.session_state.pending_ticket:
            answer = f"""
## ✅ Escalation Created Successfully

**Ticket:** {st.session_state.pending_ticket}

The ticket has been assigned to Backend Engineering with **P1 Priority**.
"""
            st.session_state.pending_ticket = None
        else:
            answer = "No pending escalation found."

    # PDF or AI reply
    else:
        pdf = search_documents(q)

        if pdf != "No matching policy found.":
            answer = pdf
        else:
            answer = ai_reply(q)

    st.session_state.messages.append(("assistant", answer))
    st.rerun()