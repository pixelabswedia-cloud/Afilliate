import os
import datetime
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate_blog():
    # Bagian Identitas Statis (Tidak akan berubah)
    header_html = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saka Crypto Hub & Monitoring</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-white font-sans">
        <nav class="p-5 border-b border-gray-800 flex justify-between items-center bg-gray-900 sticky top-0 z-50">
            <h1 class="text-2xl font-bold text-yellow-500">Saka<span class="text-white">Crypto</span></h1>
            <div class="space-x-4 text-sm">
                <a href="#proyek" class="hover:text-yellow-500">Proyek</a>
                <a href="https://sakawebsite.github.io/" class="hover:text-yellow-500 font-bold">Portfolio</a>
            </div>
        </nav>

        <section class="max-w-4xl mx-auto p-6 mt-10">
            <div class="bg-gray-800 p-8 rounded-2xl border border-gray-700 shadow-xl">
                <h2 class="text-3xl font-bold mb-4">Crypto Bot & Monitoring System</h2>
                <p class="text-gray-400 mb-6">Halo, saya <strong>Saka</strong>. Saya mengembangkan sistem bot WhatsApp untuk tracking saldo OKX dan monitoring aset kripto secara real-time. Di bawah ini adalah analisis pasar yang diperbarui otomatis oleh sistem AI saya.</p>
                <div class="flex gap-4">
                    <a href="https://wa.me/628XXXXXXXX" class="bg-green-600 px-4 py-2 rounded-lg font-bold">Hubungi Bot</a>
                    <a href="#ai-insight" class="bg-yellow-600 px-4 py-2 rounded-lg font-bold">Cek Market Insight</a>
                </div>
            </div>
        </section>
    """

    # Bagian Footer Statis
    footer_html = f"""
        <footer class="mt-20 p-10 border-t border-gray-800 text-center text-gray-500">
            <p>&copy; {datetime.datetime.now().year} Developed by Saka. System Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </footer>
    </body>
    </html>
    """

    # Prompt untuk bagian DINAMIS saja
    prompt = """
    Buatlah ringkasan singkat analisis pasar Crypto hari ini (fokus ke BTC, ETH, dan SOL). 
    Berikan tips trading singkat. 
    Format dalam HTML menggunakan Tailwind CSS:
    - Gunakan grid 3 kolom untuk harga.
    - Gunakan kartu (cards) dengan background bg-gray-800 dan border-gray-700.
    - Berikan indikator warna (hijau/merah) untuk tren.
    Hanya berikan kode HTML isi saja (tanpa tag html/body).
    """

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional Crypto Analyst. Output only HTML div sections."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
        )
        
        ai_content = completion.choices[0].message.content.strip()
        
        # Bersihkan dari tanda markdown jika ada
        if "```" in ai_content:
            ai_content = ai_content.split("```")[1].replace("html", "").strip()

        # Gabungkan semua bagian
        final_page = header_html + f"<section id='ai-insight' class='max-w-4xl mx-auto p-6'>" + ai_content + "</section>" + footer_html

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(final_page)
            
        print("Success: Landing page updated with Fixed Bio and AI Crypto Insight!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_blog()
