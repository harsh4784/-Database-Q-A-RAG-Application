# Database Q&A RAG Application

A simple chat application that lets you ask questions about your MySQL database in plain English.

## Setup

1. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   Copy `.env.example` to `.env` and fill in your details:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DB_HOST=localhost
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   ```

3. **Import your MySQL database:**
   ```bash
   mysql -u your_user -p your_database < database_file.sql
   ```

## Run

```bash
streamlit run app.py
```

## Usage

- Open the app in your browser
- Type questions about your database
- Get answers in plain English

Example questions:
- "How many records are in the users table?"
- "What are the top 5 products by sales?"
- "Show me all customers from New York"
