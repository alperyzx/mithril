# ao-hackathon-2026-mithril

## Proje adı ve tek cümlelik özet
**ao-hackathon-2026-mithril** — Operasyonel gürültüyü anlamlı sinyallere dönüştüren, aksiyon öneren hackathon prototipi.

## Çözdüğünüz problem
Etkinlik gününde açıklanan senaryo ve veri setinden operasyonel sinyalleri çıkarıp karar almayı hızlandırmak.

## Çözümünüzün nasıl çalıştığı
1. Veriyi alır ve normalize eder.
2. Gürültü/sinyal ayrımı yapar.
3. Açıklanabilir aksiyon önerileri üretir.
4. Aksiyonların takibini tek akışta gösterir.

## Kurulum adımları

Bu demo yalnızca Python standart kütüphanesini kullanır. Paket kurulumu, `.env`
dosyası, veritabanı veya dış servis gerekmez.

1. Python 3.12+ ile proje köküne gelin.
2. Otomatik testleri çalıştırın:

	```bash
	make test
	```

3. Yerel demo sunucusunu başlatın:

	```bash
	make run
	```

4. Tarayıcıda `http://127.0.0.1:8000` adresini açın. Sunucuyu kapatmak için
	terminalde `Ctrl+C` kullanın.

## Çalıştırma komutu
`make run`, `docs/project/senaryo/` altındaki kanonik senaryo verisini doğrudan
okur ve `src/alarm_core.py` ile korelasyon sonucunu üretir. Girdi senaryo
dosyaları kopyalanmaz veya değiştirilmez.

## Canlı demo akışı

1. Özet metrikte tüm veri paketinin `3000/3000` işlendiğini, olay kartı
	sayısının `≤15` olduğunu gösterin.
2. Üç olay kartında kök neden hipotezini, alternatif açıklamayı, kanıtları,
	etkilenen servisleri ve aksiyon sahibi/durumunu açın.
3. **Canlı Aksiyon Takibi** alanında bir kart seçin; durumu örneğin
	**Çalışılıyor** veya **Çözüldü** olarak güncelleyin. Güncelleme aynı sayfada
	görünür ve demo sunucusu çalıştığı sürece bellek içinde tutulur.
4. **Gürültü Denetim İzi** alanında kart dışı alarmların neden kodları ile
	(izole düşük şiddet, topoloji kanıtı yok, tekrarlayan türev belirti, olay
	penceresi dışında) sayıldığını gösterin.

## Teknik notlar

- Uygulama: `src/demo_server.py` (`http.server` tabanlı yerel sunucu)
- Korelasyon: `src/alarm_core.py` (deterministik ve açıklanabilir kurallar)
- Arayüz varlıkları: `src/demo_assets/`
- Aksiyon durumu kalıcı değildir; sunucu yeniden başlatılınca `open` durumuna
  döner. Bu, harici bağımlılığı olmayan canlı-demo geri dönüş yoludur.

## Kullanılan tüm AI araçları ve model sürümleri
- GitHub Copilot — model: `SAKA gpt-5.6-terra`; kod, test, dokümantasyon ve korelasyon analizi desteği.
- Claude SAKA / Codex — ekip tarafından kullanılabilecek araçlar; bu repoda sürüm bilgisi kaydedilmeden bir model çıktısı ürün kararına bağlanmamıştır.
- Kritik prompt ve insan denetimi kaydı: `prompts/prompt-01-scenario-analysis.md`.

## MCP sunucu listesi
- Bu MVP'de MCP sunucusu kullanılmadı.

## Entegre edilen API'ler
- Harici API kullanılmadı. Demo, verilen sentetik veri paketiyle yerelde çalışır.

## Ekran görüntüleri

### Alarm karar merkezi
![Alarm karar merkezi](demo/dashboard-overview.png)

### Canlı aksiyon durumu
![Aksiyon durumu geçişi](demo/action-status-transition.png)

### Gürültü denetimi
![Gürültü denetimi](demo/noise-audit.png)

## Deploy URL ve bilinen sınırlar
- Deploy URL: Yerel demo — `http://127.0.0.1:8000` (`make run` sonrası).
- Bilinen sınırlar:
	- Korelasyon kuralları S-A1 senaryosundaki kanıt eşiklerine göre deterministiktir; farklı senaryolarda eşikler yapılandırılmalıdır.
	- Aksiyon durumu bellek içinde tutulur ve sunucu yeniden başlatıldığında sıfırlanır.

## Takım
- Alper
- Altan
- Yiğit
