import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load API key
load_dotenv()

# 2. Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. Create prompt template
prompt = PromptTemplate.from_template(
    "Explain {topic} in 3 bullet points, using plain and simple terms for a beginner."
)

# 4. Initialize Output Parser
parser = StrOutputParser()

# 5. Build full chain
chain = prompt | llm | parser

# 6. Interactive loop
print("--- GenAI Assistant Ready! (Type 'exit' or 'quit' to stop) ---\n")

while True:
    user_input = input("Content creation topic: ")
    
    if user_input.strip().lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    if not user_input.strip():
        continue

    print("\nGenerating response...\n")
    response = chain.invoke({"topic": user_input})
    print("AI Response:\n")
    print(response)
    print("\n" + "-" * 50 + "\n")