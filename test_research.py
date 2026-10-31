
from ai_engine import get_response

messages = [
    {
        "role": "user",
        "content": "What is Python? Explain it with examples and reliable sources."
    }
]

print("\nTesting Sandarbh's AI...\n")

try:
    answer = get_response(messages)
    print(answer)

except Exception as error:
    print("\nTEST FAILED")
    print(type(error).__name__, error)
