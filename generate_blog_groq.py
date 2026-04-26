import os
import datetime
from groq import Groq

# Ambil API KEY dari GitHub Secrets
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate_web_complete():
    # 1. Bagian Atas: Header, CSS, dan Navigasi
    header_html = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SakaMarketCap | Crypto Real-Time & AI News</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .crypto-row:hover { background-color: rgba(255, 255, 255, 0.05); transition: 0.2s; }
            canvas { max-width: 100px !important; max-height: 35px !important; }
            .news-card:hover { border-color: #eab308; transform: translateY(-3px); transition: 0.3s; }
            body::-webkit-scrollbar { width: 6px; }
            body::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }
        </style>
    </head>
    <body class="bg-[#0b0e11] text-white font-sans">
        <div id="coin-modal" class="fixed inset-0 z-[100] hidden bg-black/95 backdrop-blur-md overflow-y-auto">
            <div class="max-w-4xl mx-auto min-h-screen p-6 md:p-12">
                <button onclick="closeModal()" class="mb-8 text-gray-400 hover:text-white flex items-center gap-2 transition">
                    <i class="fas fa-arrow-left"></i> Kembali ke Dashboard
                </button>
                <div id="modal-content"></div>
            </div>
        </div>

        <nav class="sticky top-0 z-50 bg-[#0b0e11]/90 backdrop-blur-md border-b border-gray-800 p-4">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <div class="bg-yellow-500 p-2 rounded-lg text-black font-bold">S</div>
                    <span class="text-xl font-bold tracking-tighter">Saka<span class="text-yellow-500">MarketCap</span></span>
                </div>
                <div class="flex gap-4 items-center">
                    <a href="https://sakawebsite.github.io/" class="text-xs hover:text-yellow-500 hidden sm:block">Portfolio</a>
                    <a href="https://wa.me/628XXXXXXXXXX" class="bg-yellow-600 hover:bg-yellow-700 px-4 py-2 rounded-full text-[10px] font-bold uppercase transition">Konsultasi Bot</a>
                </div>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto p-4 md:p-6">
            <section class="mb-10 flex flex-col md:flex-row md:justify-between md:items-end gap-4">
                <div>
                    <h1 class="text-3xl font-bold">Pasar Aset Kripto</h1>
                    <p class="text-gray-500 text-sm italic">Data Real-time: IDR (Rupiah Indonesia)</p>
                </div>
                <div class="bg-gray-800/50 p-3 rounded-xl border border-gray-700 text-xs text-gray-400">
                    <i class="fas fa-info-circle mr-2"></i> Klik pada baris koin untuk melihat detail mendalam.
                </div>
            </section>
            
            <div class="overflow-x-auto bg-[#171924] rounded-2xl border border-gray-800 shadow-2xl mb-12">
                <table class="w-full text-left">
                    <thead class="border-b border-gray-800 text-gray-500 text-[10px] uppercase tracking-widest">
                        <tr>
                            <th class="p-5">Koin</th>
                            <th class="p-5 text-right">Harga</th>
                            <th class="p-5 text-right">24j %</th>
                            <th class="p-5 text-center">Trend 7D</th>
                        </tr>
                    </thead>
                    <tbody id="crypto-table-body" class="text-sm">
                        </tbody>
                </table>
            </div>

            <section class="mb-12">
                <div class="flex items-center gap-3 mb-8">
                    <div class="h-2 w-2 bg-red-500 rounded-full animate-ping"></div>
                    <h2 class="text-xl font-bold tracking-tight uppercase">News Flash <span class="text-gray-600 text-xs ml-2 font-normal">By Saka AI</span></h2>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {{{{AI_NEWS}}}}
                </div>
            </section>
        </main>
    """

    # 2. Bagian Bawah: Footer & Logika JavaScript
    footer_html = f"""
        <footer class="mt-20 p-12 border-t border-gray-800 text-center text-gray-600 text-[10px]">
            <p class="mb-2 font-bold uppercase tracking-widest">Saka Digital Systems</p>
            <p>Terakhir diperbarui: {datetime.datetime.now().strftime('%d %b %Y, %H:%M')} WIB</p>
            <p class="mt-4 italic">Source: CoinGecko API & Groq Llama 3.1 Intelligence</p>
        </footer>

        <script>
            let cryptoData = [];

            async function fetchCrypto() {{
                try {{
                    const res = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=idr&order=market_cap_desc&per_page=10&page=1&sparkline=true&price_change_percentage=24h');
                    cryptoData = await res.json();
                    renderTable();
                }} catch(e) {{ console.log("Fetch Error:", e); }}
            }}

            function renderTable() {{
                const tbody = document.getElementById('crypto-table-body');
                tbody.innerHTML = '';

                cryptoData.forEach(coin => {{
                    const isUp = coin.price_change_percentage_24h > 0;
                    const color = isUp ? '#22c55e' : '#ef4444';
                    
                    tbody.innerHTML += `
                        <tr onclick="openDetail('${{coin.id}}')" class="border-b border-gray-800/40 crypto-row cursor-pointer transition">
                            <td class="p-5 flex items-center gap-4">
                                <img src="${{coin.image}}" class="w-6 h-6 rounded-full shadow-lg">
                                <div>
                                    <div class="font-bold text-white uppercase">${{coin.symbol}}</div>
                                    <div class="text-[10px] text-gray-500">${{coin.name}}</div>
                                </div>
                            </td>
                            <td class="p-5 text-right font-mono text-xs font-bold tracking-tighter">
                                Rp ${{coin.current_price.toLocaleString('id-ID')}}
                            </td>
                            <td class="p-5 text-right ${{isUp ? 'text-green-500' : 'text-red-500'}} text-xs font-bold">
                                ${{isUp ? '▲' : '▼'}} ${{Math.abs(coin.price_change_percentage_24h).toFixed(2)}}%
                            </td>
                            <td class="p-5"><canvas id="c-${{coin.id}}" width="100" height="35"></canvas></td>
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
                    }}, 150);
                }});
            }}

            function openDetail(id) {{
                const coin = cryptoData.find(c => c.id === id);
                const modal = document.getElementById('coin-modal');
                const content = document.getElementById('modal-content');
                modal.classList.remove('hidden');
                document.body.style.overflow = 'hidden';

                content.innerHTML = `
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
                        <div class="space-y-8">
                            <div class="flex items-center gap-6">
                                <img src="${{coin.image}}" class="w-20 h-20 shadow-2xl rounded-full border-4 border-gray-800">
                                <div>
                                    <h2 class="text-5xl font-black tracking-tighter">${{coin.name}}</h2>
                                    <span class="bg-gray-800 px-3 py-1 rounded text-xs text-yellow-500 uppercase tracking-widest">Rank #${{coin.market_cap_rank}}</span>
                                </div>
                            </div>
                            <div>
                                <p class="text-gray-500 text-sm uppercase font-bold tracking-widest mb-1">Current Price</p>
                                <div class="text-6xl font-black font-mono tracking-tighter">Rp ${{coin.current_price.toLocaleString('id-ID')}}</div>
                                <div class="text-xl ${{coin.price_change_percentage_24h > 0 ? 'text-green-500' : 'text-red-500'}} mt-2 font-bold">
                                    ${{coin.price_change_percentage_24h.toFixed(2)}}% (24j)
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-6 pt-8 border-t border-gray-800">
                                <div><p class="text-gray-500 text-[10px] uppercase">Market Cap</p><p class="text-sm font-bold tracking-tight">Rp ${{coin.market_cap.toLocaleString('id-ID')}}</p></div>
                                <div><p class="text-gray-500 text-[10px] uppercase">24h Volume</p><p class="text-sm font-bold tracking-tight">Rp ${{coin.total_volume.toLocaleString('id-ID')}}</p></div>
                                <div><p class="text-gray-500 text-[10px] uppercase">All-Time High</p><p class="text-sm font-bold text-green-500">Rp ${{coin.ath.toLocaleString('id-ID')}}</p></div>
                                <div><p class="text-gray-500 text-[10px] uppercase">Circulating Supply</p><p class="text-sm font-bold text-blue-400">${{coin.circulating_supply.toLocaleString()}} ${{coin.symbol.toUpperCase()}}</p></div>
                            </div>
                        </div>
                        <div class="bg-[#171924] p-8 rounded-3xl border border-gray-800 shadow-2xl self-start">
                            <h4 class="text-yellow-500 font-black uppercase tracking-widest text-xs mb-4">Saka AI Market Intelligence</h4>
                            <p class="text-gray-400 text-sm leading-relaxed mb-8 italic">
                                "Sistem memantau pergerakan ${{coin.name}}. Saat ini, indikator menunjukkan tingkat volatilitas yang signifikan. Volume perdagangan terakhir mencapai Rp ${{coin.total_volume.toLocaleString('id-ID')}}. Harap waspada pada area support psikologis."
                            </p>
                            <a href="https://wa.me/628XXXXXXXXXX?text=Halo%20Saka,%20saya%20ingin%20konsultasi%20mengenai%20${{coin.name}}" class="block w-full bg-green-600 text-center py-4 rounded-2xl font-black uppercase text-xs tracking-widest hover:bg-green-700 transition shadow-lg">
                                <i class="fab fa-whatsapp mr-2"></i> Konsultasi ${{coin.symbol.toUpperCase()}}
                            </a>
                        </div>
                    </div>
                `;
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

    # 3. Prompt Berita untuk Groq AI
    news_prompt = """
    Bertindaklah sebagai jurnalis senior crypto. Buatlah 3 berita crypto paling viral hari ini dalam Bahasa Indonesia.
    
    WAJIB OUTPUT 3 DIV SAJA dengan format ini:
    <div class='bg-[#171924] p-6 rounded-2xl border border-gray-800 news-card shadow-xl'>
        <span class='text-[9px] text-yellow-500 font-bold uppercase tracking-widest'>Update Terkini</span>
        <h3 class='font-bold text-sm my-3 leading-snug'>[Judul Berita Singkat & Padat]</h3>
        <p class='text-[11px] text-gray-500 leading-relaxed'>[Ringkasan 2 kalimat singkat]</p>
    </div>
    
    Jangan berikan kata pembuka/penutup. Langsung kode HTML-nya.
    """

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You output only clean HTML code for 3 divs."},
                      {"role": "user", "content": news_prompt}],
            model="llama-3.1-8b-instant",
        )
        ai_news = completion.choices[0].message.content.strip()
        if "```" in ai_news:
            ai_news = ai_news.split("```")[1].replace("html", "").strip()

        # Tulis ke index.html
        final_html = header_html.replace("{{{{AI_NEWS}}}}", ai_news) + footer_html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print("SakaMarketCap successfully updated with full features!")
    except Exception as e:
        print(f"Error during update: {e}")

if __name__ == "__main__":
    generate_web_complete()
