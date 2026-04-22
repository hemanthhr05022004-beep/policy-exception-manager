import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("prompts/describe_prompt.txt", "r") as f:
    prompt_template = f.read()

def test_prompt(title, description, risk_level, requested_by, duration):
    filled_prompt = prompt_template.format(
        title=title,
        description=description,
        risk_level=risk_level,
        requested_by=requested_by,
        duration=duration
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": filled_prompt}],
        temperature=0.3,
        max_tokens=500
    )
    print(response.choices[0].message.content)

# 5 Real Test Inputs
test_prompt("Bypass Password Expiry", "Legacy CRM does not support 90-day reset", "Medium", "IT Team", "6 months")
test_prompt("Personal Laptop for Work", "Employee working from home due to hardware shortage", "High", "HR Department", "3 months")
test_prompt("Shared Admin Account", "Legacy server supports only one admin account", "High", "DevOps Team", "2 months")
test_prompt("Disable MFA for Vendor", "Third party tool does not support MFA", "Critical", "Procurement Team", "1 month")
test_prompt("Store Data on Local Drive", "Internet outage requires local storage temporarily", "Medium", "Branch Manager", "1 week")