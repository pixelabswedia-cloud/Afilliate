import os
from groq import Groq

# Pastikan kamu sudah menyimpan GROQ_API_KEY di GitHub Secrets
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY tidak ditemukan!")
    exit(1)

client = Groq(api_key=api_key)

def generate_blog():
    # Prompt yang sangat ketat untuk memastikan output adalah HTML murni yang siap pakai
    prompt = """
    Buatlah landing page blog profesional tentang 'Tren Harga Pangan Indonesia 2026'.
    
    SYARAT WAJIB:
    1. Output HANYA kode HTML murni (lengkap dari <!DOCTYPE html> sampai </html>).
    2. WAJIB sertakan <script src="https://cdn.tailwindcss.com"></script> di bagian <head>.
    3. Desain harus mobile-friendly (responsive) karena pembaca banyak menggunakan HP.
    4. Tambahkan bagian 'Daftar Harga' menggunakan tabel atau grid yang rapi dengan Tailwind.
    5. JANGAN memberikan teks penjelasan, pembuka, atau penutup. Langsung kodenya saja.
    """
    
    try:
        print("Sedang meminta konten ke Groq AI...")
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert Web Developer. You only output pure HTML code. No talk, no explanations, no markdown ticks."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant", # Model gratis, cepat, dan pintar
            temperature=0.6,
        )
        
        raw_content = completion.choices[0].message.content.strip()
        
        # LOGIKA PEMBERSIH: Menghapus tanda ```html jika AI tetap memberikannya
        final_content = raw_content
        if "```html" in raw_content:
            final_content = raw_content.split("```html")[1].split("```")[0].strip()
        elif "```" in raw_content:
            final_content = raw_content.split("```")[1].split("```")[0].strip()

        # Simpan ke file index.html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(final_content)
            
        print("BERHASIL: File index.html telah diperbarui dengan HTML murni.")
        
    except Exception as e:
        print(f"GAGAL: Terjadi error saat proses: {e}")
        exit(1)

if __name__ == "__main__":
    generate_blog()
