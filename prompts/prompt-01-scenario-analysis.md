# Prompt Kaydı 01 — Senaryo Analizi ve Kök Neden Hipotezleri

## Kayıt Kapsamı

Bu dosya, Mithril projesinin Copilot sohbet geçmişinden çıkarılan kritik
istemleri, kararları ve insan ekip yönlendirmelerini özetler. Tarihçe, yalnız
nihai tasarıma veya teslim artefaktlarına etkisi olan istemleri kapsar.

## Prompt Geçmişi

| Aşama | İnsan ekip istemi / kararı | Çıktı ve etkisi |
|---|---|---|
| Ekip ve koordinasyon | "Üst koordinasyon PM/DRI rolü biz insan ekibi olacağız. Altan, Yiğit ve ben (Alper)." | İnsan PM/DRI sahipliği belgelendi; agent'lar uygulama ve denetim rolünde kaldı. |
| Jüri uyumu | "Jüri denetlemesini anlık yapan bir agent oluştur." | Jüri agent'ı, kural seti ve otomatik uyum raporu oluşturuldu. |
| Senaryo analizi | "Dokümanlar ve senaryo ekte. İncele ve teknik bir analiz dokümanı hazırla." | Veri profili, korelasyon yaklaşımı ve MVP mimarisi `docs/project/teknik-analiz.md` altında çıkarıldı. |
| İnsan analiziyle karşılaştırma | "Bu da bizim incelememiz. İki analizi karşılaştır." | DC1/rack-A ağ, billing-db disk ve harici ödeme sağlayıcısı olay hipotezleri ham veri ve bağımlılık grafiğiyle doğrulandı. |
| Teslim önceliği | "Proje teslimi için hazırlıkları yapalım." | Deterministik korelasyon motoru, testler, yerel demo, jüri özeti ve teslim metadata'sı tamamlandı. |
| Metrik doğrulama | "3000-2211 olması gerekmiyor mu?" | Gürültü temizleme oranı $2211 / 3000 = 73.7\%$ olarak ayrıştırıldı; olay kartı indirgeme metriğiyle karıştırılmaması kararlaştırıldı. |
| Kanıt doğrulama | "Canlı aksiyon takibini kaldıralım. Bunun yerine raw data ile hipotezlerimizi doğrulayacak interaktif bir panel ekleyelim." | Seçili olay için ham alarm, zaman yoğunluğu, alarm türü, servis ve DC/kabin dağılımlarını gösteren doğrulama paneli eklendi. |
| Sunum sadeliği | "High güven ifadesine gerek yok. Buraya P1 ile bağlantılı teknik bir ifade koy." | Belirsiz güven etiketi kaldırıldı; P1 kartlarda `S5 kritik alarm` teknik göstergesi kullanıldı. |
| Son dokümantasyon | "Projemiz tamam. Dokümanları güncelle." | README, AI jüri özeti, mimari, fazlar, plan ve submission metadata'sı nihai iş akışıyla senkronlandı. |

## Amaç

S-A1 Alarm Fırtınası veri paketindeki alarmları, servis bağımlılıkları ve host
envanteriyle birlikte inceleyerek açıklanabilir olay kartı adayları üretmek.

## Kullanılan İstem

> `alarms.json`, `service_dependencies.csv` ve `host_inventory.csv` dosyalarını birlikte analiz et. Tüm alarm kayıtlarını hesaba kat. Zaman yakınlığı, ortak veri merkezi/kabin ve yönlü servis bağımlılıklarını kullanarak bağımsız olay adaylarını ayır. Her aday için kök neden hipotezi, karşı olasılık, etkilenen servisler, kanıtlar ve ilk aksiyonu ver. Alarm tipini tek başına korelasyon kanıtı kabul etme; belirsizliği açıkça belirt.

## Uygulanan Çıktı İlkeleri

- Tüm 3.000 kayıt işlenir; alarm örneklemesi yapılmaz.
- Kök neden iddiaları zaman, topoloji ve yönlü bağımlılık kanıtıyla desteklenir.
- LLM/agent önerileri, insan ekip tarafından ham veri ve bağımlılık grafiğiyle doğrulanır.
- Demo, açıklanabilir ve deterministik çekirdeğe dayanır; ham veri paneli hipotezlerin denetlenmesini sağlar.

## İnsan Denetimi ve Sonuç

- İnsan ekip, model/araç önerilerini veri ve bağımlılık grafiği üzerinden tekrar doğruladı.
- Nihai MVP, LLM kararına bağlı değildir; `src/alarm_core.py` sabit ve açıklanabilir kurallarla çalışır.
- Doğrulanan demo kartları: DC1/rack-A ağ olayı, billing-db disk olayı ve harici ödeme sağlayıcısı olayı.
