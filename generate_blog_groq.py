import os
import datetime
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate_web_pro():
    # 1. Header & Navigation (Identitas Saka)
    header_html = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SakaMarketCap | Real-Time News & Prices</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .crypto-row:hover { background-color: rgba(255, 255, 255, 0.03); }
            canvas { max-width: 100px !important; max-height: 35px !important; }
            .news-card:hover { border-color: #eab308; transition: 0.3s; }
        </style>
    </head>
    <body class="bg-[#0b0e11] text-white font-sans">
        <nav class="sticky top-0 z-50 bg-[#0b0e11]/90 backdrop-blur-md border-b border-gray-800 p-4">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <div class="bg-yellow-500 p-2 rounded-lg text-black font-bold">S</div>
                    <span class="text-xl font-bold tracking-tight">Saka<span class="text-yellow-500">MarketCap</span></span>
                </div>
                <div class="flex gap-4 items-center">
                    <a href="https://sakawebsite.github.io/" class="text-sm hover:text-yellow-500 hidden sm:block">Portfolio</a>
                    <a href="https://wa.me/628XXXXXXXXXX" class="bg-yellow-600 hover:bg-yellow-700 px-4 py-2 rounded-full text-xs font-bold transition">Pesan Bot</a>
                </div>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto p-4 md:p-6">
            <section class="mb-10">
                <div class="flex justify-between items-end mb-4">
                    <div>
                        <h1 class="text-2xl font-bold">Harga Pasar Global</h1>
                        <p class="text-gray-400 text-sm">Data diperbarui otomatis setiap menit.</p>
                    </div>
                </div>
                
                <div class="overflow-x-auto bg-[#171924] rounded-2xl border border-gray-800 shadow-2xl">
                    <table class="w-full text-left">
                        <thead class="border-b border-gray-800 text-gray-500 text-[10px] uppercase tracking-wider">
                            <tr>
                                <th class="p-4">Koin</th>
                                <th class="p-4 text-right">Harga (IDR)</th>
                                <th class="p-4 text-right">24h %</th>
                                <th class="p-4 text-center">Trend 7D</th>
                            </tr>
                        </thead>
                        <tbody id="crypto-table-body" class="text-sm">
                            </tbody>
                    </table>
                </div>
            </section>

            <section class="mb-10">
                <div class="flex items-center gap-2 mb-6">
                    <div class="h-2 w-2 bg-red-600 rounded-full animate-pulse"></div>
                    <h2 class="text-xl font-bold italic uppercase tracking-widest">News Flash</h2>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {{{{AI_NEWS}}}}
                </div>
            </section>
    """

    footer_html = f"""
        </main>

        <footer class="p-10 border-t border-gray-800 text-center text-gray-500 text-xs">
            <p class="mb-2">SakaMarketCap &copy; {datetime.datetime.now().year}</p>
            <p>Sistem ini dijalankan secara otomatis menggunakan Groq AI & GitHub Actions</p>
        </footer>

        <script>
            async function fetchCrypto() {{
                try {{
                    const res = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=idr&order=market_cap_desc&per_page=8&page=1&sparkline=true');
                    const data = await res.json();
                    const tbody = document.getElementById('crypto-table-body');
                    tbody.innerHTML = '';

                    data.forEach(coin => {{
                        const isUp = coin.price_change_percentage_24h > 0;
                        const color = isUp ? '#22c55e' : '#ef4444';
                        
                        tbody.innerHTML += `
                            <tr class="border-b border-gray-800/50 crypto-row">
                                <td class="p-4 flex items-center gap-3">
                                    <img src="${{coin.image}}" class="w-5 h-5">
                                    <span class="font-bold">${{coin.symbol.toUpperCase()}}</span>
                                </td>
                                <td class="p-4 text-right font-mono text-xs font-bold tracking-tighter">
                                    ${{coin.current_price.toLocaleString('id-ID')}}
                                </td>
                                <td class="p-4 text-right ${{isUp ? 'text-green-500' : 'text-red-500'}} text-xs">
                                    ${{isUp ? '▲' : '▼'}} ${{Math.abs(coin.price_change_percentage_24h).toFixed(2)}}%
                                </td>
                                <td class="p-4"><canvas id="c-${{coin.id}}" width="100" height="35"></canvas></td>
                            </tr>
                        `;

                        setTimeout(() => {{
                            const ctx = document.getElementById(`c-${{coin.id}}`).getContext('2d');
                            new Chart(ctx, {{
                                type: 'line',
                                data: {{
                                    labels: coin.sparkline_in_7d.price,
                                    datasets: [{{
                                        data: coin.sparkline_in_7d.price,
                                        borderColor: color,
                                        borderWidth: 1.5,
                                        pointRadius: 0,
                                        fill: false,
                                        tension: 0.4
                                    }}]
                                }},
                                options: {{ responsive: false, plugins: {{ legend: {{display:false}}, tooltip: {{enabled:false}} }}, scales: {{ x:{{display:false}}, y:{{display:false}} }} }}
                            }});
                        }}, 100);
                    }});
                }} catch(e) {{ console.log(e); }}
            }}
            fetchCrypto();
            setInterval(fetchCrypto, 60000);
        </script>
    </body>
    </html>
    """

    # 2. Prompt News Flash untuk Groq
    news_prompt = """
    Bertindaklah sebagai jurnalis crypto handal. Buatlah 3 berita crypto paling viral atau penting untuk hari ini.
    
    FORMAT OUTPUT:
    Berikan 3 elemen <div> saja. Setiap <div> harus memiliki class:
    'bg-[#171924] p-5 rounded-xl border border-gray-800 news-card'
    
    Isi setiap div:
    1. <span class='text-[10px] text-yellow-500 font-bold uppercase'>Hot News</span>
    2. <h3 class='font-bold text-sm my-2 text-white'>[Judul Berita]</h3>
    3. <p class='text-xs text-gray-400 leading-relaxed'>[Ringkasan Berita 2 kalimat]</p>
    
    Ketentuan:
    - Gunakan Bahasa Indonesia.
    - HANYA keluarkan kode HTML <div> tersebut. Jangan ada kata pembuka.
    """

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a professional crypto journalist. Output pure HTML divs only."},
                      {"role": "user", "content": news_prompt}],
            model="llama-3.1-8b-instant",
        )
        ai_news = completion.choices[0].message.content.strip()

        # Bersihkan markdown if any
        if "```" in ai_news:
            ai_news = ai_news.split("```")[1].replace("html", "").strip()

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(header_html.replace("{{{{AI_NEWS}}}}", ai_news) + footer_html)
            
        print("Success: News Flash updated with SakaMarketCap style!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_web_pro()
