# Northstar Holdings – AI Policy Assistant

## 1. About This Project

This project is an AI-powered policy assistant for Northstar Holdings. I built it to help employees ask questions about company policies and receive answers based on the policy documents provided to the system.

Instead of searching through several Markdown files manually, a user can ask a question through one API endpoint. The application searches the available policy documents, selects the most relevant sections, and sends those sections to the OpenAI API. The AI then prepares an answer using the selected information.

All five policy documents are handled by one RAG application. They are not separate projects or separate chatbots.

## 2. What I Have Built

The application currently includes the following features:

- A browser-based chatbot interface at the home page (`http://localhost:8000`) with a message area, suggested questions, and source references. It sends questions to the existing `POST /ask` endpoint.

- A FastAPI application that provides the API for asking policy questions.
- A document loader that reads Markdown (`.md`) files from the `documents` folder.
- A text chunking process that separates documents into smaller sections.
- A TF-IDF retrieval system that finds sections related to the user's question.
- An OpenAI API integration that generates an answer from the retrieved content.
- Source details in the API response, so the user can see which document and section were used.
- A fallback response when the available documents do not contain a relevant answer.
- A health endpoint that shows whether the application is running and how many document chunks were indexed.
- Basic automated tests for document retrieval and the API home endpoint.
- Docker configuration to build and run the API in a container.

## 3. Policy Documents Used

The application reads these five documents from the `documents` folder:

| Document | What it covers |
|---|---|
| `attendance_policy.md` | Office hours, late arrivals, grace period, missing punch requests, attendance recording and attendance visibility. |
| `employee_roles.md` | Employee, Direct Manager, HR, HR Admin and Payroll HR responsibilities and access rules. |
| `flight_ticket_policy.md` | Flight ticket eligibility, request steps, approval process, booking and policy limitations. |
| `leave_policy.md` | Annual leave, sick leave, unpaid leave, approvals and leave cancellation. |
| `payslip_guide.md` | Payslip availability, publication timing, payslip contents and payroll access rules. |

When the application starts, it loads all Markdown files found in this folder. If another `.md` policy document is added to the same folder, the loader will include it the next time the application starts.

## 4. Project Folder Structure

```text
Northstar-Attendance-AI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── retrieval.py
│   └── providers.py
│
├── documents/
│   ├── attendance_policy.md
│   ├── employee_roles.md
│   ├── flight_ticket_policy.md
│   ├── leave_policy.md
│   └── payslip_guide.md
│
├── tests/
│   ├── test_api.py
│   └── test_retrieval.py
│
├── requirements.txt
├── Dockerfile
├── compose.yml
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md
```

## 5. Technologies and Packages Used

I used the following technologies in this project:

| Technology / Package | Why it is used |
|---|---|
| Python 3.11 | Main programming language used to build the application. |
| FastAPI | Creates the HTTP API and handles incoming questions. |
| Uvicorn | Runs the FastAPI application locally or inside Docker. |
| scikit-learn | Provides TF-IDF vectorization and cosine similarity for document retrieval. |
| NumPy | Supports numerical operations used by the retrieval dependencies. |
| OpenAI Python SDK | Sends the retrieved policy context to the OpenAI API and receives the generated answer. |
| Pydantic | Checks and validates the question received by the API. |
| python-dotenv | Loads configuration values and the API key from the `.env` file. |
| pytest | Runs the automated tests. |
| httpx | Supports HTTP testing with FastAPI's test client. |
| Docker | Packages the application and its dependencies into a container. |
| Docker Compose | Starts the application using the Docker configuration in `compose.yml`. |

The exact Python package versions are listed in `requirements.txt`.

**Note:** This project uses the OpenAI API for answer generation. It does not use Ollama. An OpenAI API key and available API credits are required for questions that need an AI-generated answer. A ChatGPT subscription and OpenAI API billing are separate.

## 6. How the RAG Process Works

RAG means Retrieval-Augmented Generation. In this project, the application retrieves useful information from the policy documents before asking the AI to prepare an answer.

The process works as follows:

1. The user sends a question to the `POST /ask` endpoint.
2. FastAPI receives the question and checks that it meets the input length requirements.
3. The retriever searches the Markdown content that was loaded when the application started.
4. The documents are split into smaller sections. These sections are called chunks.
5. TF-IDF converts the text into numerical vectors. Cosine similarity is used to compare the user's question with each chunk.
6. The retriever selects up to the configured number of relevant chunks that meet the similarity threshold.
7. The application sends the question and only the selected document sections to the OpenAI API.
8. The model is instructed to answer from the supplied context and not to invent policy information.
9. FastAPI returns the answer, the source document names, the section names and a `grounded` status.

If no chunk reaches the configured retrieval threshold, the application returns:

> The available documents do not provide the answer.

In that case, the application does not call the OpenAI API.

## 7. What Each Python File Does

### `app/main.py`

This is the main application file. It creates the FastAPI application and defines the `/`, `/health` and `/ask` endpoints. It loads the policy documents when the application starts, calls the retriever, sends the selected context to the answer provider and returns the result.

### `app/config.py`

This file reads the application settings from environment variables. These settings include the OpenAI API key, model name, documents folder, number of chunks to retrieve and retrieval threshold.

### `app/retrieval.py`

This file loads every `.md` file in the documents folder. It splits the content by Markdown headings and paragraphs, creates TF-IDF vectors and searches for the most relevant chunks when a question is received.

### `app/providers.py`

This file connects the application to the OpenAI API. It sends the user's question together with the retrieved policy context and returns the generated answer.

### `requirements.txt`

This file contains the Python packages and pinned versions needed by the application.

### `tests/`

This folder contains basic automated tests. The retrieval test checks that more than one Markdown file can be indexed and searched. The API test checks that the home endpoint responds successfully.

## 8. Environment Setup on Windows

Docker is optional. The application can also run directly in a Python virtual environment.

### Step 1: Install Python

Install Python 3.11 and make sure the Python launcher is available in the terminal.

### Step 2: Open the project folder

Extract the project ZIP file and open the `Northstar-Attendance-AI` folder in Visual Studio Code.

### Step 3: Create a virtual environment

Run this command in the VS Code terminal:

```powershell
py -3.11 -m venv myenv
```

This creates an isolated Python environment named `myenv` inside the project folder.

### Step 4: Activate the environment

```powershell
.\myenv\Scripts\Activate.ps1
```

After activation, the terminal prompt should show the environment name.

If PowerShell blocks activation, use Command Prompt and run:

```cmd
myenv\Scripts\activate.bat
```

### Step 5: Install the packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs the packages listed in `requirements.txt` into the active virtual environment.

## 9. Configure the OpenAI API Key

The project includes `.env.example` as a template and `.env` for local configuration.

Open the `.env` file in the project root and add your own API key:

```env
OPENAI_API_KEY=your_actual_openai_api_key
OPENAI_MODEL=gpt-4o-mini
DOCUMENTS_DIR=documents
TOP_K=4
RETRIEVAL_THRESHOLD=0.12
```

Do not include quotation marks around the key. Do not share the key or upload the `.env` file to GitHub.

The API key must belong to an OpenAI API account with available API credits. If the account has no API credits or quota, the `/ask` request that reaches the model can fail even when the FastAPI application is running correctly.

## 10. Run the Application Without Docker

Make sure the virtual environment is active and the `.env` file is configured.

Run:

```powershell
uvicorn app.main:app --reload
```

When the application starts, it loads the Markdown documents and builds the retrieval index.

Open the Swagger API page:

`http://127.0.0.1:8000/docs`

You can also check the service status at:

`http://127.0.0.1:8000/health`

## 11. Run the Application with Docker

Docker is included as an alternative way to run the application. You do not need to create the Python virtual environment to run the container, but you do need Docker Desktop installed and running.

Make sure the `.env` file exists and contains a valid OpenAI API key. Open a terminal in the project root and run:

```bash
docker compose -f compose.yml up --build
```

Docker Compose builds the image, installs the Python dependencies inside the image and starts the FastAPI container.

Open the API documentation at:

`http://localhost:8000/docs`

To stop the containers, press `Ctrl + C` in the running terminal. If you started the containers in detached mode, use:

```bash
docker compose -f compose.yml down
```

This Docker setup runs the FastAPI application only. The application connects to the OpenAI API over the internet. It does not start an Ollama container.

## 12. How to Ask a Question

In Swagger, open `POST /ask`, select **Try it out**, and enter a JSON request like this:

```json
{
  "question": "How many annual leave days do employees receive?"
}
```

Select **Execute** to send the question.

The response includes:

- `answer`: the answer generated from the retrieved policy context.
- `sources`: the document name, section name and relevance score for the retrieved chunks.
- `grounded`: `true` when relevant document chunks were retrieved and used for answer generation; `false` when no relevant chunks were found.

Other example questions include:

- What time does the office start?
- How many late arrivals require HR review?
- Who approves annual leave?
- How many months must an employee work before becoming eligible for an annual flight ticket?
- When are payslips normally published?
- Can a Direct Manager view an employee's payslip?

## 13. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Confirms that the Northstar API is running. |
| GET | `/health` | Shows the service status and the number of indexed chunks. |
| POST | `/ask` | Retrieves policy information and generates an answer. |

## 14. Run the Tests

With the virtual environment active, run:

```powershell
pytest -q
```

The tests check basic API availability and multi-document retrieval. They do not verify every possible policy question or guarantee that every AI answer is correct.

## 15. Current Limitations and Future Improvements

This project is a policy question-answering demo. It is not connected to the live Northstar ERP and does not read actual employee records.

The current retriever uses TF-IDF and cosine similarity. This is a keyword-based retrieval approach, so a question phrased very differently from the policy text may not retrieve the best section. The retrieval threshold and top-k settings may need adjustment after testing with real questions.

The model is instructed to use only retrieved context, but an AI-generated answer can still be incorrect. Important HR and payroll decisions should be checked against the original policy documents.

The current application does not authenticate employees or enforce role-based access to real employee data. The policy documents describe access rules, but simply retrieving those rules does not enforce them. Before using this system with private employee information, add secure authentication, backend authorization, employee-level access checks, audit logging and appropriate privacy controls.

Possible future improvements include semantic embeddings, a vector database, better retrieval evaluation, document version tracking, monitoring, rate limiting and production-grade authentication.

## 16. Project Summary

I combined five Northstar Holdings policy documents into one FastAPI-based RAG application. The application loads the Markdown files, retrieves relevant content using TF-IDF and cosine similarity, and uses the OpenAI API to generate an answer from the retrieved context. It returns the answer together with source information so that the user can identify which policy document was used.

The application can be run locally using a Python virtual environment or packaged and started with Docker Compose.
