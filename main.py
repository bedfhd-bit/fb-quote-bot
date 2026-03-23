import os
import requests
import random
import json

# الإعدادات (تُجلب من Secrets)
FB_PAGE_ID = os.environ.get('971729702699404')
FB_TOKEN = os.environ.get('EAAUHjZALse8cBRCAwSuFjyZB18OZCUNulLsHbwKJ9dKnImDzfOLBlwh43Rc84ZCYRI4YZBl5lj6VEoVkmFu0gJbmugx6ZCYQfqM225HsrdcUMKo81eRPmsp3yVliY3M19mqlSdSj07IompqQfSSiShA9ueGZC9c2dSOHI9rJGKKLhIfkACjyymAbgQjKZBGxDmtjGV32')

def fetch_psychology_quote():
    sources = [
        "https://zenquotes.io/api/random",
        "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en",
        "https://type.fit/api/quotes"
    ]
    
    # الكلمات المفتاحية لعلم النفس التي كانت في سكريبتك
    psych_keywords = ["mind", "mental", "emotion", "anxiety", "behavior", "thought", "psychology", "self", "habit", "success", "happiness"]
    
    try:
        for _ in range(10): # محاولات للفلترة
            source_idx = random.randint(0, 2)
            res = requests.get(sources[source_idx], timeout=10)
            quote = ""
            if source_idx == 0: quote = res.json()[0]['q']
            elif source_idx == 1: quote = res.json()['quoteText']
            else: quote = random.choice(res.json())['text']
            
            if any(word in quote.lower() for word in psych_keywords):
                return quote
        return "Your mind is your greatest tool; use it wisely."
    except:
        return None

def translate_to_ar(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ar&dt=t&q={text}"
        res = requests.get(url)
        return res.json()[0][0][0]
    except:
        return text

def post_to_facebook(message):
    url = f"https://graph.facebook.com/v24.0/{FB_PAGE_ID}/feed"
    payload = {'message': message, 'access_token': FB_TOKEN}
    res = requests.post(url, data=payload)
    return res.status_code

if __name__ == "__main__":
    quote_en = fetch_psychology_quote()
    if quote_en:
        quote_ar = translate_to_ar(quote_en)
        full_message = f"🧠 {quote_ar}\n\n#علم_النفس #تطوير_ذات"
        status = post_to_facebook(full_message)
        print(f"Status: {status} | Message: {quote_ar}")
