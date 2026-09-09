# langchain-app

CAIE Course Program - Assignment 5 (LangChain + LangSmith)

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\Activate.ps1     # Windows PowerShell

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API keys (or copy .env.example to .env and load it)
export OPENAI_API_KEY="your-openai-key"
export LANGCHAIN_API_KEY="your-langsmith-key"
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="langchain-assignment"

# 4. Run
python main.py

# 5. Deactivate when done
deactivate
```

Get an OpenAI key at platform.openai.com and a LangSmith key at smith.langchain.com.

After running, check your LangSmith project dashboard — the run (input, output, timing) should appear there.
