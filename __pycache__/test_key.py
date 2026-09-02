import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

key = os.getenv("GROQ_API_KEY")
print(f"Loaded Key: {key[:8]}... (Length: {len(key) if key else 0})")

try:
    llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=key)
    res = llm.invoke("Hello, are you active?")
    print(" Response:", res.content)
    print(" API KEY WORKING 100%!")
except Exception as e:
    print("❌ Error:", e)