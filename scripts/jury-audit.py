#!/usr/bin/env python3
"""
Jüri Denetleme Agenti — ao-hackathon-2026 uyum kontrolü

Bu script, prompts/jury-rules.md'de tanımlanan tüm 32 kontrol noktasını kontrol eder
ve docs/reports/juri-report.json dosyası oluşturur.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Proje kök dizini
PROJECT_ROOT = Path(__file__).parent.parent
REPORT_FILE = PROJECT_ROOT / "docs" / "reports" / "juri-report.json"


class JuryAudit:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
        self.categories = {
            "Belgelendirme ve Hazırlık": [],
            "Teknik Gerçeklik": [],
            "AI Kullanımı ve Şeffaflık": [],
            "Demo ve Deliverables": []
        }

    def check(self, category: str, rule: str, passed: bool, details: str = ""):
        """Kontrol noktasını kaydet"""
        item = {
            "rule": rule,
            "passed": passed,
            "details": details
        }
        self.categories[category].append(item)
        
        if passed:
            self.passed.append(f"✓ {category}: {rule}")
        else:
            self.failed.append(f"✗ {category}: {rule}")
            if details:
                self.failed.append(f"  → {details}")

    def warning(self, msg: str):
        """Uyarı ekle"""
        self.warnings.append(msg)

    # ========================
    # KATEGORİ 1: Belgelendirme
    # ========================

    def check_readme(self):
        """README.md kontrol noktaları"""
        readme = PROJECT_ROOT / "README.md"
        
        if not readme.exists():
            self.check("Belgelendirme ve Hazırlık", "README.md var", False, "Dosya bulunamadı")
            return
        
        content = readme.read_text(encoding='utf-8')
        
        checks = {
            "Proje adı ve tek cümlelik özet": "## Proje adı ve tek cümlelik özet",
            "Çözdüğünüz problem": "## Çözdüğünüz problem",
            "Çözümünüzün nasıl çalıştığı": "## Çözümünüzün nasıl çalıştığı",
            "Kurulum adımları": "## Kurulum adımları",
            "Çalıştırma komutu": "## Çalıştırma komutu",
            "Kullanılan tüm AI araçları": "## Kullanılan tüm AI araçları",
            "MCP sunucu listesi": "## MCP sunucu listesi",
            "Entegre edilen API'ler": "## Entegre edilen API",
            "Ekran görüntüleri": "## Ekran görüntüleri",
            "Deploy URL ve bilinen sınırlar": "## Deploy URL",
            "Takım": "## Takım"
        }
        
        for check_name, pattern in checks.items():
            found = pattern in content
            self.check("Belgelendirme ve Hazırlık", f"README: {check_name}", found,
                      "" if found else f"Başlık veya içerik bulunamadı: {pattern}")

    def check_submission_json(self):
        """submission.json kontrol noktaları"""
        subfile = PROJECT_ROOT / "submission.json"
        
        if not subfile.exists():
            self.check("Belgelendirme ve Hazırlık", "submission.json var", False, "Dosya bulunamadı")
            return
        
        try:
            data = json.loads(subfile.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            self.check("Belgelendirme ve Hazırlık", "submission.json geçerli JSON", False, str(e))
            return
        
        checks = [
            ("team.name", lambda d: d.get("team", {}).get("name"), "Takım adı"),
            ("team.members", lambda d: d.get("team", {}).get("members"), "Takım üyeleri"),
            ("project.title", lambda d: d.get("project", {}).get("title"), "Proje başlığı"),
            ("project.one_liner", lambda d: d.get("project", {}).get("one_liner"), "Bir cümlede özet"),
            ("project.problem", lambda d: d.get("project", {}).get("problem"), "Problem tanımı"),
            ("project.status", lambda d: d.get("project", {}).get("status"), "Proje durumu"),
            ("runtime.setup", lambda d: d.get("runtime", {}).get("setup"), "Kurulum komutu"),
            ("runtime.run_command", lambda d: d.get("runtime", {}).get("run_command"), "Çalıştırma komutu"),
            ("ai.tools", lambda d: d.get("ai", {}).get("tools"), "AI araçları"),
            ("delivery.public_repo_required", lambda d: d.get("delivery", {}).get("public_repo_required") is not None, "Depo zorunluluğu"),
            ("delivery.deploy_url", lambda d: d.get("delivery", {}).get("deploy_url"), "Deploy URL"),
        ]
        
        for field_path, getter, label in checks:
            value = getter(data)
            passed = bool(value) if not isinstance(value, bool) else value
            self.check("Belgelendirme ve Hazırlık", f"submission.json: {label}", passed,
                      "" if passed else f"Alan boş: {field_path}")

    def check_ai_juri(self):
        """AI_JURI.md kontrol noktaları"""
        aijuri = PROJECT_ROOT / "AI_JURI.md"
        
        if not aijuri.exists():
            self.check("Belgelendirme ve Hazırlık", "AI_JURI.md var", False, "Dosya bulunamadı")
            return
        
        content = aijuri.read_text(encoding='utf-8')
        
        sections = {
            "Problem Tanımı": "## 1) Problem Tanımı",
            "Çözüm Özeti": "## 2) Çözüm Özeti",
            "Mimari": "## 3) Mimari",
            "AI Kullanımı": "## 4) AI Kullanımı",
            "Değerlendirme Kontrol Listesi": "## 5) Değerlendirme",
            "Bilinen Sınırlar": "## 6) Bilinen Sınırlar"
        }
        
        for name, pattern in sections.items():
            found = pattern in content
            self.check("Belgelendirme ve Hazırlık", f"AI_JURI.md: {name}", found,
                      "" if found else f"Bölüm bulunamadı")

    # ========================
    # KATEGORİ 2: Teknik Gerçeklik
    # ========================

    def check_repository(self):
        """Depo bütünlüğü kontrol noktaları"""
        git_dir = PROJECT_ROOT / ".git"
        gitignore = PROJECT_ROOT / ".gitignore"
        env_example = PROJECT_ROOT / ".env.example"
        
        self.check("Teknik Gerçeklik", ".git/ var (git reposu)", git_dir.exists(),
                  "" if git_dir.exists() else "Git reposu başlatılmamış")
        
        if gitignore.exists():
            content = gitignore.read_text()
            has_env = ".env" in content
            has_nm = "node_modules" in content
            self.check("Teknik Gerçeklik", ".gitignore kapsamlı", has_env and has_nm,
                      "" if (has_env and has_nm) else ".env ve node_modules eksik")
        else:
            self.check("Teknik Gerçeklik", ".gitignore var", False, "Dosya bulunamadı")
        
        self.check("Teknik Gerçeklik", ".env.example var", env_example.exists(),
                  "" if env_example.exists() else "Dosya bulunamadı")

    def check_code_structure(self):
        """Kod yapısı kontrol noktaları"""
        src = PROJECT_ROOT / "src"
        src_readme = src / "README.md" if src.exists() else None
        tests = PROJECT_ROOT / "tests"
        docs = PROJECT_ROOT / "docs"
        
        self.check("Teknik Gerçeklik", "src/ klasörü var", src.exists(),
                  "" if src.exists() else "src klasörü bulunamadı")
        
        if src_readme and src_readme.exists():
            self.check("Teknik Gerçeklik", "src/README.md var", True)
        else:
            self.check("Teknik Gerçeklik", "src/README.md var", False, "src/README.md bulunamadı")
        
        self.check("Teknik Gerçeklik", "tests/ klasörü var", tests.exists(),
                  "" if tests.exists() else "tests klasörü bulunamadı")
        
        if tests.exists():
            test_files = list(tests.glob("*"))
            has_tests = len(test_files) > 0
            self.check("Teknik Gerçeklik", "En az 1 test dosyası", has_tests,
                      "" if has_tests else "Test dosyası bulunamadı")
        
        self.check("Teknik Gerçeklik", "docs/ klasörü var", docs.exists(),
                  "" if docs.exists() else "docs klasörü bulunamadı")

    def check_runnable(self):
        """Çalıştırılabilirlik kontrol noktaları"""
        makefile = PROJECT_ROOT / "Makefile"
        
        if makefile.exists():
            content = makefile.read_text()
            has_run = "run:" in content
            self.check("Teknik Gerçeklik", "Makefile var ve 'run' hedefi var", has_run,
                      "" if has_run else "'make run' hedefi bulunamadı")
        else:
            self.warning("Makefile bulunamadı - 'make run' komutunun çalışabilirliği doğrulanamadı")
            self.check("Teknik Gerçeklik", "Makefile var", False, "Makefile bulunamadı")

    # ========================
    # KATEGORİ 3: AI Kullanımı
    # ========================

    def check_ai_tools(self):
        """AI araçları açıklaması"""
        readme = PROJECT_ROOT / "README.md"
        
        if readme.exists():
            content = readme.read_text()
            # Model sürümü kontrolü
            has_model_version = "model:" in content or "version:" in content.lower()
            self.check("AI Kullanımı ve Şeffaflık", "Her AI aracı için model sürümü", has_model_version,
                      "" if has_model_version else "README'de TBD veya eksik sürümler var")
        
        prompts_dir = PROJECT_ROOT / "prompts"
        if prompts_dir.exists():
            prompt_files = list(prompts_dir.glob("prompt-*.md"))
            has_prompts = len(prompt_files) > 0
            self.check("AI Kullanımı ve Şeffaflık", "prompts/ klasöründe örnek prompt var", has_prompts,
                      f"Bulundu: {len(prompt_files)} prompt dosyası" if has_prompts else "Prompt dosyası bulunamadı")

    # ========================
    # KATEGORİ 4: Demo
    # ========================

    def check_demo(self):
        """Demo görselleri kontrol noktaları"""
        demo_dir = PROJECT_ROOT / "demo"
        
        self.check("Demo ve Deliverables", "demo/ klasörü var", demo_dir.exists(),
                  "" if demo_dir.exists() else "demo klasörü bulunamadı")
        
        if demo_dir.exists():
            images = list(demo_dir.glob("*.[pP][nN][gG]")) + \
                     list(demo_dir.glob("*.[jJ][pP][gG]")) + \
                     list(demo_dir.glob("*.[jJ][pP][eE][gG]")) + \
                     list(demo_dir.glob("*.[wW][eE][bB][pP]"))
            has_images = len(images) > 0
            self.check("Demo ve Deliverables", "En az 1 ekran görüntüsü", has_images,
                      f"Bulundu: {len(images)} görüntü" if has_images else "Görüntü dosyası bulunamadı")

    def run_all_checks(self):
        """Tüm kontrol noktalarını çalıştır"""
        print("🔍 Jüri Denetlemesi Başlamıştır...")
        print("-" * 60)
        
        # Kategori 1
        print("\n📋 Kategori 1: Belgelendirme ve Hazırlık")
        self.check_readme()
        self.check_submission_json()
        self.check_ai_juri()
        
        # Kategori 2
        print("📂 Kategori 2: Teknik Gerçeklik")
        self.check_repository()
        self.check_code_structure()
        self.check_runnable()
        
        # Kategori 3
        print("🤖 Kategori 3: AI Kullanımı ve Şeffaflık")
        self.check_ai_tools()
        
        # Kategori 4
        print("🎬 Kategori 4: Demo ve Deliverables")
        self.check_demo()

    def generate_report(self) -> Dict:
        """Rapor oluştur"""
        total = len(self.passed) + len(self.failed)
        passed_count = len(self.passed)
        compliance = (passed_count / total * 100) if total > 0 else 0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": "ao-hackathon-2026-mithril",
            "compliance": {
                "total_checks": total,
                "passed": passed_count,
                "failed": len(self.failed),
                "percentage": round(compliance, 1)
            },
            "categories": self.categories,
            "passed_items": self.passed,
            "failed_items": self.failed,
            "warnings": self.warnings,
            "status": "✓ PASSED" if compliance == 100 else f"⚠ {compliance}% COMPLIANCE"
        }
        
        return report

    def print_summary(self, report: Dict):
        """Özet yazdır"""
        print("\n" + "=" * 60)
        print("📊 JÜRİ DENETLEMESİ RAPORU")
        print("=" * 60)
        
        comp = report["compliance"]
        print(f"\n✓ Geçer: {comp['passed']}/{comp['total_checks']}")
        print(f"✗ Başarısız: {comp['failed']}/{comp['total_checks']}")
        print(f"📈 Uyum Oranı: {comp['percentage']}%")
        print(f"\n{report['status']}")
        
        if report["failed_items"]:
            print("\n⚠️  Eksik Kontrol Noktaları:")
            for item in report["failed_items"]:
                print(f"  {item}")
        
        if report["warnings"]:
            print("\n⚠️  Uyarılar:")
            for warning in report["warnings"]:
                print(f"  • {warning}")
        
        print("\n" + "=" * 60)
        print(f"📄 Tam rapor: {REPORT_FILE}")
        print("=" * 60)


def main():
    audit = JuryAudit()
    audit.run_all_checks()
    
    report = audit.generate_report()
    audit.print_summary(report)
    
    # Raporu JSON dosyası olarak kaydet
    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n✓ Rapor kaydedildi: {REPORT_FILE}")


if __name__ == "__main__":
    main()
