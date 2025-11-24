📘 Nirmaan AI – Self-Introduction Scoring Tool
==============================================

A lightweight, transparent evaluation tool built for the Nirmaan Education AI/ML Internship Case Study.The system analyses a student’s spoken introduction (via transcript) and scores it using the exact rubric defined in the case study.

✨ Overview
----------

This project is designed to demonstrate **product-oriented problem solving**, not just coding.The goal was to build a small but reliable tool that:

*   Accepts a **transcript** of a student’s introduction
    
*   Accepts **duration in seconds**
    
*   Evaluates the introduction across all rubric categories
    
*   Returns a structured **100-point score**, along with a detailed breakdown
    

The scoring follows the same criteria and weighting provided in the case study PDF.

🧠 Rubric Criteria Implemented
------------------------------

The tool computes scores for all 5 categories:

### **1\. Content & Structure (40 points)**

*   Salutation level
    
*   Keyword presence (must-have & good-to-have details)
    
*   Logical flow (salutation → basics → details → closing)
    

### **2\. Speech Rate (10 points)**

*   Words per minute
    
*   Categorized based on ideal ranges from the rubric
    

### **3\. Language & Grammar (20 points)**

Since the original LanguageTool requires Java or API limits,this project uses a **local, offline grammar approximation**:

*   Spelling error count (via pyspellchecker)
    
*   TTR (Type-Token Ratio) for vocabulary richness
    

### **4\. Clarity (15 points)**

*   Filler word detection
    
*   Filler word rate mapping to rubric scores
    

### **5\. Engagement (15 points)**

*   Positivity probability using VADER sentiment analysis
    

🛠️ Tech Stack
--------------

*   **Python 3.12**
    
*   **Flask** (for the minimal web interface)
    
*   **PySpellChecker** (grammar approximation)
    
*   **VADER Sentiment**
    
*   **Bootstrap** (light styling)
    

Everything runs **locally**, offline, and without any Java dependency.

📂 Project Structure
--------------------

```
nirmaan-case-study/
│
├── app.py               # Flask server
├── scoring.py           # Full scoring logic based on rubric
├── requirements.txt     # Install dependencies
│
├── templates/
│   └── index.html       # Minimal UI
│
└── README.md

```

🚀 How to Run Locally
---------------------

### **1\. Clone the repository**

`   git clone https://github.com/CodesbyHim/Nirmaan-Case-Study.git  cd Nirmaan-Case-Study   `

### **2\. Create a virtual environment (recommended)**

`   python -m venv venv  venv\Scripts\activate   # Windows   `

### **3\. Install dependencies**

`   pip install -r requirements.txt   `

### **4\. Start the Flask server**

`   python app.py   `

### **5\. Open the app**

Visit:👉 [**http://127.0.0.1:5000**](http://127.0.0.1:5000)

Paste a transcript + duration → get the score instantly.

🧪 Example Input
----------------

Try it with the sample given in the case study:

**Transcript:**

`   Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School.  I am 13 years old. I live with my family. There are 3 people in my family...  Thank you for listening.   `

**Duration:**

`   52   `

This example should produce a total score around **85–87**, depending on spelling variation.

🎯 Design Choices & Reasoning
-----------------------------

To meet the expectations of the case study, the tool focuses on:

### **✔ Transparency**

Every scoring step is rule-based and visible in the output.

### **✔ Reproducibility**

No cloud APIs, no hidden models, no rate-limits.

### **✔ Simplicity over complexity**

The goal is to demonstrate structured thinking, not heavyweight NLP.

### **✔ Faithfulness to the rubric**

All weights, ranges, and criteria match the official case study.

### **✔ Extendability**

The scoring logic is modular — easy to replace grammar checker, expand rubric, or integrate speech-to-text later.

📌 Limitations
--------------

A few notes to keep expectations grounded:

*   Grammar scoring uses spell-checking + heuristics (not a full parser).
    
*   Names sometimes get flagged as spelling errors (expected).
    
*   Flow detection uses simple positional heuristics.
    

These choices were made deliberately to keep the solution **fully local**, **simple**, and **functional**, as the case study requested.

📎 Future Improvements (if needed)
----------------------------------

*   Add spaCy NER for more accurate detail extraction
    
*   Replace heuristic grammar scoring with a local LLM or grammar engine
    
*   Integrate speech-to-text to allow audio uploads
    
*   Add downloadable score reports (PDF)
    

👨‍💻 Author
------------

**Himanshu Khakre**
Built as part of the **Nirmaan Education AI/ML Internship Case Study**.
