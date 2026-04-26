import os
from groq import Groq

# Mengambil API Key dari Secrets GitHub
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY tidak ditemukan di environment variables.")
    exit(1)

client = Groq(api_key=api_key)

def generate_content():
    # Prompt lebih ketat agar tidak ada teks basa-basi
    prompt = """
    Buatlah artikel blog tentang harga pangan Indonesia. 
    WAJIB memberikan HANYA kode HTML murni. 
    Sertakan link CDN Tailwind CSS di dalam <head>.
    Struktur harus lengkap: <!DOCTYPE html>, <html>, <head>, <body>.
    Gunakan container agar konten berada di tengah dan terlihat profesional di HP.
    JANGAN berikan penjelasan teks apa pun di luar tag HTML.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional web developer. Always output pure HTML code with Tailwind CDN. No conversational text."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
        )
        
        content = completion.choices[0].message.content.strip()
        
        # Membersihkan jika AI masih nakal memberikan markdown ```html
        if "```html" in content:
            content = content.split("```html")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("Konten blog berhasil diperbarui dengan struktur HTML lengkap!")
