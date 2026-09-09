"""
CAIE Course Program - Assignment 5: LangChain
A small program that sends a prompt to an OpenAI chat model via LangChain,
prints the response, and traces the run in LangSmith.
"""

import os
import sys

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Automatically find and load a .env file, even if it lives in a parent
# folder (e.g. this script is in Day09/Assignment but .env is at the
# project root). find_dotenv() walks upward from the current working
# directory until it finds one.
load_dotenv(find_dotenv())


def get_required_env(var_name: str) -> str:
    """Fetch an environment variable or exit with a clear error if missing."""
    value = os.environ.get(var_name)
    if not value:
        print(f"ERROR: Missing required environment variable '{var_name}'.")
        print("Set it before running the program, e.g.:")
        print(f'  export {var_name}="your-key-here"   # macOS/Linux')
        print(f'  $env:{var_name}="your-key-here"      # Windows PowerShell')
        sys.exit(1)
    return value


def main():
    # --- Validate required keys up front so failures are clear ---
    get_required_env("OPENAI_API_KEY")

    # LangSmith tracing is optional but recommended by the assignment.
    # If LANGCHAIN_API_KEY isn't set, tracing simply won't be sent, but
    # we warn the user so they know why nothing shows up on the dashboard.
    if not os.environ.get("LANGCHAIN_API_KEY"):
        print("WARNING: LANGCHAIN_API_KEY not set - runs will not appear in LangSmith.")
    else:
        # Make sure tracing is turned on even if the user forgot to export it.
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
        os.environ.setdefault("LANGCHAIN_PROJECT", "langchain-assignment")

    # --- Build the LangChain model wrapper (talks to OpenAI under the hood) ---
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
    )

    # --- Send an input/prompt through LangChain ---
    prompt = "Tell me about the ChatGPT latest model and its capabilities."
    print(f"Input: {prompt}\n")

    response = llm.invoke([HumanMessage(content=prompt)])

    print(f"Output: {response.content}\n")
    print("(Check your LangSmith project dashboard to see this run traced.)")


if __name__ == "__main__":
    main()