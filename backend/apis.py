import requests
import wikipedia
import yfinance as yf
from duckduckgo_search import DDGS
from backend.command import speak


# 🌦️ WEATHER
def get_weather(city="Nagpur"):
    try:
        api_key = "YOUR_OPENWEATHER_API_KEY"   # 🔑 Get it free at https://openweathermap.org/api
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") != 200:
            result = f"Could not fetch weather for {city}."
        else:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            result = f"The weather in {city} is {desc} with {temp}°C."

        print("[Weather]:", result)
        speak(result)
        return result

    except Exception as e:
        print("[Weather ERROR]:", e)
        speak("Sorry, I couldn't fetch the weather.")
        return "Sorry, I couldn't fetch the weather."


# 📰 NEWS
def get_news(country="in"):
    try:
        api_key = "YOUR_NEWSAPI_KEY"   # 🔑 Get it free at https://newsapi.org
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
        res = requests.get(url).json()

        if res.get("status") != "ok":
            result = "Could not fetch news."
        else:
            headlines = [article["title"] for article in res["articles"][:5]]
            result = "Here are today's top headlines: " + "; ".join(headlines)

        print("[News]:", result)
        speak(result)
        return result

    except Exception as e:
        print("[News ERROR]:", e)
        speak("Sorry, I couldn't fetch the news.")
        return "Sorry, I couldn't fetch the news."


# 📚 WIKIPEDIA
def get_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        print("[Wikipedia]:", result)
        speak(result)
        return result
    except Exception as e:
        print("[Wiki ERROR]:", e)
        speak("Sorry, I couldn't fetch info from Wikipedia.")
        return "Sorry, I couldn't fetch info from Wikipedia."


# 🌍 DUCKDUCKGO SEARCH (LIVE INFORMATION)
def duckduck_search(query: str):
    """
    Search DuckDuckGo for real-time info.
    """
    try:
        results = list(DDGS().text(query, max_results=3))
        if not results:
            response = "I couldn’t find anything relevant."
        else:
            summary = "; ".join([r["title"] + " — " + r["body"] for r in results])
            response = "Here’s what I found: " + summary

        print("[DuckDuckGo Search]:", response)
        speak(response)
        return response

    except Exception as e:
        print("[DuckDuckGo ERROR]:", e)
        speak("Sorry, I couldn’t search the web right now.")
        return "Error"


# 🌐 GENERIC WEB SEARCH (optional alias to DuckDuckGo)
def web_search(query):
    try:
        return duckduck_search(query)
    except Exception as e:
        print("[Search ERROR]:", e)
        speak("Sorry, I couldn't perform the web search.")
        return "Sorry, I couldn't perform the web search."


# 💹 STOCK PRICES
def get_stock(symbol="AAPL"):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.history(period="1d")["Close"].iloc[-1]
        result = f"The current price of {symbol} is {price:.2f} USD."
        print("[Stock]:", result)
        speak(result)
        return result
    except Exception as e:
        print("[Stock ERROR]:", e)
        speak("Sorry, I couldn't fetch stock prices.")
        return "Sorry, I couldn't fetch stock prices."
