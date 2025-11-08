# Import required libraries
import pandas as pd
import jellyfish
import textdistance
from fuzzywuzzy import fuzz
import streamlit as st
import random
from nltk.corpus import wordnet
import nltk
import time

nltk.download('wordnet')

# Set page configuration
st.set_page_config(page_title="Title Validator", page_icon="📰", layout="wide")


# Add custom CSS for styling
def add_custom_css():
    st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput input {
        font-size: 18px;
        padding: 12px;
    }
    .stMarkdown {
        font-family: 'Arial', sans-serif;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


add_custom_css()


# Load dataset with precomputed features
@st.cache_data
def load_data():
    df = pd.read_csv("title data.csv")
    # Precompute phonetic hashes during initial load
    df["Soundex"] = df["Title Name"].apply(lambda x: jellyfish.soundex(x.lower()))
    # Precompute lowercase versions
    df["Title_Lower"] = df["Title Name"].str.lower()
    return df


dataset = load_data()

# Configuration parameters
SIMILARITY_THRESHOLD = 0.35 # 40% similarity threshold
VALIDITY_THRESHOLD = 50  # 60% probability required for validity

disallowed_prefixes_suffixes = ["The", "India", "Samachar", "News", "india", "Report", "Bulletin", "Daily", "Times"]
disallowed_words = [
    "Police", "Crime", "Corruption", "CBI", "CID", "Army", "Terrorism", "Violence",
    "Extremism", "Rebellion", "Insurgency", "Propaganda", "Espionage", "Sedition",
    "Revolution", "Narcotics", "Illegal", "Trafficking", "Scandal", "Bribery",
    "Fraud", "Hate", "Racism", "Discrimination", "Abuse", "Exploitation",
    "Pornography", "Obscenity", "Defamation", "Blasphemy"
]

# Precompute disallowed terms sets for faster lookup
disallowed_prefix_set = set(disallowed_prefixes_suffixes)
disallowed_word_set = set(disallowed_words)


# Optimized similarity calculation using vectorization
def calculate_similarity_score(new_title):
    start_time = time.time()
    new_title_lower = new_title.lower()
    new_soundex = jellyfish.soundex(new_title_lower)

    # Vectorized calculations
    dataset["Fuzzy_Score"] = dataset["Title_Lower"].apply(
        lambda x: fuzz.ratio(new_title_lower, x) / 100
    )
    dataset["Soundex_Score"] = dataset["Soundex"].apply(
        lambda x: textdistance.levenshtein.normalized_similarity(new_soundex, x)
    )
    dataset["Combined_Score"] = (dataset["Fuzzy_Score"] + dataset["Soundex_Score"]) / 2

    # Filter and sort results
    similar_titles = dataset[dataset["Combined_Score"] > SIMILARITY_THRESHOLD]
    similar_titles = similar_titles.sort_values("Combined_Score", ascending=False)

    return list(similar_titles[["Title Name", "Combined_Score"]].itertuples(index=False, name=None))


# Optimized checks using sets
def has_disallowed_prefix_suffix(title):
    tokens = set(title.split())
    return not tokens.isdisjoint(disallowed_prefix_set)


def contains_disallowed_words(title):
    tokens = set(title.split())
    return not tokens.isdisjoint(disallowed_word_set)


# Simplified title variation generator
def generate_title_variations(title):
    variations = []
    words = title.split()

    # Synonym replacement with limit
    for i in range(min(len(words), 3)):  # Limit to first 3 words
        synonyms = get_synonyms(words[i])
        if synonyms:
            variations.append(' '.join(words[:i] + [random.choice(synonyms)] + words[i + 1:]))

    # Limited shuffling
    if len(words) > 1:
        shuffled_words = random.sample(words, len(words))
        variations.append(' '.join(shuffled_words))

    return variations[:5]  # Return max 5 variations


def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)[:3]  # Return max 3 synonyms


# Optimized suggestion validation
def suggest_valid_title(new_title, similar_titles):
    existing_titles_lower = set(dataset["Title_Lower"])
    variations = generate_title_variations(new_title)
    valid_variations = []

    for variation in variations:
        var_lower = variation.lower()
        if (var_lower not in existing_titles_lower and
                not contains_disallowed_words(var_lower) and
                not has_disallowed_prefix_suffix(var_lower)):
            valid_variations.append(variation)

    return valid_variations[:3]  # Return max 3 valid suggestions


# Optimized validation function
def is_title_valid(new_title):
    new_title_lower = new_title.lower()

    # Fast initial checks
    if new_title_lower in set(dataset["Title_Lower"]):
        return False, ["Exact match found"], 0, None
    if contains_disallowed_words(new_title_lower):
        return False, ["Contains disallowed words"], 0, None
    if has_disallowed_prefix_suffix(new_title_lower):
        return False, ["Contains disallowed prefixes/suffixes"], 0, None

    # Calculate similarities
    similar_titles = calculate_similarity_score(new_title)

    verification_probability = 100  # Default to 100% if no similarities

    if similar_titles:
        total_similarity = sum(sim for _, sim in similar_titles)
        avg_similarity = total_similarity / len(similar_titles)
        verification_probability = max(0, min(100, 100 - (avg_similarity * 100)))

        sorted_titles = sorted(similar_titles, key=lambda x: x[1], reverse=True)[:3]
        feedback = [f"Similar to '{title}' (score: {sim * 100:.1f}%)" for title, sim in sorted_titles]

        suggested_titles = suggest_valid_title(new_title, sorted_titles)
        valid_suggestions = [(title, 100 - (i * 10)) for i, title in enumerate(suggested_titles)]

        if verification_probability >= VALIDITY_THRESHOLD:
            return True, feedback, verification_probability, valid_suggestions
        else:
            return False, feedback, verification_probability, valid_suggestions

    return True, ["No significant similarities found"], verification_probability, None


# Streamlit UI
st.title("📰 News Title Validation System")

col1, col2 = st.columns([3, 2])
with col1:
    new_title = st.text_input("Enter news title to validate:", placeholder="Enter your news title here...")

if new_title:
    with st.spinner("Analyzing title..."):
        start_time = time.time()
        is_valid, feedback, verification_probability, suggested_titles = is_title_valid(new_title)

    # Results header
    st.markdown("---")

    # Validation result
    if is_valid:
        st.markdown(f"""
        <div class="success-box">
            <h3>✅ Validation Passed</h3>
            <p>Verification Probability: {verification_probability:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="error-box">
            <h3>❌ Validation Failed</h3>
            <p>Verification Probability: {verification_probability:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Similarity analysis
    if feedback:
        st.subheader("Similarity Analysis Report")
        for line in feedback:
            st.markdown(f"- {line}")

    # Suggested titles
    if suggested_titles:
        st.subheader("Recommended Title Suggestions")
        for title, prob in suggested_titles:
            color = "#2ecc71" if prob >= VALIDITY_THRESHOLD else "#e74c3c"
            st.markdown(f"""
            <div style="padding: 15px; border-left: 4px solid {color};
                        margin: 10px 0; background-color: #ffffff;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4>{title}</h4>
                <p style="color: {color}; margin: 0;">Confidence: {prob:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

# Sidebar information
with col2:
    st.markdown("""
    ## 📋 Validation Criteria
    1. **Uniqueness**: Compare with existing titles
    2. **Content Safety**: Check for restricted terms
    3. **Phonetic Originality**: Sound-based similarity check

    ## 📊 Validity Thresholds
    - **Minimum Similarity**: 40%
    - **Validity Requirement**: 50%+ probability

    ℹ️ Titles must pass all checks to be approved
    """)

# Footer
st.markdown("---")
st.markdown("""
<style>
.footer {
    text-align: center;
    padding: 10px;
}
</style>


""", unsafe_allow_html=True)














