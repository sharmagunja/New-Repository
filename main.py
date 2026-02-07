import google.generativeai as genai
from fastapi import FastAPI
from mangum import Mangum
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

app = FastAPI()

# यहाँ अपनी API Key डालें
genai.configure(api_key="AIzaSyDWDbbKhME7QZlXh3iWFUnM7WlX8VKlOwM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def read_root():
    return {"status": "Astrology Plugin is Live!"}

@app.get("/kundli")
def get_kundli(date: str, time: str, lat: float, lon: float):
    try:
        # 1. सटीक गणना (Exact Calculation)
        # date format: YYYY/MM/DD, time format: HH:MM
        dt = Datetime(date, time, '+05:30')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)
        
        asc = chart.get(const.ASC)
        moon = chart.get(const.MOON)
        sun = chart.get(const.SUN)
        nakshatra = moon.getNakshatra()

        # 2. Gemini के लिए डेटा तैयार करना
        astro_data = f"Lagn: {asc.sign}, MoonSign: {moon.sign}, SunSign: {sun.sign}, Nakshatra: {nakshatra}"

        # 3. Gemini से भविष्यवाणी लिखवाना
        prompt = f"""
        तुम एक प्रोफेशनल भारतीय ज्योतिषी हो। इस सटीक डेटा के आधार पर कुंडली विश्लेषण हिंदी में लिखो:
        डेटा: {astro_data}
        निर्देश: 1. स्वभाव, 2. करियर, 3. उपाय। 
        भाषा सरल और प्रभावशाली होनी चाहिए। टेबल का उपयोग करें।
        """
        
        response = model.generate_content(prompt)
        return {"result": response.text}

    except Exception as e:
        return {"error": str(e)}

handler = Mangum(app)
