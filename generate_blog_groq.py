import os
import datetime
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate_web_with_charts():
    # Bagian Header dengan Library Chart.js
    header_html = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saka Crypto Monitor - Pro Charts</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            .crypto-row:hover { background-color: rgba(255, 255, 255, 0.03); }
            canvas { max-width: 120px !important; max-height: 40px !important; }
        </style>
    </head>
    <body class="bg-[#0b0e11] text-white font-sans">
        <nav class="sticky top-0 z-50 bg-[#0b0e11]/90 backdrop-blur-md border-b border-gray-800 p-4">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <div class="bg-yellow-500 p-2 rounded-lg text-black font-bold">S</div>
                    <span class="text-xl font-bold">Saka<span class="text-yellow-500">MarketCap</span></span>
                </div>
                <div class="flex gap-4 text-sm font-medium">
                    <a href="https://sakawebsite.github.io/" class="hover:text-yellow-500 hidden md:block">Portfolio</a>
                    <a href="https://wa.me/628XXXXXXXXXX" class="bg-yellow-600 px-3 py-1 rounded text-white">Pesan Bot</a>
                </div>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto p-4">
            <header class="my-8">
                <h1 class="text-2xl font-bold">Market Update Pro</h1>
                <p class="text-gray-400 text-sm">Real-time data dengan grafik tren 7 hari terakhir.</p>
            </header>

            <div class="overflow-x-auto bg-[#171924] rounded-xl border border-gray-800">
                <table class="w-full text-left">
                    <thead class="border-b border-gray-800 text-gray-400 text-xs uppercase">
                        <tr>
                            <th class="p-4">Nama</th>
                            <th class="p-4 text-right">Harga (IDR)</th>
                            <th class="p-4 text-right">24h %</th>
                            <th class="p-4 text-center">Last 7 Days</th>
                        </tr>
                    </thead>
                    <tbody id="crypto-table-body">
                        <tr><td colspan="4" class="p-10 text-center text-gray-500">Memuat data pasar...</td></tr>
                    </tbody>
                </table>
            </div>
    """

    footer_html = f"""
            <section class="mt-8 bg-[#171924] p-6 rounded-xl border border-gray-800">
                <h3 class="text-yellow-500 font-bold mb-2">💡 AI Market Insight</h3>
                <div class="text-gray-300 text-sm leading-relaxed">
                    {{{{AI_CONTENT}}}}
                </div>
            </section>
        </main>

        <script>
            async function fetchCryptoData() {{
                try {{
                    // Mengambil data dengan 'sparkline=true' untuk mendapatkan data grafik
                    const response = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=idr&order=market_cap_desc&per_page=10&page=1&sparkline=true&price_change_percentage=24h');
                    const data = await response.json();
                    const tableBody = document.getElementById('crypto-table-body');
                    tableBody.innerHTML = '';

                    data.forEach((coin, index) => {{
                        const isUp = coin.price_change_percentage_24h > 0;
                        const color = isUp ? '#22c55e' : '#ef4444';
                        
                        const row = `
                            <tr class="border-b border-gray-800 crypto-row transition">
                                <td class="p-4 flex items-center gap-3">
                                    <img src="${{coin.image}}" class="w-6 h-6">
                                    <div>
                                        <div class="font-bold text-sm">${{coin.name}}</div>
                                        <div class="text-xs text-gray-500 uppercase">${{coin.symbol}}</div>
                                    </div>
                                </td>
                                <td class="p-4 text-right font-mono text-sm">
                                    ${{coin.current_price.toLocaleString('id-ID')}}
                                </td>
                                <td class="p-4 text-right text-sm ${{isUp ? 'text-green-500' : 'text-red-400'}}">
                                    ${{isUp ? '▲' : '▼'}} ${{Math.abs(coin.price_change_percentage_24h).toFixed(2)}}%
                                </td>
                                <td class="p-4">
                                    <canvas id="chart-${{coin.id}}" width="120" height="40"></canvas>
                                </td>
                            </tr>
                        `;
                        tableBody.innerHTML += row;

                        // Render grafik setelah baris ditambahkan
                        setTimeout(() => {{
                            const ctx = document.getElementById(`chart-${{coin.id}}`).getContext('2d');
                            new Chart(ctx, {{
                                type: 'line',
                                data: {{
                                    labels: coin.sparkline_in_7d.price,
                                    datasets: [{{
                                        data: coin.sparkline_in_7d.price,
                                        borderColor: color,
                                        borderWidth: 2,
                                        pointRadius: 0,
                                        fill: false,
                                        tension: 0.4
                                    }}]
                                }},
                                options: {{
                                    responsive: false,
                                    plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }},
                                    scales: {{ x: {{ display: false }}, y: {{ display: false }} }}
                                }}
                            }});
                        }}, 100);
                    }});
                }} catch (e) {{ console.error(e); }}
            }}
            fetchCryptoData();
        </script>
    </body>
    </html>
    """

    # Analisis AI yang lebih tajam
    prompt = "Buat analisa singkat crypto hari ini dalam 3 poin bullet. Gunakan Bahasa Indonesia yang santai tapi profesional. Jangan pakai penjelasan pembuka."

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a crypto trader. Output only HTML list items <li>."},
                      {"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        ai_insight = f"<ul class='list-disc ml-5 space-y-2'>{completion.choices[0].message.content.strip()}</ul>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(header_html + footer_html.replace("{{AI_CONTENT}}", ai_insight))
        print("Success: Web Pro Charts berhasil di-update!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_web_with_charts()
