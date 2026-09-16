# Prompt Kaydı 01 — Senaryo Analizi ve Kök Neden Hipotezleri

## Amaç

S-A1 Alarm Fırtınası veri paketindeki alarmları, servis bağımlılıkları ve host
envanteriyle birlikte inceleyerek açıklanabilir olay kartı adayları üretmek.

## Kullanılan İstem

> `alarms.json`, `service_dependencies.csv` ve `host_inventory.csv` dosyalarını birlikte analiz et. Tüm alarm kayıtlarını hesaba kat. Zaman yakınlığı, ortak veri merkezi/kabin ve yönlü servis bağımlılıklarını kullanarak bağımsız olay adaylarını ayır. Her aday için kök neden hipotezi, karşı olasılık, etkilenen servisler, kanıtlar ve ilk aksiyonu ver. Alarm tipini tek başına korelasyon kanıtı kabul etme; belirsizliği açıkça belirt.

## İnsan Denetimi ve Sonuç

- İnsan ekip, model/araç önerilerini veri ve bağımlılık grafiği üzerinden tekrar doğruladı.
- Nihai MVP, LLM kararına bağlı değildir; `src/alarm_core.py` sabit ve açıklanabilir kurallarla çalışır.
- Doğrulanan demo kartları: DC1/rack-A ağ olayı, billing-db disk olayı ve harici ödeme sağlayıcısı olayı.
