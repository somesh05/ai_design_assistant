
import os
import json
import base64
from io import BytesIO

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_llm(
    system_prompt,
    user_prompt,
    temperature=0.7,
    max_tokens=1500
):
    """
    Send a text prompt to Groq and return the response.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system","content": system_prompt},
                {"role": "user","content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    except Exception as e:
        return (f"Error: {str(e)}.""Check your GROQ_API_KEY in .env")


# --------------------------------------------------
# VISION MODEL CALL
# --------------------------------------------------

def call_vision(image_pil, user_prompt):
    """
    Send a PIL image + prompt to a Groq vision model.
    """

    try:
        # Convert image to bytes
        buffer = BytesIO()

        image_pil.save(
            buffer,
            format="JPEG",
            quality=85
        )

        image_bytes = buffer.getvalue()

        # Convert image to Base64
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        # Create Data URL
        data_url = (f"data:image/jpeg;base64,{image_b64}")

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url","image_url": {"url": data_url}},
                        {"type": "text","text": user_prompt}
                    ]
                }
            ],
            max_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Vision API Error: {str(e)}"

def safe_json_parse(text):
    """
    LLMs often wrap JSON in markdown fences like:
    ```json
    { "key": "value" }
    ```
    This strips the fences and parses safely.
    Returns: (parsed_dict, None) on success OR (None, error_string) on failure.
    """
    try:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] # remove opening fence line
            cleaned = cleaned.rsplit("```", 1)[0] # remove closing fence
        return json.loads(cleaned.strip()), None
    except json.JSONDecodeError as e:
        return None, str(e)
