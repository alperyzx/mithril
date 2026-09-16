# GitHub Copilot Özel Talimatları — Mithril Hackathon

Bu talimatlar, Mithril hackathon projesi için GitHub Copilot davranışını özelleştirir.

## 1. Jüri Denetleme Agenti

Kullanıcı aşağıdaki komutlardan birini yazdığında, **jüri denetleme agentini** kullanın:

- "jüri denetlemesini yap"
- "jüri raporunu göster"
- "uyum kontrolü yap"
- "submission kontrol et"
- "jury audit"
- "check compliance"

### Agent İş Akışı

1. **Raporu Çalıştır**
	 ```bash
	 cd /home/alper/Projects/mithril
	 python3 scripts/jury-audit.py
	 ```

2. **Raporu Oku ve Açıkla**
	 - `docs/reports/juri-report.json` dosyasını oku
	 - Uyum yüzdesini (%) göster
	 - **Başarısız kontrol noktalarını** listele:
		 - Nedir?
		 - Neden başarısız?
		 - Nasıl düzeltilir?

3. **İyileştirme Önerileri**
	 - Eksik alanları tamamlamak için spesifik adımlar
	 - README, submission.json, demo vb. güncellemeler
	 - Dosya yolu ve önerilen içerik

## 2. MVP Öncelikleri

Jüri denetleme bağlamında, şu sıralamayla düzelt:

1. **Kritik (Engellemeyen)**: README ve submission.json tamamlama
2. **Yüksek**: Demo görselleri ve test dosyaları
3. **Orta**: Makefile ve prompt örnekleri
4. **Düşük**: Ek dokümantasyon

## 3. Rapor İçeriği Örnekleri

Raporlar şu bilgileri içermelidir:

```json
{
	"timestamp": "2026-09-16T14:09:42...",
	"project": "ao-hackathon-2026-mithril",
	"compliance": {
		"total_checks": 45,
		"passed": 37,
		"failed": 8,
		"percentage": 82.2
	},
	"status": "⚠ 82.2% COMPLIANCE"
}
```

## 4. Denetleme Kuralları

Kurallar dosya: `prompts/jury-rules.md`

4 kategori, 32+ kontrol noktası:
- 📋 Belgelendirme ve Hazırlık
- 📂 Teknik Gerçeklik
- 🤖 AI Kullanımı ve Şeffaflık
- 🎬 Demo ve Deliverables

## 5. Copilot Davranışı

- **Denetleme istendiğinde**: Her zaman raporu çalıştır, sonra bulguları açıkla
- **Düzeltme önerileri**: Spesifik dosyalar ve içerik
- **İteratif iyileştirme**: "Raporu yeniden çalıştır" komutuna hazır ol
- **100% hedefi**: Tüm 45 kontrol noktasını yeşil yapmaya yardımcı ol

## 6. Özel Dosyalar

- `prompts/jury-rules.md` — Tüm denetleme kuralları
- `scripts/jury-audit.py` — Denetleme script'i
- `docs/reports/juri-report.json` — En son rapor (otomatik oluşturulur)
- `.github/agents/mithril-jury-audit.agent.md` — Agent belgesi
- `AI_JURI.md` — Jüri özeti (projeye özel)

## 7. Hedef

- **Başlangıç**: 82.2% (37/45 kontrol noktası ✓)
- **Hedef**: 100% (45/45 kontrol noktası ✓)

---

**Güncelleme Tarihi**: 2026-09-16
**Agent Sürümü**: 1.0
