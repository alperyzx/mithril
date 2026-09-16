# AI Jüri Özeti

## Proje
- Ad: ao-hackathon-2026-mithril
- Takım: Alper, Altan, Yiğit
- Kategori: Operasyonel sinyal çıkarımı ve aksiyon takibi

## 1) Problem Tanımı
Etkinlik günü açıklanan senaryo kapsamında, yüksek hacimli operasyonel gürültü içinden anlamlı sinyalleri hızlı ve izlenebilir şekilde çıkarmak.

## 2) Çözüm Özeti
- Tüm 3.000 alarmı, envanter ve yönlü servis bağımlılıklarıyla doğrulama
- Deterministik zaman/topoloji/etki korelasyonu ile üç kanıta dayalı olay kartı
- Kök neden hipotezi, karşı olasılık, kanıtlar ve sahipli ilk aksiyon
- Her hipotezi ham alarm kayıtları, zaman yoğunluğu ve dağılım görselleştirmeleriyle doğrulayan etkileşimli panel

## 3) Mimari (Kısa)
- `src/alarm_core.py`: açıklanabilir, bağımlılıksız korelasyon motoru
- `src/demo_server.py`: yerel canlı demo sunucusu
- `src/demo_assets/`: olay kartları ve ham veri görselleştirmeleri
- `docs/`: plan, fazlar, mimari
- `prompts/`: kritik prompt kayıtları
- `demo/`: ekran görüntüleri / video bağlantısı

## 4) AI Kullanımı
- GitHub Copilot (`SAKA gpt-5.6-terra`): kod üretimi, test, refactor ve dokümantasyon desteği
- Kritik analiz istemi `prompts/prompt-01-scenario-analysis.md` altında kayıtlıdır.
- Nihai korelasyon kararları deterministik kurallarla üretilir ve insan ekip tarafından doğrulanır.
- Playwright, yerel demo arayüzünün doğrulanması ve teslim ekran görüntülerinin
	alınması için geliştirme aşamasında kullanıldı; uygulamanın runtime bağımlılığı değildir.

## 5) Değerlendirme İçin Hızlı Kontrol
- README zorunlu başlıklar tam mı?
- `submission.json` alanları dolu mu?
- Demo artefaktları (`demo/`) mevcut mu?
- Çalıştırma adımları tekrar edilebilir mi?

## 6) Bilinen Sınırlar
- Korelasyon eşikleri S-A1 veri paketi için kalibre edilmiştir.
- Ham veri doğrulama görünümü yalnız seçili olayın zaman/servis/topoloji penceresini gösterir; genel amaçlı bir sorgu arayüzü değildir.
