@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    if not data.get("title") or not data.get("risk_level"):
        return jsonify({"error": "title and risk_level are required"}), 400

    prompt = f"""
You are a Policy Exception Manager AI assistant.

Given this policy exception:
- Title: {data['title']}
- Risk Level: {data['risk_level']}
- Description: {data.get('description', '')}

Give exactly 3 recommendations to mitigate the risk.
Return ONLY this JSON array:
[
  {{"action_type": "...", "description": "...", "priority": "HIGH or MEDIUM or LOW"}},
  {{"action_type": "...", "description": "...", "priority": "HIGH or MEDIUM or LOW"}},
  {{"action_type": "...", "description": "...", "priority": "HIGH or MEDIUM or LOW"}}
]

Return ONLY the JSON array. No extra text. No markdown.
"""

    result = call_groq(prompt)

    if result is None:
        return jsonify({"error": "AI service failed", "is_fallback": True}), 500

    return jsonify(result), 200