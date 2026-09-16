# Mithril Rol ve Sorumluluklar (RACI)

## Üst Koordinasyon (İnsan Ekip)

**PM/DRI (ortak sahiplik):** Alper, Altan, Yiğit

Bu rolün kapsamı:
- Önceliklendirme ve kapsam kararı
- 17:30 hard-stop teslim onayı
- Sunum akışı (7 dk anlatım + 3 dk Q&A)
- Agent çıktılarında nihai karar ve birleştirme

---

## Agent Rolleri

- `Mithril Data & AI Engineer`
- `Mithril Full-stack Demo Engineer`
- `Mithril QA & Release Engineer`
- `Mithril Jury Audit Agent`

---

## RACI Matrisi

| İş Kalemi | PM/DRI (Alper+Altan+Yiğit) | Data & AI | Full-stack Demo | QA & Release | Jury Audit |
|---|---|---|---|---|---|
| Problem çözüm yönü ve kapsam | **A/R** | C | C | C | I |
| Veri işleme + sinyal mantığı | A | **R** | C | C | I |
| Demo akışı ve UI | A | C | **R** | C | I |
| README + submission.json senkronu | A | I | C | **R** | C |
| Uyum denetimi (kurallar) | A | I | I | C | **R** |
| Raporlama (`docs/reports/juri-report.json`) | A | I | I | C | **R** |
| Hard-stop öncesi go/no-go | **A/R** | C | C | **R** | C |
| Sahne sunumu ve Q&A sahipliği | **A/R** | C | C | C | I |

> R = Responsible, A = Accountable, C = Consulted, I = Informed
