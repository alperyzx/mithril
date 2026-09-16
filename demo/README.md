# Demo Assets

Bu klasör, çalışan yerel demonun teslim için alınmış ekran görüntülerini içerir:

- `dashboard-overview.png` — 3.000/3.000 işleme, üç olay kartı ve indirgeme özeti
- `action-status-transition.png` — canlı aksiyonun `Çözüldü` durumuna geçişi
- `noise-audit.png` — gürültü denetim nedenleri ve sayıları

## Tekrarlanabilir demo yakalama adımları

1. Proje kökünde `make test` çalıştırın.
2. `make run` ile yerel sunucuyu başlatın.
3. Tarayıcıda `http://127.0.0.1:8000` adresini açın.
4. Birinci karede `3000/3000` işleme özeti, en fazla 15 kart sınırı ve üç olay
	kartını görünür bırakın.
5. İkinci karede **Canlı Aksiyon Takibi** bölümünden bir kartın durumunu
	**Çalışılıyor** veya **Çözüldü** olarak değiştirin; karttaki durum rozetinin
	güncellendiğini gösterin.
6. Üçüncü karede **Gürültü Denetim İzi** neden ve sayım listesini gösterin.

Demo, yalnızca Python standart kütüphanesiyle çalışır. Senaryo girdileri
`docs/project/senaryo/` altında yerinde okunur; bu klasöre kopyalanmaz.
