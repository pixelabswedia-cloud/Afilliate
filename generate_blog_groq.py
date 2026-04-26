import os
from groq import Groq

# Mengambil API Key dari Secrets GitHub
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY tidak ditemukan di environment variables.")
    exit(1)

client = Groq(api_key=api_key)

def generate_content():
    prompt = "Buatlah artikel blog singkat tentang tren harga pangan di Indonesia menggunakan format HTML sederhana dengan Tailwind CSS classes."
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "Kamu adalah asisten penulis blog profesional yang ahli dalam SEO dan HTML/Tailwind CSS."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            # Menggunakan model Llama 3.1 8B yang sangat cepat dan gratis
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=2048,
        )
        
        content = completion.choices[0].message.content
        
        # Simpan hasil ke file index.html atau sesuai folder blog kamu
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("Konten blog berhasil dibuat!")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        exit(1)

if __name__ == "__main__":
    generate_content()
