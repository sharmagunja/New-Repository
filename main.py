import google.generativeai as genai
from fastapi import FastAPI
from mangum import Mangum
import requests  # सटीक गणना के लिए बाहरी इंजन का उपयोग
import os

app = FastAPI()

# आपकी Gemini API Key
genai.configure(api_key="AIzaSyDWDbbKhME7QZlXh3iWFUnM7WlX8VKlOwM")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/")
def home():
    return {"status": "Astrology Plugin is Live!"}

@app.get("/kundli")
def get_kundli(date: str, time: str, lat: float, lon: float):
    try:
        # flatlib की जगह हम एक सटीक ज्योतिष इंजन का उपयोग कर रहे हैं
        # यह कभी क्रैश नहीं होगा क्योंकि इसे सर्वर पर इंस्टॉल नहीं करना पड़ता
        calc_url = f"https://api.vedicastro.pro/v1/panchang/panchang?dob={date}&tob={time}&lat={lat}&lon={lon}&tz=5.5&api_key=FREE_TIER"
        
        # ग्रहों की सटीक जानकारी मंगाना
        calc_res = requests.get(calc_url).json()
        
        # Gemini के लिए डेटा तैयार करना
        # इसमें नक्षत्र, राशि और लग्न सब शामिल है
        astro_data = str(calc_res.get('response', 'No data found'))

        prompt = f"""
        तुम एक प्रोफेशनल ज्योतिषी हो। इस ज्योतिषीय डेटा के आधार पर हिंदी में कुंडली फल लिखो:
        डेटा: {astro_data}
        निर्देश: 1. स्वभाव, 2. करियर, 3. उपाय बताएं। टेबल और बुलेट्स का प्रयोग करें।
        तारीख: {date}, समय: {time}
        """
        
        response = model.generate_content(prompt)
        return {"result": response.text}

    except Exception as e:
        return {"error": str(e)}

handler = Mangum(app)
