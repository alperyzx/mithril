# mimari.md

## Bileşenler
- Veri giriş ve doğrulama katmanı
- Deterministik korelasyon/sinyal motoru
- Olay kartı ve gürültü denetim çıktısı
- Ham veri hipotez doğrulama API'si
- Demo arayüzü ve veri görselleştirmeleri

## Akış
Girdi -> Normalizasyon -> Korelasyon -> Olay Kartı / Gürültü -> Ham Veri Doğrulama -> Görselleştirme

## S-A1 Deterministik Korelasyon Çekirdeği

`src/alarm_core.py`, kaynak veriyi kopyalamadan `docs/project/senaryo/alarms.json`,
`host_inventory.csv` ve yönlü `service_dependencies.csv` dosyalarını okur. Girdi
doğrulaması alarm kimliği, zaman, şiddet ve host/servis envanter eşleşmesini
kapsar.

Üç kart yalnızca kanıt eşikleri geçildiğinde üretilir: DC1/rack-A ağ öncülleri,
`billing-db` disk doluluğu ve `payment-provider-gw` dış erişim sinyalleri.
Bağımlılık grafiği, ağ olayında aşağı akış semptomları bağlamak için kullanılır;
ödeme ve billing kartlarında yalnız doğrulanmış doğrudan zincirler kullanılır.
Her alarm, bir kartın olayı veya gerekçeli gürültü (`noise_reason`) olarak tek
kez çıktılanır. Çekirdek harici paket veya LLM kullanmaz.

`src/demo_server.py`, seçili kart için yalnız ilgili zaman penceresi ve
etkilenen servislerdeki ham alarmları sunar. Arayüz; dakika bazlı yoğunluk,
alarm türü, servis ve veri merkezi/kabin dağılımlarını standart kütüphane ile
görselleştirir. Bu görünüm hipotez kanıtını denetlenebilir kılar.

Çalıştırma: `python3 -m src.alarm_core --output /tmp/s-a1-report.json` veya `make run`
