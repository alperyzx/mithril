# mimari.md

## Bileşenler
- Veri giriş katmanı
- İşleme/sinyal motoru
- Aksiyon ve çıktı katmanı
- Demo arayüzü

## Akış
Girdi -> Normalizasyon -> Sinyal Çıkarma -> Aksiyon -> Görselleştirme

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

Çalıştırma: `python3 -m src.alarm_core --output /tmp/s-a1-report.json`
