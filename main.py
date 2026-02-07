import google.generativeai as genai
from fastapi import FastAPI
from mangum import Mangum
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
import os

app = FastAPI()

# API Key को सुरक्षित रूप से पढ़ना
# अगर आप सीधे डाल रहे हैं तो नई Key यहाँ लिखें
api_key = os.getenv("AIzaSyDWDbbKhME7QZlXh3iWFUnM7WlX8VKlOwM", "AIzaSyDWDbbKhME7QZlXh3iWFUnM7WlX8VKlOwM") 
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def read_root():
    return {"status": "Astrology Plugin is Live!"}

@app.get("/kundli")
def get_kundli(date: str, time: str, lat: float, lon: float):
    try:
        # तारीख का फॉर्मेट सही करना (YYYY/MM/DD को YYYY/MM/DD में ही रहने दें)
        dt = Datetime(date, time, '+05:30')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)
        
        asc = chart.get(const.ASC)
        moon = chart.get(const.MOON)
        sun = chart.get(const.SUN)
        
        # Nakshatra निकालने का सही तरीका flatlib में
        nakshatra = moon.getNakshatra()

        astro_data = f"Lagn: {asc.sign}, MoonSign: {moon.sign}, SunSign: {sun.sign}, Nakshatra: {nakshatra}"

        prompt = f"""
        तुम एक प्रोफेशनल भारतीय ज्योतिषी हो। इस डेटा के आधार पर कुंडली विश्लेषण हिंदी में लिखो:
        डेटा: {astro_data}
        निर्देश: 1. स्वभाव, 2. करियर, 3. उपाय। 
        भाषा सरल हो और उत्तर Markdown टेबल और बुलेट्स में हो।
        """
        
        response = model.generate_content(prompt)
        return {"result": response.text}

    except Exception as e:
        # एरर को विस्तार से देखना
        return {"error": str(e)}

# Vercel के लिए handler
handler = Mangum(app)
