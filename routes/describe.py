from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from datetime import datetime
import os

ai_bp = Blueprint("ai", __name__)


# ─────────────────────────────────────────
# POST /describe  (already built on Day 3)
# ─────────────────────────────────────────
@ai_bp.route("/describe", methods=["POST"])
def describe():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is missing",
            "status": 400
        }), 400

    required_fields = [
        "title",
        "description",
        "risk_level",
        "requested_by",
        "duration"
    ]

    missing_fields = []
    for field in required_fields:
        if not data.get(field) or str(data.get(field)).strip() == "":
            missing_fields.append(field)

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields,
            "status": 400
        }), 400

    allowed_risk_levels = ["Low", "Medium", "High", "Critical"]
    if data["risk_level"] not in allowed_risk_levels:
        return jsonify({
            "error": f"risk_level must be one of: {allowed_risk_levels}",
            "status": 400
        }), 400

    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "prompts",
        "describe_prompt.txt"
    )

    try:
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        return jsonify({
            "error": "Prompt template file not found",
            "status": 500
        }), 500

    filled_prompt = prompt_template.format(
        title=data["title"],
        description=data["description"],
        risk_level=data["risk_level"],
        requested_by=data["requested_by"],
        duration=data["duration"]
    )

    result = call_groq(filled_prompt)

    if result is None:
        return jsonify({
            "summary": "Unable to process request at this time.",
            "risk_assessment": "Manual review required.",
            "recommendation": "REVIEW",
            "reason": "AI service temporarily unavailable.",
            "generated_at": datetime.now().isoformat(),
            "is_fallback": True
        }), 200

    result["generated_at"] = datetime.now().isoformat()
    result["is_fallback"] = False

    return jsonify(result), 200


# ─────────────────────────────────────────
# POST /recommend  (NEW - Day 4)
# ─────────────────────────────────────────
@ai_bp.route("/recommend", methods=["POST"])
def recommend():

    # ── Step 1: Get JSON body
    data = request.get_json()

    # ── Step 2: Check if body exists
    if not data:
        return jsonify({
            "error": "Request body is missing",
            "status": 400
        }), 400

    # ── Step 3: Validate required fields
    required_fields = [
        "title",
        "description",
        "risk_level",
        "requested_by",
        "duration"
    ]

    missing_fields = []
    for field in required_fields:
        if not data.get(field) or str(data.get(field)).strip() == "":
            missing_fields.append(field)

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields,
            "status": 400
        }), 400

    # ── Step 4: Validate risk_level
    allowed_risk_levels = ["Low", "Medium", "High", "Critical"]
    if data["risk_level"] not in allowed_risk_levels:
        return jsonify({
            "error": f"risk_level must be one of: {allowed_risk_levels}",
            "status": 400
        }), 400

    # ── Step 5: Load recommend prompt template
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "prompts",
        "recommend_prompt.txt"
    )

    try:
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        return jsonify({
            "error": "Recommend prompt template file not found",
            "status": 500
        }), 500

    # ── Step 6: Fill placeholders
    filled_prompt = prompt_template.format(
        title=data["title"],
        description=data["description"],
        risk_level=data["risk_level"],
        requested_by=data["requested_by"],
        duration=data["duration"]
    )

    # ── Step 7: Call Groq AI
    result = call_groq(filled_prompt)

    # ── Step 8: Handle AI failure — return fallback
    if result is None:
        return jsonify([
            {
                "action_type": "ESCALATE",
                "description": "Escalate this exception request to senior management for manual review.",
                "priority": "HIGH"
            },
            {
                "action_type": "DOCUMENT",
                "description": "Document all details of this exception request for audit purposes.",
                "priority": "MEDIUM"
            },
            {
                "action_type": "MONITOR",
                "description": "Monitor all activities related to this exception on a daily basis.",
                "priority": "MEDIUM"
            }
        ]), 200

    # ── Step 9: Validate AI returned exactly 3 items
    if not isinstance(result, list) or len(result) != 3:
        return jsonify([
            {
                "action_type": "ESCALATE",
                "description": "Escalate this exception request to senior management for manual review.",
                "priority": "HIGH"
            },
            {
                "action_type": "DOCUMENT",
                "description": "Document all details of this exception request for audit purposes.",
                "priority": "MEDIUM"
            },
            {
                "action_type": "MONITOR",
                "description": "Monitor all activities related to this exception on a daily basis.",
                "priority": "MEDIUM"
            }
        ]), 200

    # ── Step 10: Return recommendations array
    return jsonify(result), 200


# ─────────────────────────────────────────
# GET /health
# ─────────────────────────────────────────
@ai_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "port": 5000
    }), 200