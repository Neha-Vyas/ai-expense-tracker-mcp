# AI Expense Tracker MCP

An AI-powered personal expense tracker built to learn and implement **Model Context Protocol (MCP)** from the ground up.

The project will progressively evolve from a local MCP server connected to PostgreSQL into a remote, AI-powered expense management system accessible through different MCP clients.

## 🚧 Project Status

**Currently:** Project setup and architecture phase

This project is being developed incrementally. Each phase introduces a new concept while building on the previous one.

## 🎯 Project Goal

Build a personal expense tracker where natural-language requests such as:

> "I spent ₹450 on dinner today."

can eventually be understood by an LLM and converted into an appropriate MCP tool call that stores the expense in PostgreSQL.

## 🏗️ Planned Architecture

```text
User
 │
 ▼
LLM
 │
 ▼
MCP Client
 │
 ▼
MCP Server
 │
 ▼
PostgreSQL
```

The project will initially use **Claude Desktop** as an MCP client for testing.

Later, we will build our **own Python MCP client** and connect it to an LLM.

## 🛠️ Technology Stack

* Python
* FastMCP
* Model Context Protocol (MCP)
* PostgreSQL
* SQL
* LangChain MCP Adapters
* LLM
* Git & GitHub

### Planned Technologies

* Remote MCP
* FastMCP Cloud / remote deployment
* Docker
* Qdrant / pgvector for future AI features

## 🗺️ Development Roadmap

### Phase 1 — PostgreSQL Foundation

* Set up PostgreSQL
* Create the `expense_tracker` database
* Design the expenses table
* Connect Python to PostgreSQL
* Test CRUD operations

### Phase 2 — Local MCP Server

* Build the FastMCP server
* Create expense-management tools
* Connect MCP tools to PostgreSQL
* Understand MCP tools and resources

### Phase 3 — Claude Desktop

* Connect the local MCP server to Claude Desktop
* Test natural-language expense operations
* Verify database changes

### Phase 4 — Custom MCP Client

* Build our own Python MCP client
* Discover MCP tools
* Execute MCP tools programmatically
* Understand MCP client-server communication

### Phase 5 — LLM + MCP

* Connect an LLM to our MCP client
* Allow the LLM to select appropriate tools
* Execute tool calls
* Return tool results to the LLM

### Phase 6 — Remote MCP

* Convert the local MCP server into a remote MCP server
* Learn remote MCP communication
* Deploy the MCP server

### Phase 7 — Remote Access

* Connect remote MCP clients
* Explore Claude mobile/web access
* Secure the remote service

### Phase 8 — AI Expense Intelligence

* Spending analysis
* Monthly summaries
* Budget insights
* Natural-lan



One more important thing: MCP itself does not require AI. MCP is a protocol for exposing and calling tools. An AI model is one possible client, but a normal Python program can also be an MCP client.
