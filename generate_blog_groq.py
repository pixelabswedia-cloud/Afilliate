import os
import datetime
from groq import Groq

# 1. KONFIGURASI API (GitHub Secrets)
api_key = os.environ.get("GROQ_API_KEY")
cg_api_key = os.environ.get("CG_API_KEY") 
client = Groq(api_key=api_key)

def generate_web_saka_clean():
    # Menyiapkan API Key untuk dikirim ke JavaScript secara aman
    cg_auth = cg_api_key if cg_api_key else ""

    # 2. STRUKTUR HTML & CSS
    header_html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SakaMarketCap | Pro Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {{ background-color: #0b0e11; color: white; font-family: sans-serif; }}
            .crypto-row:hover {{ background-color: rgba(255, 255, 255, 0.05); cursor: pointer; transition: 0.2s; }}
            .market-table-row:nth-child(even) {{ background-color: rgba(255,255,255,0.02); }}
            body::-webkit-scrollbar {{ width: 5px; }}
            body::-webkit-scrollbar-thumb {{ background: #374151; border-radius: 10px; }}
        </style>
    </head>
    <body>
        
        <div id="coin-modal" class="fixed inset-0 z-[100] hidden bg-[#0b0e11] overflow-y-auto">
            <div class="max-w-5xl mx-auto p-6 md:p-12">
                <button onclick="closeModal()" class="text-gray-400 hover:text-white mb-8 transition">
                    <i class="fas fa-arrow-left mr-2"></i> Kembali
                </button>
                <div id="modal-content"></div>
            </div>
        </div>

        <nav class="sticky top-0 z-50 bg-[#0b0e11]/90 backdrop-blur-md border-b border-gray-800 p-4">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <div class="bg-yellow-500 p-1.5 rounded text-black font-bold">S</div>
                    <span class="text-xl font-bold tracking-tighter">Saka<span class="text-yellow-500">Market</span></span>
                </div>
                <a href="https://wa.me/628XXXXXXXXXX" class="text-[10px] bg-green-600 px-4 py-2 rounded-lg font-bold uppercase tracking-wider">Konsultasi Bot</a>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto p-4 md:p-6">
            <header class="mb-8">
                <h1 class="text-2xl font-bold text-white">Market Update</h1>
                <p class="text-gray-500 text-xs italic">Data Real-time IDR</p>
            </header>
            
            <div class="overflow-x-auto bg-[#171924] rounded-2xl border border-gray-800 mb-12 shadow-2xl">
                <table class="w-full text-left text-sm">
                    <thead class="text-gray-500 text-[10px] uppercase border-b border-gray-800 tracking-widest font-bold">
                        <tr>
                            <th class="p-4"># Koin</th>
                            <th class="p-4 text-right">Harga</th>
                            <th class="p-4 text-right">24j %</th>
                            <th class="p-4 text-center">Trend 7H</th>
                        </tr>
                    </thead>
                    <tbody id="crypto-table-body"></tbody>
                </table>
            </div>

            <h2 class="text-lg font-bold mb-6 flex items-center gap-2 uppercase tracking-tighter">
                <span class="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span> News Flash AI
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20" id="ai-news-container">
                {{{{AI_NEWS}}}}
            </div>
        </main>
    """

    footer_html = f"""
        <footer class="p-10 border-t border-gray-800 text-center text-gray-600 text-[10px]">
            <p>&copy; {datetime.datetime.now().year} SAKA DIGITAL SYSTEMS | DATA BY COINGECKO</p>
        </footer>

        <script>
            let cryptoData = [];
            const AUTH = "{cg_auth}";

            // Fungsi ambil data koin utama
            async function fetchCrypto() {{
                try {{
                    const url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=idr&order=market_cap_desc&per_page=10&page=1&sparkline=true&price_change_percentage=24h';
                    const headers = AUTH ? {{ 'x-cg-demo-api-key': AUTH }} : {{}};
                    const res = await fetch(url, {{ headers }});
                    cryptoData = await res.json();
                    renderTable();
                }} catch(e) {{ console.error("Error utama:", e); }}
            }}

            function renderTable() {{
                const tbody = document.getElementById('crypto-table-body');
                tbody.innerHTML = '';
                cryptoData.forEach((coin, i) => {{
                    const isUp = coin.price_change_percentage_24h > 0;
                    tbody.innerHTML += `
                        <tr onclick="openDetail('${{coin.id}}')" class="border-b border-gray-800/40 crypto-row">
                            <td class="p-4 flex items-center gap-3">
                                <span class="text-[10px] text-gray-600">${{i+1}}</span>
                                <img src="${{coin.image}}" class="w-5 h-5 rounded-full">
                                <span class="font-bold text-white uppercase">${{coin.symbol}}</span>
                            </td>
                            <td class="p-4 text-right font-mono text-xs text-white">Rp ${{coin.current_price.toLocaleString('id-ID')}}</td>
                            <td class="p-4 text-right ${{isUp ? 'text-green-500' : 'text-red-500'}} text-[11px] font-bold">
                                ${{isUp ? '▲' : '▼'}} ${{Math.abs(coin.price_change_percentage_24h).toFixed(2)}}%
                            </td>
                            <td class="p-4 text-center"><canvas id="c-${{coin.id}}" width="100" height="30"></canvas></td>
                        </tr>
                    `;
                    drawChart(coin);
                }});
            }}

            function drawChart(coin) {{
                setTimeout(() => {{
                    const canvas = document.getElementById(`c-${{coin.id}}`);
                    if (!canvas) return;
                    new Chart(canvas.getContext('2d'), {{
                        type: 'line',
                        data: {{
                            labels: coin.sparkline_in_7d.price,
                            datasets: [{{
                                data: coin.sparkline_in_7d.price,
                                borderColor: coin.price_change_percentage_24h > 0 ? '#22c55e' : '#ef4444',
                                borderWidth: 1.5, pointRadius: 0, fill: false, tension: 0.4
                            }}]
                        }},
                        options: {{ responsive: false, plugins: {{ legend:{{display:false}}, tooltip:{{enabled:false}} }}, scales: {{ x:{{display:false}}, y:{{display:false}} }} }}
                    }});
                }}, 200);
            }}

            async function openDetail(id) {{
                const coin = cryptoData.find(c => c.id === id);
                const modal = document.getElementById('coin-modal');
                const content = document.getElementById('modal-content');
                modal.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
                
                content.innerHTML = `
                    <div class="mb-10">
                        <div class="flex items-center gap-4 mb-4">
                            <img src="${{coin.image}}" class="w-12 h-12 shadow-xl">
                            <h2 class="text-4xl font-bold text-white uppercase">${{coin.name}}</h2>
                        </div>
                        <div class="flex items-baseline gap-4">
                            <span class="text-5xl font-bold font-mono text-white">Rp ${{coin.current_price.toLocaleString('id-ID')}}</span>
                            <span class="text-lg ${{coin.price_change_percentage_24h > 0 ? 'text-green-500' : 'text-red-500'}} font-bold uppercase">
                                ${{coin.price_change_percentage_24h.toFixed(2)}}%
                            </span>
                        </div>
                    </div>

                    <div class="bg-[#171924] rounded-2xl border border-gray-800 overflow-hidden shadow-2xl mb-10">
                        <div class="p-4 border-b border-gray-800 bg-gray-800/20 font-bold text-sm text-yellow-500 uppercase tracking-widest">Market Listings</div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-[11px]">
                                <thead class="text-gray-500 uppercase border-b border-gray-800">
                                    <tr><th class="p-4">Exchange</th><th class="p-4 text-center">Pairs</th><th class="p-4 text-right">Price</th></tr>
                                </thead>
                                <tbody id="market-list-body">
                                    <tr><td colspan="3" class="p-10 text-center text-gray-600 italic animate-pulse">Menghubungkan ke Bursa...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                `;
                fetchTickers(id);
            }}

            async function fetchTickers(coinId) {{
                const tbody = document.getElementById('market-list-body');
                try {{
                    const url = 'https://api.coingecko.com/api/v3/coins/' + coinId + '/tickers?include_exchange_logo=true';
                    const headers = AUTH ? {{ 'x-cg-demo-api-key': AUTH }} : {{}};
                    const res = await fetch(url, {{ headers }});
                    const data = await res.json();
                    
                    if (!data.tickers || data.tickers.length === 0) {{
                        tbody.innerHTML = '<tr><td colspan="3" class="p-10 text-center text-gray-500">Data pasar tidak tersedia.</td></tr>';
                        return;
                    }}

                    tbody.innerHTML = '';
                    data.tickers.slice(0, 8).forEach(t => {{
                        tbody.innerHTML += `
                            <tr class="border-b border-gray-800/50 market-table-row transition">
                                <td class="p-4 flex items-center gap-3 font-bold text-white uppercase">
                                    <img src="${{t.market.logo}}" class="w-4 h-4 rounded-full bg-white p-0.5" onerror="this.src='https://cdn-icons-png.flaticon.com/512/25/25231.png'">
                                    ${{t.market.name}}
                                </td>
                                <td class="p-4 text-blue-400 text-center uppercase font-bold">${{t.base}}/${{t.target}}</td>
                                <td class="p-4 text-right font-mono text-white font-bold">
                                    Rp ${{t.converted_last.idr ? t.converted_last.idr.toLocaleString('id-ID') : '---'}}
                                </td>
                            </tr>
                        `;
                    }});
                }} catch(e) {{ tbody.innerHTML = '<tr><td colspan="3" class="p-10 text-center text-red-500">Gagal memuat pasar.</td></tr>'; }}
            }}

            function closeModal() {{ document.getElementById('coin-modal').classList.add('hidden'); document.body.style.overflow = 'auto'; }}

            fetchCrypto();
            setInterval(fetchCrypto, 60000);
        </script>
    </body>
    </html>
    """

    # 3. LOGIKA AI (GROQ) DENGAN FAIL-SAFE
    news_prompt = "Buat 3 berita singkat crypto viral hari ini dalam Bahasa Indonesia. Output HANYA kode HTML tanpa penjelasan. Gunakan 3 div dengan class 'bg-[#171924] p-6 rounded-2xl border border-gray-800 news-card shadow-lg'."

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a clean HTML generator. No chatter."}, {"role": "user", "content": news_prompt}],
            model="llama-3.1-8b-instant",
        )
        ai_news = completion.choices[0].message.content.strip()
        
        # Pembersihan Markdown AI
        if "```" in ai_news:
            ai_news = ai_news.split("```")[1].replace("html", "").strip()
            
        # Fail-safe: Jika AI error/kosong, pasang berita cadangan agar web tidak rusak
        if len(ai_news) < 100:
            ai_news = "<div class='p-6 bg-gray-800/20 border border-gray-800 rounded-xl text-gray-500 text-xs italic text-center col-span-3'>Berita sedang diperbarui oleh Saka AI...</div>"

    except Exception as e:
        print(f"AI Error: {e}")
        ai_news = "<div class='p-6 bg-gray-800/20 border border-gray-800 rounded-xl text-gray-500 text-xs italic text-center col-span-3'>Sistem AI sedang sibuk. Silakan refresh.</div>"

    # 4. WRITE KE FILE
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(header_html.replace("{{{{AI_NEWS}}}}", ai_news) + footer_html)
    
    print("SakaMarketCap Clean Build Success!")

if __name__ == "__main__":
    generate_web_saka_clean()
