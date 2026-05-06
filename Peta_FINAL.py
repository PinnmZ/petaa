import folium
from folium.plugins import Fullscreen, MiniMap, MeasureControl, MousePosition
from folium import IFrame

# =========================
# PETA DASAR
# =========================
m = folium.Map(location=[0.35, 111.5], zoom_start=7, control_scale=True, tiles=None)

# =========================
# TILE
# =========================
folium.TileLayer("OpenStreetMap", name="OpenStreetMap (melihat detail nama jalan dan tempat)").add_to(m)

folium.TileLayer("CartoDB positron", name="Minimalis (melihat lebih jelas aliran sungai dan perbatasan)").add_to(m)

folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    name="Satelit (melihat kondisi hutan dan sungai secara nyata)",
    attr="© Esri"
).add_to(m)

# =========================
# FITUR WEBGIS
# =========================
Fullscreen().add_to(m)
MiniMap().add_to(m)
MeasureControl().add_to(m)
MousePosition().add_to(m)

# =========================
# HULU & MUARA
# =========================
layer_hulu = folium.FeatureGroup(name="Hulu & Muara")

# 🔵 DATA TITIK
data_hulu = [
    ("Hulu Kapuas", 0.616424, 113.792087, "Hutan tropis, curah hujan tinggi"),
    ("Muara Kapuas", 0.055618, 109.191055, "Wilayah pesisir, dipengaruhi pasang surut")
]

# 🔵 MARKER
for nama, lat, lon, info in data_hulu:
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(f"""
        <div style="width:220px; font-size:13px; line-height:1.4;">
        <b>{nama}</b>
        <hr style="margin:5px 0;">
        {info}<br>
        📊 Data: BMKG & BPS
        </div>
        """, max_width=250),
        tooltip=nama,
        icon=folium.Icon(color="blue")
    ).add_to(layer_hulu)

# 🔵 ALIRAN SUNGAI (SEKARANG MASUK LAYER)
flow = [
    [0.616424, 113.792087],
    [0.3, 112.5],
    [0.1, 111.0],
    [0.055618, 109.191055]
]

folium.PolyLine(
    flow,
    color="yellow",
    weight=5,
    dash_array="10,10"
).add_to(layer_hulu)

# 🔵 TAMBAHKAN KE MAP
layer_hulu.add_to(m)

# =========================
# SUNGAI BESAR
# =========================
layer_besar = folium.FeatureGroup(name="Sungai Besar")

folium.Marker(
    [0.3, 112.5],
    popup=folium.Popup("""
    <div style="width:220px; font-size:13px; line-height:1.4;">
    <b>Sungai Kapuas</b>
    <hr style="margin:5px 0;">
    📏 Panjang: 1.143 km<br>
    🌊 Debit: 5000–6000 m³/s<br>
    🌧 Curah hujan: Tinggi<br>
    📊 Kondisi: Rawan banjir musiman<br>
    🐟 Ikan: Arwana, patin, baung<br>
    📊 Data: BMKG & BPS
    </div>
    """, max_width=250),
    tooltip="Kapuas",
    icon=folium.Icon(color="green")
).add_to(layer_besar)

layer_besar.add_to(m)

# =========================
# ANAK SUNGAI
# =========================
layer_anak = folium.FeatureGroup(name="Anak Sungai")

anak = [
    ("Melawi", -0.329, 111.733, "471 km", "patin, baung"),
    ("Sekayam", 0.126, 110.610, "221 km", "lele"),
    ("Landak", -0.021, 109.350, "178 km", "gabus"),
    ("Kubu", -0.488, 109.376, "150 km", "udang"),
    ("Pawan", -1.3264924979543993, 110.46605968163382, "197 km", "ikan air tawar"),
    ("Sambas", 1.3645208467684382, 109.30968793264805, "233 km", "kepiting")
]

for nama, lat, lon, panjang, Ikan in anak:
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(f"""
        <div style="width:220px; font-size:13px; line-height:1.4;">
        <b>Sungai {nama}</b>
        <hr style="margin:5px 0;">
        📏 Panjang: {panjang}<br>
        🌧 Curah hujan: Tinggi<br>
        📊 Kondisi: Rawan banjir<br>
        🐟 Ikan: {Ikan}<br>
        📊 Data: BMKG & BPS
        </div>
        """, max_width=250),
        tooltip=nama,
        icon=folium.Icon(color="orange")
    ).add_to(layer_anak)

layer_anak.add_to(m)

# =========================
# POPUP GRAFIK (FIX)
# =========================
def popup_kota(nama, data):
    html = f"""
    <html>
    <head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
    <h4>{nama}</h4>
    <canvas id="chart" width="250" height="150"></canvas>
    <script>
    var ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {{
        type: 'line',
        data: {{
            labels: ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'],
            datasets: [{{ data: {data}, borderWidth: 2 }}]
        }},
        options: {{ responsive: false, plugins: {{ legend: {{ display: false }} }} }}
    }});
    </script>
    </body>
    </html>
    """
    return folium.Popup(IFrame(html, width=300, height=250))

# =========================
# KOTA
# =========================
layer_kota = folium.FeatureGroup(name="Kota (Curah Hujan)")

kota = [
    ("Pontianak", -0.02612510056551984, 109.34699526061569, [300,280,320,290,260,200,180,190,220,270,310,330]),
    ("Sintang", 0.06379206456542849, 111.48554055559367, [280,260,300,270,250,210,190,200,230,260,290,310]),
    ("Sanggau", 0.12026204881459146, 110.597426671826 , [290,270,310,280,260,220,200,210,240,270,300,320]),
    ("Putussibau", 0.852309058851196, 112.92538755551811, [320,300,340,310,290,250,230,240,270,300,330,350]),
    ("Mempawah", 0.3642598941145667, 108.95494584114053, [310,290,330,300,270,230,210,220,250,280,310,340])
]

for nama, lat, lon, data in kota:
    folium.Marker(
        [lat, lon],
        popup=popup_kota(nama, data),
        tooltip=nama,
        icon=folium.Icon(color="red", icon="cloud")
    ).add_to(layer_kota)

layer_kota.add_to(m)

# =========================
# LEGENDA
# =========================
legend = """
<div style="
position: fixed;
bottom: 50px;
left: 10px;
z-index:9999;
background: white;
padding: 12px;
border-radius: 10px;
box-shadow: 0 0 10px rgba(0,0,0,0.3);
font-size:14px;
">

<b>Legenda</b><br> 
🔵 Hulu/Muara<br> 
🟢 Sungai Besar<br> 
🟠 Anak Sungai<br> 
🔴 Kota (Grafik Hujan)<br> 
🟡 Garis kuning: Aliran Air
</div>
"""
m.get_root().html.add_child(folium.Element(legend))
# =========================
# CONTROL
# =========================
folium.LayerControl(collapsed=False).add_to(m)

# =========================
# SIMPAN
# =========================
m.save("peta_KTI_fix.html")

print("Peta final siap 🚀")