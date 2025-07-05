from openai import OpenAI

# Test your API key
api_key = "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"

try:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print("✅ API key works!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API key error: {e}") 