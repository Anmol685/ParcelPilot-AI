import streamlit as st
from tools import (
    search_documents,
    get_excel_info,
    get_order,
    get_ticket,
    ai_reply,
    create_escalation
)

st.set_page_config(page_title="ParcelPilot AI", page_icon="🤖")

st.title("🤖 ParcelPilot AI Support Agent")
st.write("Internal Operations Support Chatbot")

# -------------------------
# Session State
# -------------------------
if "pending_escalation" not in st.session_state:
    st.session_state.pending_escalation = None

user = st.chat_input("Ask about orders, tickets or policies...")

if user:
    user = user.strip()

    st.chat_message("user").write(user)

    # -------------------------
    # Greeting
    # -------------------------
    if any(greet in user.lower() for greet in [
        "hi", "hello", "hey", "hy", "hii",
        "kaise ho", "kese ho", "kaisi ho"
    ]):
        st.chat_message("assistant").markdown("""
## 👋 Hello!

I'm **ParcelPilot AI**, an Internal Operations Support Chatbot.

You can ask me:

- `excel`
- `ORD-1001`
- `TKT-501`
- `support policy`
- `cancellation fee`
- `Why is shipment creation failing?`
- `escalate TKT-501`
""")

    # -------------------------
    # Excel
    # -------------------------
    elif user.lower() == "excel":
        st.chat_message("assistant").markdown(get_excel_info())

    # -------------------------
    # Order
    # -------------------------
    elif user.upper().startswith("ORD-"):
        st.chat_message("assistant").markdown(get_order(user))

    # -------------------------
    # Ticket
    # -------------------------
    elif user.upper().startswith("TKT-"):
        st.chat_message("assistant").markdown(get_ticket(user))

    # -------------------------
    # Escalation
    # -------------------------
    elif user.lower().startswith("escalate"):
        ticket = user.split()[-1].upper()
        st.session_state.pending_escalation = ticket
        st.chat_message("assistant").markdown(create_escalation(ticket))

    elif user.upper() == "CONFIRM":
        if st.session_state.pending_escalation:
            ticket = st.session_state.pending_escalation
            st.chat_message("assistant").success(
                f"""✅ Escalation Created Successfully

**Ticket:** {ticket}

Assigned to **Backend Engineering** with **P1 Priority**.
"""
            )
            st.session_state.pending_escalation = None
        else:
            st.chat_message("assistant").warning("No pending escalation found.")

    # -------------------------
    # AI Resolution
    # -------------------------
    elif (
        "shipment" in user.lower()
        or "500" in user.lower()
        or "cancellation" in user.lower()
        or "service credit" in user.lower()
    ):
        st.chat_message("assistant").markdown(ai_reply(user))

    # -------------------------
    # PDF Search
    # -------------------------
    else:
        result = search_documents(user)

        if result == "No matching policy found.":
            st.chat_message("assistant").markdown(
                "I couldn't find an exact answer. Try **ORD-1001**, **TKT-501**, **support policy**, or **escalate TKT-501**."
            )
        else:
            st.chat_message("assistant").markdown(result)
