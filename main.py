import google.generativeai as genai
from fastapi import FastAPI
from mangum import Mangum
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
import os

app = FastAPI()

# अपनी API Key डालें
genai.configure(api_key="AIzaSyDWDbbKhME7QZlXh3iWFUnM7WlX8VKlOwM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def read_root():
    return {"status": "Astrology Plugin is Live!"}

@app.get("/kundli")
def get_kundli(date: str, time: str, lat: float, lon: float):
    try:
        # सटीक गणना (flatlib)
        dt = Datetime(date, time, '+05:30')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)
        
        asc = chart.get(const.ASC)
        moon = chart.get(const.MOON)
        sun = chart.get(const.SUN)
        nakshatra = moon.getNakshatra()

        astro_data = f"Lagn: {asc.sign}, MoonSign: {moon.sign}, SunSign: {sun.sign}, Nakshatra: {nakshatra}"

        prompt = f"तुम एक ज्योतिषी हो। डेटा: {astro_data} के आधार पर हिंदी में स्वभाव और उपाय लिखें।"
        response = model.generate_content(prompt)
        
        return {"result": response.text}
    except Exception as e:
        return {"error": str(e)}

# Vercel के लिए यह लाइन सबसे ज़रूरी है
handler = Mangum(app)
