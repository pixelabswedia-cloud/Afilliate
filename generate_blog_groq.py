import os
import datetime
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate_web_ultra():
    header_html = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SakaMarketCap | Pro Crypto Monitor</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .crypto-row:hover { background-color: rgba(255, 255, 255, 0.05); cursor: pointer; }
            .news-card:hover { border-color: #eab308; transform: translateY(-3px); transition: 0.3s; }
            body::-webkit-scrollbar { width: 5px; }
            body::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }
            .market-table-row:nth-child(even) { background-color: rgba(255,255,255,0.02); }
        </style>
    </head>
    <body class="bg-[#0b0e11] text-white font-sans">
        
        <div id="coin-modal" class="fixed inset-0 z-[100] hidden bg-[#0b0e11] overflow-y-auto">
            <div class="max-w-5xl mx-auto p-4 md:p-10">
                <nav class="flex justify-between items-center mb-8">
                    <button onclick="closeModal()" class="text-gray-400 hover:text-white flex items-center gap-2">
                        <i class="fas fa-chevron-left"></i> Markets
                    </button>
                    <div id="modal-header-price" class="text-right"></div>
                </nav>
                <div id="modal-content"></div>
            </div>
        </div>

        <nav class="sticky top-0 z-50 bg-[#0b0e11]/90 backdrop-blur-md border-b border-gray-800 p-4">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <div class="bg-yellow-500 p-1.5 rounded text-black font-bold text-sm">S</div>
                    <span class="text-lg font-bold tracking-tighter">Saka<span class="text-yellow-500 text-xs">MARKET</span></span>
                </div>
                <div class="flex gap-4">
                    <a href="https://wa.me/628XXXXXXXXXX" class="text-xs font-bold bg-gray-800 px-4 py-2 rounded-lg border border-gray-700">Order Bot</a>
                </div>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto p-4 md:p-6">
            <section class="mb-8">
                <h1 class="text-2xl font-bold">Harga Aset Kripto</h1>
                <p class="text-gray-500 text-xs mt-1 italic">Update Otomatis setiap 60 detik</p>
            </section>
            
            <div class="overflow-x-auto bg-[#171924] rounded-xl border border-gray-800 mb-12">
                <table class="w-full text-left text-sm">
                    <thead class="text-gray-500 text-[10px] uppercase border-b border-gray-800 tracking-widest">
                        <tr>
                            <th class="p-4"># Name</th>
                            <th class="p-4 text-right">Price (IDR)</th>
                            <th class="p-4 text-right">24h %</th>
                            <th class="p-4 text-center">Trend 7D</th>
                        </tr>
                    </thead>
                    <tbody id="crypto-table-body"></tbody>
                </table>
            </div>

            <h2 class="text-lg font-bold mb-6 flex items-center gap-2">
                <span class="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span> News Flash AI
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20">
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

            async function fetchCrypto() {{
                try {{
                    const res = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=idr&order=market_cap_desc&per_page=10&page=1&sparkline=true&price_change_percentage=24h');
                    cryptoData = await res.json();
                    renderTable();
                }} catch(e) {{ console.log(e); }}
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
                                <span class="font-bold tracking-tight">${{coin.name}}</span>
                            </td>
                            <td class="p-4 text-right font-mono text-xs tracking-tighter">Rp ${{coin.current_price.toLocaleString('id-ID')}}</td>
                            <td class="p-4 text-right ${{isUp ? 'text-green-500' : 'text-red-500'}} text-[11px] font-bold">
                                ${{isUp ? '+' : ''}}${{coin.price_change_percentage_24h.toFixed(2)}}%
                            </td>
                            <td class="p-4"><canvas id="c-${{coin.id}}" width="100" height="35"></canvas></td>
                        </tr>
                    `;
                    renderSparkline(coin);
                }});
            }}

            function renderSparkline(coin) {{
                setTimeout(() => {{
                    const ctx = document.getElementById(`c-${{coin.id}}`).getContext('2d');
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
                }}, 100);
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
                            <h2 class="text-3xl font-bold">${{coin.name}} <span class="text-gray-500 text-lg uppercase">${{coin.symbol}}</span></h2>
                        </div>
                        <div class="flex items-center gap-4">
                            <span class="text-4xl font-bold font-mono">Rp ${{coin.current_price.toLocaleString('id-ID')}}</span>
                            <span class="bg-${{coin.price_change_percentage_24h > 0 ? 'green' : 'red'}}-600 px-2 py-1 rounded text-xs font-bold">
                                ${{coin.price_change_percentage_24h.toFixed(2)}}%
                            </span>
                        </div>
                    </div>

                    <div class="bg-[#171924] rounded-2xl border border-gray-800 overflow-hidden mb-10">
                        <div class="p-4 border-b border-gray-800 bg-gray-800/20 font-bold text-sm">
                            ${{coin.name}} Markets
                        </div>
                        <div class="overflow-x-auto text-[11px]">
                            <table class="w-full">
                                <thead class="text-gray-500 uppercase border-b border-gray-800">
                                    <tr>
                                        <th class="p-3 text-left"># Exchange</th>
                                        <th class="p-3">Pairs</th>
                                        <th class="p-3 text-right">Price</th>
                                    </tr>
                                </thead>
                                <tbody id="market-list-body">
                                    <tr><td colspan="3" class="p-10 text-center text-gray-600">Loading Market Data...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="bg-yellow-600/10 p-6 rounded-2xl border border-yellow-600/20">
                        <h4 class="text-yellow-500 font-bold mb-2">Saka AI Insights</h4>
                        <p class="text-xs text-gray-400 leading-relaxed italic">
                            Sistem Saka mendeteksi volume perdagangan ${{coin.name}} sebesar Rp ${{coin.total_volume.toLocaleString('id-ID')}} dalam 24 jam terakhir. 
                            Ini adalah bursa teraktif untuk saat ini.
                        </p>
                    </div>
                `;
                fetchTickers(id);
            }}

            async function fetchTickers(coinId) {{
                try {{
                    const res = await fetch(`https://api.coingecko.com/api/v3/coins/${{coinId}}/tickers?include_exchange_logo=true&depth=false`);
                    const data = await res.json();
                    const tbody = document.getElementById('market-list-body');
                    tbody.innerHTML = '';

                    data.tickers.slice(0, 10).forEach((t, i) => {{
                        tbody.innerHTML += `
                            <tr class="border-b border-gray-800/50 market-table-row">
                                <td class="p-3 flex items-center gap-3 font-bold">
                                    <span class="text-gray-600 w-3">${{i+1}}</span>
                                    <img src="${{t.market.logo}}" class="w-4 h-4 rounded-full bg-white p-0.5">
                                    ${{t.market.name}}
                                </td>
                                <td class="p-3 text-blue-400 text-center uppercase tracking-tighter">
                                    ${{t.base}}/${{t.target}} <i class="fas fa-external-link-alt text-[8px] ml-1"></i>
                                </td>
                                <td class="p-3 text-right font-mono tracking-tighter">
                                    Rp ${{t.converted_last.idr.toLocaleString('id-ID')}}
                                </td>
                            </tr>
                        `;
                    }});
                }} catch(e) {{ console.log(e); }}
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

    news_prompt = "Buat 3 berita singkat crypto viral hari ini. Bahasa Indonesia. Output HANYA 3 elemen <div> dengan class 'bg-[#171924] p-5 rounded-xl border border-gray-800 news-card'. Tanpa penjelasan."

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "HTML Output only."}, {"role": "user", "content": news_prompt}],
            model="llama-3.1-8b-instant",
        )
        ai_news = completion.choices[0].message.content.strip()
        if "
http://googleusercontent.com/immersive_entry_chip/0

### Apa yang ditambahkan di kode ini?
1.  **Market Table (Ala Screenshot):** Di dalam modal koin, sekarang ada tabel bursa (Exchange) dengan logo asli, pasangan aset (seperti BTC/USDT), dan harga di tiap bursa tersebut.
2.  **Ticker Integration:** Mengambil data langsung dari endpoint Tickers CoinGecko, sehingga daftar bursa yang muncul adalah yang paling aktif.
3.  **UI Detail yang Rapih:** Menggunakan font mono untuk harga agar sejajar dan mudah dibaca (persis gaya aplikasi finansial).
4.  **Exchange Icons:** Menambahkan logo kecil bursa di daftar market untuk memudahkan identifikasi.

Silakan ganti script lama kamu dengan ini, Saka. Sekarang tiap kali kamu klik koin di webmu, tampilannya akan sangat profesional seperti aplikasi aslinya!
