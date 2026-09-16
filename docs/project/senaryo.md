SENARYO S-A1
Alarm Fırtınası
Alert Storm Correlator
"Saat 02 : 14. Üç bin alarm. Kaçı gerçek?
Nöbetçi mühendisin elinde yedi dakika var. Ona neye bakacağını söyleyin."


📦 Veri paketi: ./docs/project/senaryo/*
Paket içeriği: alarms.json · alarms.csv · service_dependencies.csv · host_inventory.csv · VERI_SOZLUGU.md · SENARYO_BRIFINGI.md


🎬 SAHNE
Eylül ayının bir gecesi, saat 02 : 14. Operasyon merkezindeki alarm ekranı sessizce akmaya başlar, sonra hızlanır. Farklı izleme sistemlerinden, farklı servislerden, farklı şiddetlerde alarmlar birbirini kovalar. Nöbetçi mühendis ekrana baktığında iki saatlik pencerede binlerce satır görür.

O gece birden fazla şey aynı anda ters gitmiştir. Bazıları birbiriyle ilişkilidir, bazıları tamamen bağımsızdır; alarm ekranında hepsi yan yana akmaktadır.


🎯 ÇÖZÜLMESİ BEKLENEN PROBLEM
Nöbetçi mühendisin karşılaştığı asıl güçlük alarm sayısı değil, alarmlar arasındaki neden-sonuç ilişkisinin görünmez olmasıdır. Hangi alarmın kök neden, hangisinin türev etki, hangisinin ise tamamen alakasız gürültü olduğu ayırt edilemediği için müdahale sırası yanlış kurulur ve çözüm süresi uzar.

Göreviniz: Alarm selini, nöbetçi mühendisin okuyup harekete geçebileceği birkaç karara indirgemek ve bu indirgemenin gerekçesini gösterebilmek.


📊 VERİ PAKETİ
Gözlem penceresi: 10 Eylül 2026 Perşembe, 01:30 – 03:30 (2 saat)  ·  3.000 alarm  ·  27 servis  ·  56 sunucu  ·  32 bağımlılık kaydı. Tüm veriler sentetiktir; hiçbir kurumsal sisteme erişim gerekmez.
DOSYA

İÇERİK VE ŞEMA

alarms.json

3.000 alarm kaydı. Alanlar: alarm_id, timestamp (ISO-8601), source_system, host, service, severity (1-5), alarm_type, message, tags{veri_merkezi, kabin, ortam}

alarms.csv

Aynı verinin düz tablo hâli; tags üç sütuna açılmıştır. İçerik farkı yoktur, hangisiyle çalışacağınız sizin tercihinizdir.

service_dependencies.csv

kaynak_servis, hedef_servis, bagimlilik_tipi (senkron/asenkron), kritiklik
Okuma yönü: kaynak_servis, hedef_servis'e bağımlıdır. Hedef bozulursa kaynak etkilenir.

host_inventory.csv

host, servis, veri_merkezi (dc1/dc2), kabin (rack-A/B/C), ortam, is_kritikligi

VERI_SOZLUGU.md

Tüm alan açıklamaları, şiddet ölçeğinin anlamı ve 26 alarm tipi kodunun tam listesi. Kod yazmadan önce mutlaka okuyun.


Veri hakkında bilmeniz gerekenler
• Veri setinde birden fazla bağımsız gerçek olay vardır. Kaç tane olduğu size söylenmeyecektir; bunu veriden çıkarmak senaryonun parçasıdır.
• Alarmların önemli bir bölümü arka plan gürültüsüdür: hiçbir olayla ilgisi yoktur ve hiçbir aksiyona yol açmaz.
• Bazı olaylar ani patlama şeklinde, bazıları ise uzun süreye yayılarak gelişir. İkincisini yakalamak birincisinden zordur.
• Alarm tipleri olaylar arasında paylaşılır. Yalnızca alarm tipine bakarak ayrım yapmak yanıltıcıdır.
• Doğrulama verisi (hangi alarmın hangi olaya ait olduğu) jüriye değerlendirme aşamasında açılacaktır.


✅ ZORUNLU GEREKSİNİMLER
01.  Verilen alarm akışının tamamını okuyup işleyebilmek. Kısmi veri ile çalışan çözümler eksik sayılır.
02.  Alarmları anlamlı gruplara indirgemek ve her grup için tek bir olay kartı üretmek.
03.  Her olay kartında kök neden hipotezi, etkilenen servis listesi, alarm sayısı ve zaman aralığını göstermek.
04.  Her kart için önerilen ilk aksiyonu üretmek ve bu aksiyonu sahip ile durum bilgisi içerecek şekilde kayıt altına almak.
05.  OPSİYONEL  Bir aksiyonun açıldıktan sonra kapanana kadar izlenebildiğini demoda göstermek. Yapılması durumunda çözümünüze güç katar.


⭐ BONUS — X-Factor alanı
• Kök neden hipotezinin neden bu olduğunu doğal dille açıklamak ve karşı olasılıkları da belirtmek
• Gürültü olarak elenen alarmların neden elendiğini gösteren bir denetim görünümü sunmak
• Benzer geçmiş olay örüntülerini yakalayıp kartın üzerine iliştirmek



🚫 KAPSAM DIŞI — vakit harcamayın
• Gerçek zamanlı akış işleme altyapısı gerekli değildir; dosyayı toplu okumak yeterlidir
• Kullanıcı yönetimi, oturum açma ve yetkilendirme beklenmemektedir
• Kalıcı veritabanı zorunlu değildir; bellek içi saklama kabul edilir


☑️ KABUL KRİTERLERİ
Demo öncesi kendi kendinizi denetleyin:
☐  Uygulama, verilen veri paketiyle sıfırdan ayağa kalkıp sonuç üretiyor
☐  3.000 alarm, en fazla on beş olay kartına indirgenmiş
☐  OPSİYONEL En az bir aksiyon demoda açılıp durumu değiştirilerek gösteriliyor
☐  Kök neden hipotezleri ekranda gerekçesiyle görülebiliyor



📏 BAŞARI NASIL ÖLÇÜLECEK
İndirgeme oranı — kart sayısının toplam alarm sayısına oranı
Kök neden isabeti — kapalı doğrulamadaki gerçek köklerden kaçını yakaladığınız
Yanlış birleştirme — ilgisiz iki olayı tek karta koyup koymadığınız
Gürültü elemesi — elenen alarmların ne kadarının gerçekten gürültü olduğu


💬 PEŞİN YANITLANAN SORULAR
Aşağıdaki sorular zaten yanıtlanmıştır; lütfen önce bu listeyi okuyun.
Alarmların hepsini kullanmak zorunda mıyız?
Evet. Veri setinin tamamı işlenmelidir. Örnekleme yaparsanız demoda mutlaka belirtin.



Kök nedeni bulamazsak sıfır mı alırız?
Hayır. Doğru gerekçelendirilmiş yanlış hipotez, gerekçesiz doğru hipotezden daha yüksek puan alabilir. Jüri düşünme sürecinizi değerlendirir.



Kaç tane gerçek olay var?
Söylenmeyecektir. Bunu veriden çıkarmak senaryonun bir parçasıdır. Çözümünüz, kaç olay olduğunu bilmeden çalışabilmelidir.



Hazır korelasyon kütüphanesi kullanabilir miyiz?
Evet, tüm açık kaynak kütüphaneler serbesttir. Kullandığınız her kütüphaneyi README dosyanızda belirtin.



Arayüz web olmak zorunda mı?
Hayır. Terminal, masaüstü veya web fark etmez. Tek şart: demoda canlı çalışması.



JSON mu CSV mi kullanmalıyız?
İkisi de aynı veriyi içerir. Tercih tamamen sizindir; bu bir tuzak değildir.



Kaç olay kartı üretmeliyiz?
Üst sınır on beştir. Kesin sayı sizin tasarım kararınızdır ve jüri bu kararın gerekçesini soracaktır. "Nöbetçinin bakabileceği kadar" iyi bir ölçüttür.



Veriyi değiştirebilir, temizleyebilir miyiz?
İşleme sırasında istediğiniz dönüşümü yapabilirsiniz. Ancak orijinal dosyaları repoya değiştirilmemiş hâliyle koymayın; veri paketini repoya eklemenize gerek yoktur.


Son kontrol listesi:
☐ Repo public  ·  ☐ README.md güncel  ·  ☐ AI_JURI.md dolduruldu  ·  ☐ submission.json geçerli JSON
☐ docs/ klasörü dolu  ·  ☐ AI yapılandırma dosyası mevcut  ·  ☐ .env commit edilmemiş  ·  ☐ Ekran görüntüleri eklendi


🎤 Sunumda jürinin bakacağı üç şey
1 · AI Stratejiniz ve iş akışı — Yapay zekâyı hangi iş bölümüyle kullandınız, hangi kararı siz verdiniz?
2 · Canlı demo — Slaytlara boğulmadan çalışan ürünü açın; problemi nasıl çözdüğünüzü sahnede gösterin.
3 · X-Factor — Sıradan bir veri listelemenin ötesine geçen en akıllı özelliğiniz nedir?

