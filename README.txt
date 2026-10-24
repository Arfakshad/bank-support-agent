# Bank Support Agent 🤖🏦

**An AI-powered banking support chatbot built with Python, Flask, and Google Gemini.**

Developed by **Arfakshad**

## 📌 Project Overview

Bank Support Agent is an AI-powered chatbot designed to assist customers with common banking support tasks through a conversational interface.

The application uses Google's Gemini API to understand customer queries and Python-based banking tools to perform operations using demo banking data.

Customers can sign in with sample credentials, check account balances, view transaction information, request card blocking, and register complaints.

> **Disclaimer:** This project uses mock banking data for demonstration and educational purposes. It is not connected to a real bank and must not be used for real financial transactions.

## ✨ Features

- **AI-powered conversations:** Understands natural-language banking queries using Google Gemini.
- **Customer login:** Supports sample customer IDs and PINs.
- **Balance inquiry:** Retrieves account balance from demo data.
- **Transaction history:** Displays available transaction information.
- **Transaction status:** Checks the status of a transaction using its reference.
- **Card blocking:** Supports card-blocking requests in the demo environment.
- **Complaint registration:** Registers customer complaints in demo data.
- **Web interface:** Interact with the assistant through a browser.
- **Session management:** Uses Flask sessions for web interactions.
- **Deployment support:** Includes configuration for deployment using Gunicorn.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and banking tools |
| Flask | Web server and HTTP routes |
| Google Gemini API | Natural-language understanding and responses |
| HTML and JavaScript | Chat interface |
| Git and GitHub | Source-code management |
| Gunicorn | Production-style WSGI server |
| Render | Cloud deployment target |

## 📁 Project Structure

```text
bank-support-agent/
├── bank_web_app.py
├── bank_support_agent.py
├── bank_tools.py
├── bank_db.py
├── bank_ui.html
├── requirements.txt
├── run_bank_agent.bat
├── run_bank_agent.sh
├── README.md
└── .gitignore
```

- `bank_web_app.py` — Flask application, routes, sessions, and chat handling.
- `bank_support_agent.py` — Gemini client and AI agent instructions.
- `bank_tools.py` — Functions for banking operations.
- `bank_db.py` — Sample customer, account, and transaction data.
- `bank_ui.html` — Browser-based chatbot interface.
- `requirements.txt` — Python dependencies.
- `run_bank_agent.bat` — Windows launch script.
- `run_bank_agent.sh` — Linux/macOS launch script.
- `.gitignore` — Excludes configured files from Git tracking.

## ⚙️ Prerequisites

- Python 3.10 or newer
- Internet connection
- Google Gemini API key
- Git (optional, for source-code management)

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

## 🚀 Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Arfakshad/bank-support-agent.git
cd bank-support-agent
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Set your Gemini API key without placing it in source code.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
$env:FLASK_SECRET_KEY = "YOUR_RANDOM_SECRET"
```

**Linux/macOS:**

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
export FLASK_SECRET_KEY="YOUR_RANDOM_SECRET"
```

Use your own valid API key and a strong, random Flask secret. Never commit secrets to GitHub.

If the application supports loading a local `.env` file, keep that file private and excluded from Git.

### 5. Run the application

```bash
python bank_web_app.py
```

Open the local address shown by the application, typically:

`http://127.0.0.1:5000`

Keep the terminal running while using the application.

## 🔐 Demo Login Credentials

The project includes sample accounts defined in `bank_db.py`.

| Customer ID | Demo PIN | Customer |
|---|---|---|
| `C1001` | `1234` | Ahmed Khan |
| `C1002` | `5678` | Fatima Ali |

**These credentials are for demonstration only.** Do not use real banking credentials or personal financial information.

## 💬 Example Queries

After signing in, try queries such as:

- “What is my account balance?”
- “Show my recent transactions.”
- “What happened to transaction TXN1003?”
- “I want to block my card.”
- “I want to register a complaint.”

The response depends on the available demo records, implemented tools, and Gemini API configuration.

## ☁️ Deployment on Render

The project can be deployed as a Render Web Service.

1. Push the project to GitHub.
2. Open the [Render Dashboard](https://dashboard.render.com/).
3. Create a new **Web Service** and connect the repository.
4. Configure the following commands:

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
gunicorn bank_web_app:app
```

5. Add the required environment variables in Render:

| Variable | Value |
|---|---|
| `GEMINI_API_KEY` | Your valid Gemini API key |
| `FLASK_SECRET_KEY` | A strong, random secret |
| `GEMINI_MODEL` | A model supported by your Gemini API account, if configurable |

6. Deploy the service and check the build logs.
7. Test login, chatbot responses, and each banking operation on the deployed URL.

The deployment is not considered fully verified until a live Gemini request and the relevant application flows have been tested successfully.

## 🔒 Security Considerations

- Never upload API keys, `.env` files, or passwords to GitHub.
- Use a strong, unpredictable Flask secret key.
- Demo PINs are not suitable for production authentication.
- Use server-side authorization for every sensitive banking operation.
- Validate user inputs and transaction references.
- Add persistent storage, audit logs, rate limiting, and robust authentication before any real-world use.
- Protect sensitive data and follow applicable security and privacy requirements.

## ⚠️ Current Limitations

- Banking records are demo data rather than live bank records.
- In-memory data may reset when the application restarts.
- In-memory session storage is not designed for reliable sharing across multiple server workers or instances.
- Gemini model availability and API quotas depend on the configured account.
- Real banking integration and production-grade identity verification are not included.

## 🔮 Future Enhancements

- Integrate an authorized banking API.
- Add persistent database storage.
- Implement stronger customer authentication and authorization.
- Improve multilingual conversation support.
- Add audit logging and monitoring.
- Add automated unit and integration tests.
- Improve deployment reliability and session storage.

## 👨‍💻 Author

**Arfakshad**

GitHub: [@Arfakshad](https://github.com/Arfakshad)

Repository: [bank-support-agent](https://github.com/Arfakshad/bank-support-agent)

## 📄 License

No license has been specified yet. Add a `LICENSE` file before allowing others to reuse, modify, or distribute this project.

---

**Built as an educational demonstration of AI-assisted banking support using Python, Flask, and Google Gemini.**
