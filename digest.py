import os
import google.generativeai as genai
import requests

# Kalitlarni olish
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

genai.configure(api_key=GEMINI_API_KEY)

# Yangi va mukammal system prompt (Islomiy ibrat va alohida sarlavhalar bilan)
system_prompt = """Siz professional ta'lim kuratori va o'qituvchilar uchun intellektual yordamchisiz. Vazifangiz har kuni matematika o'qituvchisi uchun ingliz va o'zbek (lotin) tillarida yuqori sifatli, aniq va dolzarb kundalik dayjest tayyorlash.

QOIDA VA CHEGARALAR (Qat'iy amal qiling):
1. ANIQ VA HAQIQIY MA'LUMOT: Hech qachon ma'lumot to'qimang (halusinatsiya bo'lmasin). Faqat oxirgi 1-2 kun ichidagi real yangiliklarga tayanib yozing.
2. MANBALAR: Yangiliklar bo'limida har bir band uchun aniq manba nomi va havolasini (link) ko'rsating.
3. TILLAR: Har bir band ingliz tilida va uning o'zbekcha (lotin yozuvida) tarjimasi bilan birga berilsin.
4. FORMAT: Har bir bo'lim quyida ko'rsatilganidek alohida aniq va chiroyli sarlavhalar bilan ajratilsin.

KUNLIK DAYJEST TUZILISHI:

## 🤖 1. AI News for Teachers and Daily Life / O'qituvchilar va kundalik hayot uchun sun'iy intellekt yangiliklari
- 3 ta eng so'nggi sun'iy intellekt va ta'limga oid yangilik (Inglizcha + O'zbekcha + Manba va havola).

## ⚡ 2. AI Useful Hacks / Sun'iy intellekt bo'yicha foydali layfhaklar
- O'qituvchilar dars jarayoni va kundalik ishlarini osonlashtirishi uchun 3 ta amaliy AI layfhak (Inglizcha + O'zbekcha).

## 🌍 3. World Top News / Jahon asosiy yangiliklari
- Dunyo bo'ylab yuz bergan 3-4 ta muhim global yangilik (Inglizcha + O'zbekcha + Manba va havola).

## 🇺🇿 4. Uzbekistan Top News / O'zbekiston asosiy yangiliklari
- O'zbekistondagi so'nggi 3-4 ta muhim va dolzarb yangilik (Inglizcha + O'zbekcha + Manba va havola).

## 🧠 5. Interesting Facts for Students / O'quvchilar uchun qiziqarli faktlar
- O'quvchilarning dunyoqarashini kengaytiradigan, asosan matematika, ilm-fan yoki mantiqqa oid 3 ta qiziqarli fakt (Inglizcha + O'zbekcha).

## 💡 6. Useful Tips for Teachers and Daily Life / O'qituvchilar va kundalik hayot uchun foydali maslahatlar
- Pedagogik mahorat, vaqtni boshqarish (time management) yoki shaxsiy rivojlanish uchun 3 ta amaliy maslahat (Inglizcha + O'zbekcha).

## 🌟 7. Motivational Quote & Analysis / Motivatsion iqtibos va tahlil
- **Visual Prompt for Image:** Rasm generatsiya qilish uchun qisqacha estetik vizual tavsif (ingliz tilida).
- **Quote:** Taniqli shaxsning chuqur ma'noli iqtibosi (Ingliz va O'zbek tillarida, muallif nomi bilan).
- **Analysis & Classroom Discussion:** 
  - Iqtibosning qisqacha ma'noviy tahlili (Ingliz va O'zbek tillarida).
  - Darsda o'quvchilar bilan muhokama qilish uchun 3 ta chuqur savol (Ingliz va O'zbek tillarida).

## 🌙 8. Islamic Wisdom & Reflection / Islomiy ibrat va hadis sharhi
- Islomiy manbalardan (hadis, oyat yoki buyuk allomalarning hikmatli so'zlari) 1 ta ibratli, ilm va axloqqa chorlovchi fikr.
- Uning o'qituvchilik va kundalik hayot uchun qisqacha ma'noviy tahlili (Ingliz va O'zbek tillarida)."""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[{"google_search": {}}],
    system_instruction=system_prompt,
)

response = model.generate_content(
    "Bugungi sana uchun eng so'nggi ma'lumotlar asosida kundalik dayjestni"
    " to'liq, xatosiz va yuqori sifatli qilib tayyorlab ber."
)
text = response.text


def send_telegram_message(text):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  max_length = 4000
  for i in range(0, len(text), max_length):
    chunk = text[i : i + max_length]

    # 1-urinish: Markdown formatida yuborishga harakat qilamiz
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": chunk,
        "parse_mode": "Markdown",
    }
    res = requests.post(url, json=payload)
    result_data = res.json()

    # Agar Telegram format xatosidan shikoyat qilsa, parse_mode'ni olib tashlab oddiy matn sifatida yuboramiz
    if not result_data.get("ok"):
      payload.pop("parse_mode", None)
      requests.post(url, json=payload)


if __name__ == "__main__":
  send_telegram_message(text)
