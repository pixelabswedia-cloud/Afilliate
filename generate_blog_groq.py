import os
import datetime
from groq import Groq

# Ambil API KEY dari GitHub Secrets
api_key = os.environ.get("GROQ_API_KEY")
cg_api_key = os.environ.get("CG_API_KEY") # Tambahkan ini di GitHub Secrets
client = Groq(api_key=api_key)

def generate_web_pro_final():
    # Gunakan API Key jika ada, jika tidak kosongkan (agar tidak error)
    cg_key_js = cg_api_key if cg_api_key else ""

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
            .crypto-row:hover {{ background-color: rgba(255, 255, 255, 0.05); cursor: pointer; }}
            .news-card:hover {{ border-color: #eab308; transform: translateY(-3px); transition: 0.3s; }}
            body::-webkit-scrollbar {{ width: 5px; }}
            body::-webkit-scrollbar-thumb {{ background: #374151; border-radius: 10px; }}
            .market-table-row:nth-child(even) {{ background-color: rgba(255,255,255,0.02); }}
        </style>
    </head>
    <body class="bg-[#0b0e11] text-white font-sans">
        
        <div id="coin-modal" class="fixed inset-0 z-[100] hidden bg-[#0b0e11] overflow-y-auto">
            <div class="max-w-5xl mx-auto p-4 md:p-10">
                <nav class="flex justify-between items-center mb-8">
                    <button onclick="closeModal()" class="text-gray-400 hover:text-white flex items-center gap-2">
                        <i class="fas fa-chevron-left"></i> Kembali ke Pasar
                    </button>
                    <div class="text-yellow-500 font-bold text-xs uppercase tracking-widest">Saka Pro Intelligence</div>
                </nav>
                <div id="modal-content"></div>
            </div>
        </div>

        <nav class="sticky top-0 z-50 bg-[#0b0e11]/90 backdrop-blur-md border-b border-gray-800 p-4">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <div class="bg-yellow-500 p-1.5 rounded text-black font-bold text-sm">S</div>
                    <span class="text-lg font-bold tracking-tighter text-white">Saka<span class="text-yellow-500 text-xs">MARKET</span></span>
                </div>
                <div class="flex gap-4">
                    <a href="https://wa.me/628XXXXXXXXXX" class="text-[10px] font-bold bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition uppercase">Pesan Bot WA</a>
                </div>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto p-4 md:p-6">
            <section class="mb-8">
                <h1 class="text-2xl font-bold text-white">Harga Aset Kripto Global</h1>
                <p class="text-gray-500 text-xs mt-1 italic">Update: IDR (Rupiah Indonesia)</p>
            </section>
            
            <div class="overflow-x-auto bg-[#171924] rounded-xl border border-gray-800 mb-12 text-sm">
                <table class="w-full text-left">
                    <thead class="text-gray-500 text-[10px] uppercase border-b border-gray-800 tracking-widest font-bold">
                        <tr>
                            <th class="p-4 font-bold"># Nama Aset</th>
                            <th class="p-4 text-right font-bold">Harga</th>
                            <th class="p-4 text-right font-bold">24j %</th>
                            <th class="p-4 text-center font-bold">Trend 7H</th>
                        </tr>
                    </thead>
                    <tbody id="crypto-table-body"></tbody>
                </table>
            </div>

            <h2 class="text-lg font-bold mb-6 flex items-center gap-2 text-white uppercase tracking-tighter">
                <span class="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span> News Flash AI
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20">
                {{{{AI_NEWS}}}}
            </div>
        </main>
    """

    footer_html = f"""
        <footer class="p-10 border-t border-gray-800 text-center text-gray-600 text-[10px]">
            <p>&copy; {datetime.datetime.now().year} SAKA DIGITAL SYSTEMS | DATA BY COINGECKO PRO</p>
        </footer>

        <script>
            let cryptoData = [];
            const CG_KEY = "{cg_key_js}";

            async function fetchCrypto() {{
                try {{
                    const url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=idr&order=market_cap_desc&per_page=10&page=1&sparkline=true&price_change_percentage=24h';
                    const options = CG_KEY ? {{ headers: {{ 'x-cg-demo-api-key': CG_KEY }} }} : {{}};
                    
                    const res = await fetch(url, options);
                    cryptoData = await res.json();
                    renderTable();
                }} catch(e) {{ console.log("Fetch Crypto Error:", e); }}
            }}

            function renderTable() {{
                const tbody = document.getElementById('crypto-table-body');
                tbody.innerHTML = '';
                cryptoData.forEach((coin, i) => {{
                    const isUp = coin.price_change_percentage_24h > 0;
                    tbody.innerHTML += `
                        <tr onclick="openDetail('${{coin.id}}')" class="border-b border-gray-800/40 crypto-row">
                            <td class="p-4 flex items-center gap-3">
                                <span class="text-[10px] text-gray-600 w-4">${{i+1}}</span>
                                <img src="${{coin.image}}" class="w-5 h-5 rounded-full">
                                <span class="font-bold tracking-tight text-white uppercase">${{coin.symbol}}</span>
                            </td>
                            <td class="p-4 text-right font-mono text-xs tracking-tighter text-white">Rp ${{coin.current_price.toLocaleString('id-ID')}}</td>
                            <td class="p-4 text-right ${{isUp ? 'text-green-500' : 'text-red-500'}} text-[11px] font-bold">
                                ${{isUp ? '▲' : '▼'}} ${{Math.abs(coin.price_change_percentage_24h).toFixed(2)}}%
                            </td>
                            <td class="p-4"><canvas id="c-${{coin.id}}" width="100" height="35"></canvas></td>
                        </tr>
                    `;
                    renderSparkline(coin);
                }});
            }}

            function renderSparkline(coin) {{
                setTimeout(() => {{
                    const el = document.getElementById(`c-${{coin.id}}`);
                    if (!el) return;
                    const ctx = el.getContext('2d');
                    new Chart(ctx, {{
                        type: 'line',
                        data: {{
                            labels: coin.sparkline_in_7d.price,
                            datasets: [{{
                                data: coin.sparkline_in_7d.price,
                                borderColor: coin.price_change_percentage_24h > 0 ? '#22c55e' : '#ef4444',
                                borderWidth: 1.5,
                                pointRadius: 0,
                                fill: false,
                                tension: 0.4
                            }}]
                        }},
                        options: {{ responsive: false, plugins: {{ legend: {{display:false}}, tooltip: {{enabled:false}} }}, scales: {{ x:{{display:false}}, y:{{display:false}} }} }}
                    }});
                }}, 150);
            }}

            async function openDetail(id) {{
                const coin = cryptoData.find(c => c.id === id);
                document.getElementById('coin-modal').classList.remove('hidden');
                document.body.style.overflow = 'hidden';
                
                const content = document.getElementById('modal-content');
                content.innerHTML = `
                    <div class="mb-10">
                        <div class="flex items-center gap-4 mb-4">
                            <img src="${{coin.image}}" class="w-12 h-12">
                            <h2 class="text-3xl font-bold text-white uppercase">${{coin.name}}</h2>
                        </div>
                        <div class="flex items-center gap-4">
                            <span class="text-4xl font-bold font-mono text-white">Rp ${{coin.current_price.toLocaleString('id-ID')}}</span>
                            <span class="bg-${{coin.price_change_percentage_24h > 0 ? 'green' : 'red'}}-600 px-2 py-1 rounded text-xs font-bold text-white uppercase">
                                ${{coin.price_change_percentage_24h.toFixed(2)}}%
                            </span>
                        </div>
                    </div>

                    <div class="bg-[#171924] rounded-2xl border border-gray-800 overflow-hidden mb-8 shadow-2xl">
                        <div class="p-4 border-b border-gray-800 bg-gray-800/20 font-bold text-sm text-yellow-500 uppercase tracking-widest">
                            Pasar Teraktif (Markets)
                        </div>
                        <div class="overflow-x-auto text-[11px]">
                            <table class="w-full text-left">
                                <thead class="text-gray-500 border-b border-gray-800">
                                    <tr>
                                        <th class="p-4 font-bold">Exchange</th>
                                        <th class="p-4 text-center font-bold">Pairs</th>
                                        <th class="p-4 text-right font-bold">Price</th>
                                    </tr>
                                </thead>
                                <tbody id="market-list-body">
                                    <tr><td colspan="3" class="p-10 text-center text-gray-500 italic">Memuat data bursa...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="bg-gray-800/30 p-6 rounded-2xl border border-gray-700">
                        <p class="text-xs text-gray-400 italic">Analisis AI: Pergerakan volume ${{coin.name}} menunjukkan aktivitas tinggi di beberapa bursa utama. Tetap pantau support level.</p>
                    </div>
                `;
                fetchTickers(id);
            }}

            async function fetchTickers(coinId) {{
                const tbody = document.getElementById('market-list-body');
                try {{
                    const url = 'https://api.coingecko.com/api/v3/coins/' + coinId + '/tickers?include_exchange_logo=true';
                    const options = CG_KEY ? {{ headers: {{ 'x-cg-demo-api-key': CG_KEY }} }} : {{}};
                    
                    const res = await fetch(url, options);
                    const data = await res.json();
                    
                    if (!data.tickers || data.tickers.length === 0) {{
                        tbody.innerHTML = '<tr><td colspan="3" class="p-10 text-center text-gray-600">Data market tidak ditemukan.</td></tr>';
                        return;
                    }}

                    tbody.innerHTML = '';
                    data.tickers.slice(0, 8).forEach((t) => {{
                        tbody.innerHTML += `
                            <tr class="border-b border-gray-800/50 market-table-row transition hover:bg-white/5">
                                <td class="p-4 flex items-center gap-3 font-bold text-white uppercase">
                                    <img src="${{t.market.logo}}" class="w-4 h-4 rounded-full bg-white p-0.5" onerror="this.src='https://cdn-icons-png.flaticon.com/512/25/25231.png'">
                                    ${{t.market.name}}
                                </td>
                                <td class="p-4 text-blue-400 text-center uppercase tracking-tighter font-bold">${{t.base}}/${{t.target}}</td>
                                <td class="p-4 text-right font-mono tracking-tighter text-white font-bold">
                                    Rp ${{t.converted_last.idr ? t.converted_last.idr.toLocaleString('id-ID') : 'N/A'}}
                                </td>
                            </tr>
                        `;
                    }});
                }} catch(e) {{ 
                    tbody.innerHTML = '<tr><td colspan="3" class="p-10 text-center text-red-500 text-[10px]">Gagal memuat daftar bursa.</td></tr>';
                }}
            }}

            function closeModal() {{
                document.getElementById('coin-modal').classList.add('hidden');
                document.body.style.overflow = 'auto';
            }}

            fetchCrypto();
            setInterval(fetchCrypto, 60000);
        </script>
    </body>
    </html>
    """

    # --- BAGIAN GROQ AI (NEWS FLASH) ---
    news_prompt = """
    Bertindaklah sebagai jurnalis senior crypto. Buatlah 3 berita crypto viral hari ini.
    Bahasa Indonesia. HANYA OUTPUT 3 ELEMEN DIV SAJA dengan class:
    'bg-[#171924] p-6 rounded-2xl border border-gray-800 news-card shadow-lg'
    
    Format dalam div:
    1. <span class='text-yellow-500 font-bold uppercase text-[9px]'>Saka Update</span>
    2. <h3 class='text-white font-bold text-sm my-3 leading-snug'>[Judul]</h3>
    3. <p class='text-gray-500 text-[11px] leading-relaxed'>[Ringkasan 2 kalimat]</p>
    
    Jangan berikan pembukaan/penutup markdown. Langsung kode HTML.
    """

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a clean HTML output engine."}, {"role": "user", "content": news_prompt}],
            model="llama-3.1-8b-instant",
        )
        ai_news = completion.choices[0].message.content.strip()
        
        # Bersihkan dari kode markdown jika AI bandel
        if "```" in ai_news:
            ai_news = ai_news.split("```")[1].replace("html", "").strip()

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(header_html.replace("{{{{AI_NEWS}}}}", ai_news) + footer_html)
            
        print("Success: SakaMarketCap Pro Fully Built!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_web_pro_final()
