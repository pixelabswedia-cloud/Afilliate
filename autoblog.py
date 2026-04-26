import google.generativeai as genai
import os

# Konfigurasi Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

def generate_blog_post(topic):
    prompt = f"""
    Write a professional blog post in English about the health benefits of {topic}.
    Target audience: Health-conscious people in the US and Europe.
    Structure:
    1. Catchy Title
    2. Introduction with scientific context
    3. 3 Key Benefits (based on research)
    4. How to use/consume
    5. Conclusion and medical disclaimer
    Use clean HTML tags like <h2>, <p>, and <ul>.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Contoh penggunaan: Membuat konten tentang Ashwagandha
topics = ["Ashwagandha for Stress", "Lion's Mane for Brain Fog", "Rhodiola Rosea Benefits"]
# Daftar topik berdasarkan riset keyword global
topics = [
    "Benefits of Lion's Mane for Cognitive Function",
    "How Ashwagandha Helps Lower Cortisol Levels",
    "Berberine: The Natural Solution for Metabolic Health",
    "Rhodiola Rosea for Professional Burnout Recovery",
    "Best Herbal Teas for Deep REM Sleep",
    "The Science Behind Holy Basil and Stress Management"
]
for topic in topics:
    content = generate_blog_post(topic)
    filename = f"blog-{topic.lower().replace(' ', '-')}.html"
    
    with open(filename, "w") as f:
        f.write(content)
    print(f"Successfully created: {filename}")
