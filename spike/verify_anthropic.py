import os

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key is None:
    raise RuntimeError("ANTHROPIC_API_KEY not found. Check that .env exists and contains the key.")

client = Anthropic(api_key=api_key)

response = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens=100,
    messages=[{"role": "user", "content":"Say hello in one short sentence."}],
)

print(response.content[0].text)
print(f"Token used -input: {response.usage.input_tokens}, output: {response.usage.output_tokens}")