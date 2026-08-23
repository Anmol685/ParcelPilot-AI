# ParcelPilot AI Support Agent

An AI-powered internal operations support chatbot built using **Streamlit, LangChain, FAISS, Google Gemini 3.6 Flash, and Excel**.

The application helps support agents retrieve company policies, look up operational records, and perform ticket escalation from a single chat interface.

---

## Live Links

**GitHub Repository:**
https://github.com/Anmol685/ParcelPilot-AI

**Hosted Application:**
https://parcelpilot-ai.streamlit.app/

---

## Features

* PDF-based policy retrieval using Retrieval-Augmented Generation (RAG)
* Order lookup (`ORD-1001`)
* Account lookup (`ACCT-001`)
* Ticket lookup (`TKT-501`)
* Ticket escalation workflow
* Streamlit chat interface

---

## Technology Stack

* Streamlit
* Google Gemini 3.6 Flash
* LangChain
* FAISS
* Google Generative AI Embeddings
* Pandas
* OpenPyXL
* PyPDF

---

## Project Structure

```text
ParcelPilot-AI/
│── app.py
│── tools.py
│── excel_tools.py
│── actions.py
│── requirements.txt
│── escalations.json
│── README.md
│── ParcelPilot_Assessment_Data.xlsx
│── 01_Support_Policy_v3_CURRENT.pdf
│── 02_Support_Policy_v2_DEPRECATED.pdf
│── 03_Cancellation_and_Service_Credit_SOP_v4.pdf
│── 04_Product_Operations_Guide_and_Known_Issues.pdf
│── 05_Northstar_Logistics_Enterprise_Agreement.pdf
│── 06_LumenWorks_Service_Agreement.pdf
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Anmol685/ParcelPilot-AI.git
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` File

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

> **Note:** Generate your API key from Google AI Studio. Never commit your actual API key to GitHub. The hosted Streamlit app uses Streamlit Secrets to store it securely.

### 4. Run the Application

```bash
streamlit run app.py
```

---

## Sample Queries

```text
ORD-1001
ACCT-001
TKT-501
ESCALATE TKT-501
What is the cancellation policy?
What service credit applies for late delivery?
Explain the Northstar Logistics agreement.
```

---

# Architecture Note

## Agent Design

ParcelPilot AI uses a **single intelligent support agent**. The chatbot first identifies whether the user's query belongs to structured operational data (Order, Account, Ticket, Escalation) or document-based policy questions. Structured requests are routed directly to local tools, while policy questions use Retrieval-Augmented Generation (RAG).

## Tool Design

The application contains four tools:

* **Order Tool** — Retrieves shipment information from Excel.
* **Account Tool** — Returns enterprise customer details.
* **Ticket Tool** — Fetches support ticket information.
* **Escalation Tool** — Creates a Tier-2 escalation after user confirmation and stores it in `escalations.json`.

## Document & Structured Data Handling

* **Structured Data:** Excel workbook containing Orders, Accounts, and Tickets.
* **Unstructured Data:** Operational policy PDFs.
* PDFs are chunked using LangChain, converted into embeddings, indexed with FAISS, and searched before Gemini generates the final response.

## Source Reliability & Conflict Handling

* Excel is treated as the authoritative source for operational IDs.
* Policy answers are generated only from retrieved PDF content.
* If no matching record exists, the chatbot returns a clear **"Not Found"** response instead of generating unsupported information.

## Major Technical Trade-offs

* FAISS is generated locally instead of using a persistent vector database.
* JSON is used for escalation storage instead of SQL for simplicity.
* A single-agent architecture was chosen over multi-agent orchestration to keep deployment lightweight.

---

# Product Note

## Additional Client Problem Addressed

I implemented a **Ticket Escalation Workflow** that allows support agents to escalate tickets directly from chat with a confirmation step, reducing manual operational effort.

## Future Improvements

* Live shipment tracking
* SLA breach alerts
* Customer authentication
* Analytics dashboard
* Persistent SQL database

## Intentionally Left Out

* User authentication
* Real-time carrier APIs
* Multi-user chat history
* Production monitoring

These features were intentionally excluded to keep the project focused on the assessment scope.

## Success Metric

**First Contact Resolution (FCR)** — the percentage of customer queries resolved without requiring human escalation.

---

# AI Tool Usage

## AI Tools Used

* ChatGPT
* Google Gemini 3.6 Flash API

## How They Were Used

* **ChatGPT:** Architecture planning, debugging, Streamlit development, LangChain integration, FAISS implementation, and code refactoring.
* **Gemini 3.6 Flash:** Large Language Model for answering policy questions using retrieved PDF context.

---

## Author

**Anmol Goel**

B.Tech Computer Science Engineering

ParcelPilot AI Assessment
