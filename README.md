# Anonim Chat - K va D

Oddiy real-time chat - faqat 2 foydalanuvchi (K va D) uchun.

## 🎯 Xususiyatlar

✅ **2 foydalanuvchi** - K va D
✅ **Parol bilan kirish** - K parol: `K`, D parol: `D`
✅ **Real-time xabarlar** - WebSocket orqali
✅ **O'qilganlik statusi** - ✓ (yuborildi), ✓✓ (o'qildi)
✅ **Vaqt ko'rsatkichi** - Har bir xabarda yuborilgan vaqt
✅ **Qulflash** - Tepada 🔒 tugmasi
✅ **Auto-logout** - 5 daqiqa faolsizlik
✅ **Session** - Yangilashda parol so'ramaydi
✅ **Jazzmin Admin** - Chiroyli admin panel

## 🚀 Ishga tushirish

### 1. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. Ma'lumotlar bazasini yaratish
```bash
python manage.py makemigrations chat
python manage.py migrate
```

**MUHIM:** Agar avval ishlatgan bo'lsangiz, yangi fieldlar qo'shilgan:
```bash
rm db.sqlite3  # Eski bazani o'chirish
python manage.py makemigrations chat
python manage.py migrate
```

### 5. Superuser yaratish (admin panel uchun)
```bash
python manage.py createsuperuser
```

Username, email va parol kiriting.

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

### 7. Admin panelga kirish
http://127.0.0.1:8000/admin/

Superuser ma'lumotlaringiz bilan kiring.

### 4. Brauzerda ochish
http://127.0.0.1:8000/

## 📱 Foydalanish

### K sifatida kirish:
1. K tugmasini bosing
2. Parol: `Kamola`
3. "Kirish" tugmasini bosing

### D sifatida kirish:
1. Yangi brauzer oynasi oching (yoki boshqa kompyuter)
2. D tugmasini bosing
3. Parol: `Doniyor`
4. "Kirish" tugmasini bosing

### Xabar yuborish:
- Pastdagi inputga xabar yozing
- Enter bosing yoki "Yuborish" tugmasini bosing
- Ikkinchi foydalanuvchida darhol paydo bo'ladi

### O'qilganlik:
- **✓ (bitta check)** - Xabar yuborildi
- **✓✓ (ikkita check, ko'k)** - Xabar o'qildi
- Boshqa foydalanuvchi chatga kirganda avtomatik o'qilgan bo'ladi

### Vaqt:
- Har bir xabarda yuborilgan vaqt ko'rsatiladi (masalan: 14:30)
- O'ng pastda ko'rinadi

### Qulflash:
- Tepada 🔒 tugmasini bosing
- Chatdan chiqadi, qayta kirish uchun parol kerak

### Auto-logout:
- 5 daqiqa faolsizlik - avtomatik chiqaradi
- Qayta kirish uchun parol so'raydi

## 🔐 Parollar

| Foydalanuvchi | Parol   |
|---------------|---------|
| K             | Kamola  |
| D             | Doniyor |

**O'zgartirish uchun:** `chat/views.py` faylidagi `PASSWORDS` ni tahrirlang.

## 📁 Loyiha tuzilishi

```
simple_chat/
├── config/              # Asosiy sozlamalar
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL routing
│   └── asgi.py         # WebSocket config
│
├── chat/               # Chat aplikatsiyasi
│   ├── models.py       # Message modeli
│   ├── views.py        # Login, Chat views
│   ├── consumers.py    # WebSocket consumer
│   ├── routing.py      # WebSocket routing
│   └── urls.py         # URL patterns
│
├── templates/          # HTML shablonlar
│   ├── login.html      # Login sahifasi
│   └── chat.html       # Chat sahifasi
│
└── manage.py          # Django manage
```

## ⚙️ Sozlamalar

### Session muddati (settings.py):
```python
SESSION_COOKIE_AGE = 300  # 5 daqiqa (sekundlarda)
```

### Parollarni o'zgartirish (chat/views.py):
```python
PASSWORDS = {
    'K': 'sizning_parolingiz',
    'D': 'boshqa_parol',
}
```

## 🐛 Muammolar

### Port band bo'lsa:
```bash
python manage.py runserver 8080
```

### WebSocket ishlamasa:
- settings.py da `CHANNEL_LAYERS` to'g'ri sozlanganini tekshiring
- Development uchun InMemoryChannelLayer yetarli

### Ma'lumotlar bazasi xatosi:
```bash
rm db.sqlite3
python manage.py makemigrations chat
python manage.py migrate
```

## 💡 Test qilish

1. **Birinchi brauzer:** K sifatida kiring
2. **Ikkinchi brauzer/tab:** D sifatida kiring
3. K dan xabar yuboring → D da paydo bo'ladi
4. D dan javob yuboring → K da paydo bo'ladi

## 🔒 Xavfsizlik

⚠️ **DIQQAT:** Bu oddiy demo loyiha!

Production uchun:
- Parollarni shifrlang (hash)
- SECRET_KEY ni o'zgartiring
- DEBUG = False qiling
- HTTPS ishlatish (WSS uchun)
- Xavfsiz parollar ishlatish

## 📝 Eslatma

- Session 5 daqiqa amal qiladi
- Faolsizlik 5 daqiqa - avtomatik logout
- Xabarlar ma'lumotlar bazasida saqlanadi
- Sahifani yangilash - parol so'ramaydi (session bor)
- 🔒 tugmasini bosish - chatdan chiqadi

---

**Tayyor! Chat ishlatishga tayyor! 🎉**
