# ============================================
# insight_generator.py
# Takes raw database results (list of dicts) and turns them into
# a plain English summary using an AI model via Groq.
# ============================================

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"


def generate_insight(user_question, results):
    """
    Takes the original question and the raw SQL results, and returns
    a natural-language summary sentence.
    """

    if not results:
        return "No matching records were found for this question."

    if TEST_MODE:
        return f"[TEST MODE] Found {len(results)} matching record(s)."

    preview_rows = results[:20]
    results_text = "\n".join([str(row) for row in preview_rows])

    prompt = f"""You are a business analyst. A user asked this question about their
company database:

"{user_question}"

Here is the raw data returned from the database:
{results_text}

Write a short, direct, plain-English answer (1-2 sentences max) using
ONLY the data given above. Rules:
- State the answer directly and confidently. Do not say things like
  "further investigation is needed" or "more data may be required" --
  the data above is complete and final, just answer using it.
- Mention specific numbers or names where relevant.
- Do not mention SQL, databases, or tables -- speak naturally like
  you're briefing a business manager.
- If the data list has multiple items, you may state the count
  (e.g. "There are 2 customers...") followed by their names."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    fake_question = "Show me the names of all customers from Lucknow"
    fake_results = [
        {"name": "Raj Kumar", "city": "Lucknow"},
        {"name": "Rohit Sharma", "city": "Lucknow"}
    ]

    summary = generate_insight(fake_question, fake_results)
    print("Insight:", summary)