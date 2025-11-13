from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
from fuzzywuzzy import process 
import os # Import os for directory check

# Requires: pip install fuzzywuzzy python-levenshtein

app = Flask(__name__, static_folder="static")
CORS(app)  # allow frontend access

# ------------------------------
# ASSISTANT LOGIC
# ------------------------------
responses = {
    "what is gravity": "Gravity is a force that attracts objects toward each other.",
    "who discovered electricity": "Benjamin Franklin is famous for his kite experiment in 1752.",
    # This is a callable function, it will run when asked
    "what is the time": lambda: f"The current time is {datetime.now().strftime('%H:%M')}", 
    "who created you": "I was created by students of class 10th with the help of our AI teacher.",
    "what is the speed of light": "The speed of light in vacuum is approximately 299,792,458 meters per second.",
    "who is the principal of school": "The principal of the school is Mr. Pradipta Kumar Samal.",
    "who is the director of the school": "The director of the school is Dr.Mayank Kant Singhal.",
    "when is the lunch break": "The lunch break is from 12:30 PM to 1:00 PM.",
    "what is photosynthesis": "Photosynthesis is the process in which green plants use sunlight to produce food from carbon dioxide and water.",
    "who invented the telephone": "The telephone was invented by Alexander Graham Bell in 1876.",
    "what is your name": "I am your school query answering assistant.",
    "how are you": "I am just a program, but thank you for asking!",
    "what is the time": lambda: f"The current time is {datetime.now().strftime('%H:%M')}",
    "who created you": "I was created by students of class 10th with the help of our AI teacher.",
    "what is the school schedule": "The school opens at 8:00 AM. Classes start at 7:30 AM and end at 2:00 PM.",
    "who is the teacher of AI": "The teacher for AI is Mr. Surender Singh Saini.",
    "what is the homework": "Your homework for today is to complete page 45 in your Math workbook.",
    "where is the library": "The library is located on the ground floor.",
    "when is the next holiday": "The next holidays are from June 20th, Summer vacation.",
    "who is the head of the science department": "Dr. Anita Sharma is the head of the science department.",
    "how do I contact the school office": "You can contact the school office at 9587384459 or email www.vmpsschool.com .",
    "What’s the school’s address?": "Our address is Padampur Road 12PS,Raisinghnagar.",
    "Where can I find the school calendar?": "You can find the school calendar on our website.",
    "What’s the procedure for picking up a student early?": "A parent or guardian must sign the student out at the front office withproper ID.",
    "How do I request a meeting with a teacher?": "You can email the teacher directly or call the school office to schedule an appointment.",
    "How do I enroll my child in the school?": "Visit our admissions office or our website for the application form and requirements",
    "What documents are required for enrollment?": "You’ll need proof of residence, birth certificate, immunization records, and prior school transcripts.",
    "Does the school accept transfer students?": "Yes, transfer students are accepted based on availability and academic records.",
    "Is there an entrance exam for new students?": "Yes, students may need to take an assessment for placement.",
    "How much is the tuition?": "Tuition fees vary; please check our website or contact the finance office for details.",
    "Are scholarships available?": "Yes, we offer merit-based and need-based scholarships.",
    "Does the school offer financial aid?": "Yes, financial aid applications are available through the finance office.",
    "What age groups does the school cater to?": "We accept students from age 3 to 18.",
    "Can I schedule a school tour?": "Yes, tours are available by appointment. Contact the admissions office.",
    "What curriculum does the school follow?": "We follow [mention curriculum, e.g., IB, CBSE, National Curriculum].",
    "What are the core subjects taught?": "Our core subjects include Math, Science, English, History, and [list other subjects].",
    "How are students graded?": "Students are graded based on tests, assignments, participation, and projects.",
    "Does the school have a special education program?": "Yes, we have resources for students with special learning needs.",
    "Does the school offer extracurricular academic clubs?": "Yes, we have clubs for robotics, debate, science, and more.",
    "Does the school have a library?": "Yes, the library is open during school hours.",
    "Is there a cafeteria?": "Yes, the cafeteria serves meals during lunch hours.",
    "What kind of sports facilities are available?": "We have football field, volleyball and basketball court.",
    "Does the school provide transportation?": "Yes, bus services are available for eligible students.",
    "How can parents contact teachers?": "Parents can email teachers or schedule an appointment through the office.",
    "How does the school communicate important updates?": "Updates are sent via email, text messages, and posted on the school website.",
    "Can parents volunteer at the school?": "Yes, parents can sign up for volunteer opportunities through the PTA.",
    "How can parents monitor their child’s grades?": "Parents can check grades through the online student portal.",
    "What is the policy on parent-teacher conferences?": "Conferences are scheduled twice a year, but parents can request additional meetings.",
    "what is your name": "I am your school query answering assistant."
}
# Normalize keys for fuzzy matching
normalized_responses = {k.lower(): v for k, v in responses.items()}


def find_best_match(query):
    """Find closest matching question key using fuzzy logic"""
    # The keys must be strings for fuzzy matching
    best = process.extractOne(query, normalized_responses.keys())
    # Return the key if the match score is high enough (85% confidence)
    return best[0] if best and best[1] > 85 else None

# ------------------------------
# ROUTES
# ------------------------------

# Route to serve the main HTML file from the static folder
@app.route("/")
def home():
    # Sends the INDEXAI1.html file located in the 'static' folder
    return send_from_directory(app.static_folder, "INDEXAI1.html")

# Route to handle the assistant's query (API Endpoint)
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "").lower()
    best = find_best_match(query)
    
    answer = "I don't know the answer to that."
    
    if best:
        response_data = normalized_responses[best]
        if callable(response_data):  # Check if the response is a function (like 'what is the time')
            answer = response_data()
        else:
            answer = response_data
            
    # FIXED: The pyttsx3 call 'speak(answer)' is permanently removed.
    # We simply return the text answer in a JSON object.
    return jsonify({"answer": answer})
        
# ------------------------------
if __name__ == "__main__":
    # Ensure the static directory exists
    if not os.path.exists("static"):
        os.makedirs("static")
    
    print("✅ Assistant running at http://127.0.0.1:5000")
    app.run(debug=True)
