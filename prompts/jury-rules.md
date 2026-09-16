# Jüri Değerlendirme Kuralları

Bu dosya, ao-hackathon-2026 jüri denetlemesinin tüm kontrol noktalarını içerir.

## Kategori 1: Belgelendirme ve Hazırlık

### 1.1 README Zorunlu Başlıkları
- [ ] **Proje adı ve tek cümlelik özet** — Proje adı ve çözümün kısa açıklaması
- [ ] **Çözdüğünüz problem** — Hackathon senaryosundan problem tanımı
- [ ] **Çözümünüzün nasıl çalıştığı** — Adım adım akış açıklaması (en az 3 adım)
- [ ] **Kurulum adımları** — Tekrarlanabilir kurulum (klona, env, dependencies, vb.)
- [ ] **Çalıştırma komutu** — Tek satırda çalıştırılacak komut
- [ ] **Kullanılan tüm AI araçları ve model sürümleri** — Hangi araçlar, hangi sürümler
- [ ] **MCP sunucu listesi** — Entegre edilen MCP sunucuları (varsa)
- [ ] **Entegre edilen API'ler** — API integrayonları (varsa)
- [ ] **Ekran görüntüleri** — Demo görselleri (minimum 1, önerilen 2-3)
- [ ] **Deploy URL ve bilinen sınırlar** — Deploy bağlantısı ve kapsam sınırlaması
- [ ] **Takım** — Takım üyeleri

### 1.2 submission.json Bütünlüğü
- [ ] `team.name` dolu
- [ ] `team.members` (en az 1)
- [ ] `project.title` dolu
- [ ] `project.one_liner` dolu (en az bir cümle)
- [ ] `project.problem` dolu
- [ ] `project.status` dolu (`skeleton`, `wip`, `alpha`, `beta`, `rc`, `released`)
- [ ] `runtime.setup` dolu
- [ ] `runtime.run_command` dolu
- [ ] `ai.tools` (en az 1 araç, `name` ve `model` dolu)
- [ ] `delivery.public_repo_required` boolean
- [ ] `delivery.deploy_url` dolu veya açıklanmış

### 1.3 AI Jüri Özeti (AI_JURI.md)
- [ ] Mevcut ve okunabilir
- [ ] Problem Tanımı bölümü
- [ ] Çözüm Özeti bölümü
- [ ] Mimari açıklaması
- [ ] AI Kullanımı bölümü
- [ ] Değerlendirme Kontrol Listesi
- [ ] Bilinen Sınırlar bölümü

## Kategori 2: Teknik Gerçeklik

### 2.1 Depo Bütünlüğü
- [ ] `.git/` var (git reposu)
- [ ] `.gitignore` var ve `.env`, `node_modules`, vb. kapsıyor
- [ ] `.env.example` var ve çalışan örnek içeriyor
- [ ] Kritik dosyalar `.github/` veya `.vscode/` içinde değil

### 2.2 Kod Yapısı
- [ ] `src/` klasörü var
- [ ] `src/README.md` var ve amaçlarını açıklıyor
- [ ] `tests/` klasörü var (en az 1 test dosyası)
- [ ] `docs/` klasörü var ve mimaride referans var

### 2.3 Çalıştırılabilirlik
- [ ] `make run` komutu hatasız çalışıyor
- [ ] Çıkış (stdout) anlamlı ve test edilebilir
- [ ] 30 saniye içinde tamamlanıyor (veya uzun işlem ise progress gösteriyor)
- [ ] Hata mesajları okunabilir

### 2.4 İşlevsellik
- [ ] Giriş verisi işleniyor (normalize, parse, vb.)
- [ ] Sinyal çıkarımı veya karar mantığı var
- [ ] Çıktı (signal, action proposal, vb.) üretiliyor
- [ ] Önceki adımlara referans (README veya docs)

## Kategori 3: AI Kullanımı ve Şeffaflık

### 3.1 AI Araçları Açıklaması
- [ ] Her AI aracı için model sürümü belirtilmiş
- [ ] Claude/LLM seçimi ve neden yapıldığı
- [ ] Prompt engineering başında `prompts/` klasöründe referans
- [ ] Kod üretimi, hata ayıklama, dokümantasyon alanları açıklanmış

### 3.2 MCP Sunucuları (Varsa)
- [ ] `submission.json` > `integrations.mcp_servers` dolu
- [ ] MCP sunucusu konfigürasyonu `.env.example` veya docs'ta
- [ ] İşlevselliğin kaynağı belirtilmiş

### 3.3 Prompt Kayıtları
- [ ] `prompts/` klasöründe en az 1 örnek prompt var
- [ ] Her prompt dosya adı açıklayıcı (ör. `prompt-01-problem-framing.md`)
- [ ] Prompt içeriği jüri tarafından değerlendirilebilir

## Kategori 4: Demo ve Deliverables

### 4.1 Demo Görselleri
- [ ] `demo/` klasörü var
- [ ] En az 1 ekran görüntüsü (PNG, JPG, WebP)
- [ ] README'de referans var (`demo/` klasörüne bakın)
- [ ] Görüntüler proje çıkışını veya arayüzü gösteriyor

### 4.2 Deploy (Varsa)
- [ ] Deploy URL `submission.json` > `delivery.deploy_url` dolu
- [ ] Deploy accessible ve test edilebilir
- [ ] Deploy logs veya health check var (docs'ta)

## Kategori 5: Uyum Toplamı

- [ ] **Kategori 1 (Belgelendirme)**: 12/12 kontrol noktası
- [ ] **Kategori 2 (Teknik)**: 9/9 kontrol noktası
- [ ] **Kategori 3 (AI Kullanımı)**: 7/7 kontrol noktası
- [ ] **Kategori 4 (Demo)**: 4/4 kontrol noktası
- [ ] **TOPLAM**: 32/32

## Notlar
- Bu kontrol listesi `juri-audit-agent` tarafından otomatik olarak denetlenir.
- Her hata ya da boş alan bir rapor satırı olarak kaydedilir.
- Jüri raporlandırması: `juri-report.json` dosyası.
