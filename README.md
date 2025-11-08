
# 📰 Automated Similarity Check of Title Submissions Using Phonetic and Fuzzy Matching Algorithms

## 📖 Overview
This project, **"Automated Similarity Check of Title Submissions Using Phonetic and Fuzzy Matching Algorithms"**, is designed to ensure **uniqueness, ethical compliance, and phonetic distinction** of news or article titles.  
The system combines **phonetic matching (Soundex)** and **fuzzy logic (Levenshtein distance)** to automatically detect duplicate or similar titles, improving originality and ethical publishing standards.

Developed with **Python** and **Streamlit**, the tool provides a real-time interface that validates news titles, checks for ethical words, and suggests alternative titles using synonym substitution via **WordNet**.

---

## ⚙️ Features
- ✅ **Phonetic Matching (Soundex):** Detects titles that sound alike but are spelled differently.  
- ✅ **Fuzzy Matching (Levenshtein Distance):** Measures text similarity to find near-duplicate titles.  
- ✅ **Ethical Content Filtering:** Flags titles containing restricted or unethical terms.  
- ✅ **Title Suggestions:** Generates new, valid, and ethical title alternatives.  
- ✅ **Interactive Web Interface:** Built with Streamlit for instant feedback.  
- ✅ **Optimized Performance:** Uses caching, vectorized operations, and preprocessed data for speed.  

---

## 🧠 Technologies Used
| Category | Tools & Libraries |
|-----------|------------------|
| Frontend | Streamlit |
| Backend | Python |
| NLP & Matching | fuzzywuzzy, textdistance, jellyfish, nltk |
| Data Processing | pandas |
| Phonetic Algorithm | Soundex |
| Fuzzy Matching | Levenshtein Distance |
| Synonym Generation | WordNet (NLTK) |

---

## 🧩 System Architecture
The project consists of three main modules:

1. **Title Similarity Detection** – Uses Soundex and Levenshtein Distance to calculate a composite similarity score.  
2. **Ethical Content Filtering** – Flags inappropriate or sensitive words using a predefined blacklist.  
3. **Title Suggestion Module** – Suggests alternative valid titles using synonym replacement and word rearrangement.

---

## 🚀 How It Works
1. **Input a News Title** through the Streamlit web app.  
2. **Phonetic and Fuzzy Matching** calculates similarity with existing dataset titles.  
3. **Ethical Filtering** checks for disallowed or restricted words.  
4. **Validation Result** displays as:
   - ✅ Valid (Unique & Ethical)
   - ❌ Invalid (Too Similar or Contains Restricted Terms)  
5. **Alternative Suggestions** are generated for invalid titles.

---

## 🧪 Example Output

**Input:**  
> "Breaking News: Government Announces New Policy"

**Output:**  
- ✅ **Status:** Valid (Unique & Ethical)  
- 💡 **Suggestions (if invalid):**  
  - "Government Unveils New Policy Update"  
  - "New Policy Announcement by Government"  

---

## 📂 Project Structure
```
📁 Automated-Title-Validator
├── title_validator1.py      # Core validation logic
├── title.py                 # Streamlit interface for user interaction
├── requirements.txt         # Dependencies list
├── data/
│   └── titles.csv           # Dataset of existing titles
├── README.md                # Project documentation
└── report/
    └── AUTOMATED SIMILARITY CHECK.pdf  # Project report
```

---

## 💻 Installation & Usage

### Prerequisites
- Python 3.8 or above  
- Install dependencies using:
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
streamlit run title.py
```

---

## 📊 Results & Performance
- High accuracy in identifying duplicate and similar titles.  
- Optimized runtime with caching and preprocessed phonetic hashes.  
- Real-time validation and feedback through Streamlit interface.  

---

## 🔮 Future Enhancements
- Cloud database integration for real-time validation.  
- Deep learning models (BERT, GPT) for semantic understanding and synonym generation.  
- Multi-language title validation support.  

---

## 👨‍💻 Contributors
- Ms. Ch. Lakshmi Veenadhari  
- Mr. Madala Tejvarsith  
- Mr. Kosuru Surya Sai  
- Ms. Meda Mohanasrivarsitha  
- Mr. Mutyala Sriramsai  
- Mr. Mutyala B.N.D.Muralikrishna  

**Department of Computer Science and Engineering**  
Vishnu Institute of Technology, Bhimavaram, India  

---

## 🏁 Conclusion
The **Automated Title Validator** is a robust and intelligent tool that ensures originality and ethical integrity in news and media publications.  
It uses **AI-powered text comparison techniques** to reduce redundancy, maintain credibility, and promote responsible journalism.

---
