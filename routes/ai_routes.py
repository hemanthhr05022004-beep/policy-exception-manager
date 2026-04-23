from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/describe", methods=["POST"])
def describe():
    data = request.json   # ✅ data is defined here

    prompt = f"""
Return ONLY valid JSON. No explanation.

Format:
{{
  "summary": "...",
  "risk_assessment": "...",
  "recommendation": "..."
}}

Input:
{data}
"""

    result = call_groq(prompt)

    return jsonify(result)