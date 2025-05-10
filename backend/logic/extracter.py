from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def extract_variables_from_response(response_text, expected_variables):
    prompt = f"""
You are a helpful assistant collecting loan application data.
Extract the following fields from this response: {', '.join(expected_variables)}.

User Response: "{response_text}"

Return a JSON object. If a value is unknown, return null.
"""

    try:
        completion = client.chat.completions.create(
            model="openchat/openchat-3.5",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Loan Profiling App",
            }
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print("Error in LLM response:", e)
        return {}
