from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

# ==========================================
# API KEY IS NOW LOADED FROM ENVIRONMENT VARIABLES FOR SECURITY
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# We configure static_url_path="/" so that <link href="css/styles.css"> 
# seamlessly maps to the backend/static/css folder without changing any HTML!
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
CORS(app)

# Mock Knowledge Base (Used if API Key is not set)
KNOWLEDGE_BASE = {
    "admission": "Admissions for the 2026 academic year at Baderia Global are open. Apply via the main portal or visit the admission office between 10 AM and 4 PM. Required documents: 12th mark sheet, ID proof.",
    "fee": "The fee structure is ₹64,000 per year for B.Tech and ₹1,00,000 (1 Lakh) per year for MBA. Pay online via the student portal.",
    "exam": "Semester examination forms will be released in October. Fill them out through the student portal (fee: ₹1,500).",
    "scholarship": "We offer merit-based scholarships. If you scored >85% in your 12th boards, you are eligible for the Merit Tier 1 scholarship.",
    "contact": "Contact the main office at admin@baderia.edu or call +91-1234567890."
}

def generate_mock_response(query: str) -> str:
    query = query.lower()
    for key, response in KNOWLEDGE_BASE.items():
        if key in query:
            return response
    return "I am the Baderia Global AI Assistant. I couldn't find the exact information for that. Please contact the administration office for further help."

# UI Routes
@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/landing.html")
def landing():
    return render_template("landing.html")

@app.route("/index.html")
def chat_ui():
    return render_template("index.html")

@app.route("/admin-login.html")
def admin_login():
    return render_template("admin-login.html")

@app.route("/admin-dashboard.html")
def admin_dashboard():
    return render_template("admin-dashboard.html")

# API Route
@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            # Context representing a strict RAG system
            system_prompt = """
            You are a helpful, professional AI assistant exclusively for Baderia Global Institute of Engineering and Management (BGIEM), also known as Global Engineering College.
            Your ONLY job is to answer questions related to the college, admissions, fees, courses, and basic polite greetings.
            If the user asks about ANY topic outside of the college (like general world knowledge, coding, sports, etc.), you MUST politely refuse and state that you can only answer questions related to BGIEM.
            
            College Information to use for answers:
            - History & Location: Established in 1999 by Global Nature Care Sangathan (GNCS). Located at Global Square, Patan Bypass, Raigwan, Jabalpur, MP – 482002.
            - Affiliations: Approved by AICTE, affiliated with RGPV Bhopal and RDVV Jabalpur, engaged in NAAC accreditation.
            - Courses: B.Tech & M.Tech (CSE, Civil, Mechanical, EC, AIML, Data Science, IoT & Cyber Security). Diploma in Civil, CSE, Mech. MBA and MBA Hospital Administration.
            - Fees: B.Tech is ₹64,000 per year. MBA is ₹1,00,000 (1 Lakh) per year.
            - Placements & Recruiters: Highest package is 46.71 LPA. 800+ placements with companies like TCS, Wipro, Infosys, Cognizant, L&T, Persistent, Intel, Zscaler, EPAM.
            - Facilities & Campus Life: Wi-Fi classrooms, central library, sports, cafeteria, NCC, R&D cell, entrepreneurship cell, grievance redressal, anti-ragging, women counselling cell.
            - Admissions & Contact: Open for 2026. Contact official admission helplines at 9575300122 and 9575300123.
            
            Keep answers under 3 sentences unless specifically asked for details.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"System Instructions: {system_prompt}\n\nUser Question: {user_message}"
            )
            return jsonify({"response": response.text})
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "Quota" in error_msg:
                # If Google blocks us for asking too fast, secretly fallback to the local mock logic!
                mock_reply = generate_mock_response(user_message)
                return jsonify({"response": mock_reply})
            return jsonify({"response": "I am having trouble connecting to my brain right now. Please try again later."})
    else:
        # Fallback to mock logic if no API key is provided
        mock_reply = generate_mock_response(user_message)
        return jsonify({"response": mock_reply})

if __name__ == "__main__":
    # In production, Render uses gunicorn, but this works for local testing
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
