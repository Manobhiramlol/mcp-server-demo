import streamlit as st
import openai
import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Weather API configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def get_weather_data(city):
    """Get current weather data for a city"""
    url = f"{BASE_URL}weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_weather_forecast(city):
    """Get weather forecast for a city"""
    url = f"{BASE_URL}forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def analyze_weather_data(weather_data):
    """Analyze weather data using GPT"""
    prompt = f"""
    Analyze this weather data and provide a detailed weather prediction:
    Temperature: {weather_data['main']['temp']}°C
    Humidity: {weather_data['main']['humidity']}%
    Wind Speed: {weather_data['wind']['speed']} m/s
    Description: {weather_data['weather'][0]['description']}
    
    Provide:
    1. Current weather conditions
    2. Potential weather changes in the next few hours
    3. Recommendations for outdoor activities
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a weather expert who provides detailed weather analysis and predictions."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("Weather Prediction App")
    
    # City input
    city = st.text_input("Enter city name:", "Bangalore")
    
    if st.button("Get Weather Prediction"):
        try:
            # Get current weather
            weather_data = get_weather_data(city)
            
            if weather_data.get('cod') != 200:
                st.error(f"Error: {weather_data.get('message', 'City not found')}")
                return
            
            # Get weather forecast
            forecast_data = get_weather_forecast(city)
            
            # Create DataFrame for forecast
            forecast_list = forecast_data['list'][:5]  # Show next 5 hours
            forecast_df = pd.DataFrame([
                {
                    'Time': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
                    'Temperature': f"{item['main']['temp']}°C",
                    'Weather': item['weather'][0]['description']
                }
                for item in forecast_list
            ])
            
            # Display current weather
            st.subheader("Current Weather")
            st.write(f"Temperature: {weather_data['main']['temp']}°C")
            st.write(f"Humidity: {weather_data['main']['humidity']}%")
            st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
            st.write(f"Description: {weather_data['weather'][0]['description']}")
            
            # Display forecast
            st.subheader("Weather Forecast")
            st.table(forecast_df)
            
            # Get AI analysis
            st.subheader("Weather Analysis")
            analysis = analyze_weather_data(weather_data)
            st.write(analysis)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()