import google.generativeai as genai
from fastapi import FastAPI
from mangum import Mangum
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
import os

app = FastAPI()

# API Key
genai.configure(api_key="AIzaSyDWDbbKhME7QZlXh3iWFUnM7WlX8VKlOwM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def home():
    return {"status": "Astrology Plugin is Live!"}

@app.get("/kundli")
def get_kundli(date: str, time: str, lat: float, lon: float):
    try:
        # flatlib गणना (100% सटीक)
        # date format: 2024/05/20, time: 10:30
        dt = Datetime(date, time, '+05:30')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)
        
        # ग्रहों की स्थिति निकालना
        asc = chart.get(const.ASC)
        moon = chart.get(const.MOON)
        sun = chart.get(const.SUN)
        nakshatra = moon.getNakshatra()

        # यह डेटा 100% सही है, अब इसे Gemini को देंगे
        astro_data = (f"Lagn: {asc.sign} ({asc.lon}), "
                      f"MoonSign: {moon.sign} ({moon.lon}), "
                      f"SunSign: {sun.sign}, "
                      f"Nakshatra: {nakshatra}")

        prompt = f"तुम एक ज्योतिष विशेषज्ञ हो। इस सटीक डेटा {astro_data} के आधार पर जातक का स्वभाव और भविष्यफल हिंदी में लिखें। गणना मैं कर चुका हूँ, तुम बस फल बताओ।"
        
        response = model.generate_content(prompt)
        return {"result": response.text, "raw_data": astro_data}

    except Exception as e:
        return {"error": f"Calculation Error: {str(e)}. Please check date format YYYY/MM/DD"}

handler = Mangum(app)
