"""
Playwright Visual E2E Automated Test Suite
Generates high-resolution screenshots of all views, charts, and dialogs,
and applies visual annotations (arrows, target click boxes, and pointer banners).
"""

import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

CHROMIUM_PATH = "/data/data/com.termux/files/usr/bin/chromium-browser"
HTML_PATH = "file://" + str(Path("/home/sukata/jagannatha_hora_re/web/index.html").resolve())
SCREENSHOTS_DIR = Path("/home/sukata/jagannatha_hora_re/screenshots")
ARTIFACTS_SCREENSHOTS_DIR = Path("/home/sukata/.gemini/antigravity-cli/brain/70f2f778-a7d6-4293-8970-320a72981297/screenshots")

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def draw_arrow(draw, start, end, color=(255, 50, 50), width=4):
    """Draws a bold arrow from start (x1, y1) to end (x2, y2)."""
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 16
    arrow_angle = math.pi / 6
    
    p1 = (x2 - arrow_len * math.cos(angle - arrow_angle), y2 - arrow_len * math.sin(angle - arrow_angle))
    p2 = (x2 - arrow_len * math.cos(angle + arrow_angle), y2 - arrow_len * math.sin(angle + arrow_angle))
    draw.polygon([end, p1, p2], fill=color)


def annotate_image(image_path: Path, annotations: list):
    """
    Applies annotations:
    annotation: dict(type='arrow'|'box'|'badge', start, end, label, color)
    """
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for a in annotations:
        color = a.get("color", (255, 60, 60, 255))
        if a["type"] == "box":
            box = a["box"]
            draw.rectangle(box, outline=color, width=a.get("width", 3))
            if "label" in a:
                lbl = a["label"]
                lx, ly = box[0], max(0, box[1] - 22)
                draw.rectangle([lx, ly, lx + len(lbl)*8 + 14, ly + 20], fill=color)
                draw.text((lx + 6, ly + 3), lbl, fill=(0, 0, 0, 255))
        elif a["type"] == "arrow":
            draw_arrow(draw, a["start"], a["end"], color=color, width=a.get("width", 4))
            if "label" in a:
                lbl = a["label"]
                sx, sy = a["start"]
                draw.rectangle([sx - 10, sy - 22, sx + len(lbl)*8 + 14, sy], fill=color)
                draw.text((sx - 4, sy - 18), lbl, fill=(0, 0, 0, 255))

    combined = Image.alpha_composite(img, overlay).convert("RGB")
    combined.save(image_path)
    # Also copy to artifacts dir
    shutil.copy(image_path, ARTIFACTS_SCREENSHOTS_DIR / image_path.name)


def run_playwright_e2e():
    print("🚀 Launching Playwright Chromium...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROMIUM_PATH,
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(viewport={"width": 1280, "height": 880})
        page = context.new_page()

        print(f"🌐 Navigating to {HTML_PATH}...")
        page.goto(HTML_PATH)
        page.wait_for_timeout(1000)

        # 1. Screen 1: Data Entry Dialog Modal
        print("📸 Capturing Screen 1: Modal de Entrada de Dados...")
        page.click("#btn-open-modal")
        page.wait_for_timeout(500)
        s1_path = SCREENSHOTS_DIR / "01_data_entry_dialog.png"
        page.screenshot(path=str(s1_path))
        annotate_image(s1_path, [
            {
                "type": "box",
                "box": [640, 520, 890, 560],
                "color": (59, 130, 246, 255),
                "label": "CLIQUE AQUI: Recalcular"
            },
            {
                "type": "arrow",
                "start": (980, 540),
                "end": (895, 540),
                "color": (255, 60, 60, 255),
                "label": "TRIGGER: Recalcular Mapa"
            },
            {
                "type": "box",
                "box": [340, 420, 580, 465],
                "color": (249, 226, 175, 255),
                "label": "Ayanamsa: Lahiri Chitra Paksha"
            }
        ])

        # Close Modal
        page.click("#btn-recalculate-modal")
        page.wait_for_timeout(500)

        # 2. Screen 2: Dashboard Overview & Rasi Kundali
        print("📸 Capturing Screen 2: Dashboard & Rasi Kundali...")
        s2_path = SCREENSHOTS_DIR / "02_dashboard_overview.png"
        page.screenshot(path=str(s2_path))
        annotate_image(s2_path, [
            {
                "type": "arrow",
                "start": (430, 160),
                "end": (350, 220),
                "color": (255, 60, 60, 255),
                "label": "STELLIUM: 5 Planetas em Libra"
            },
            {
                "type": "box",
                "box": [35, 375, 235, 445],
                "color": (137, 180, 250, 255),
                "label": "LAGNA: Sagitário 28°45' (Dhanus)"
            },
            {
                "type": "arrow",
                "start": (1180, 50),
                "end": (1080, 50),
                "color": (166, 227, 161, 255),
                "label": "SWISS EPHEMERIS DE405"
            }
        ])

        # 3. Screen 3: Planetary Table (Sayana vs Nirayana)
        print("📸 Capturing Screen 3: Tabela Planetária...")
        page.click("#tab-planets")
        page.wait_for_timeout(500)
        s3_path = SCREENSHOTS_DIR / "03_planetary_positions_table.png"
        page.screenshot(path=str(s3_path))
        annotate_image(s3_path, [
            {
                "type": "arrow",
                "start": (1100, 185),
                "end": (960, 185),
                "color": (255, 60, 60, 255),
                "label": "CLIQUE AQUI: Alternar Modo"
            },
            {
                "type": "box",
                "box": [20, 395, 1240, 435],
                "color": (166, 227, 161, 255),
                "label": "👑 SATURNO EXALTADO (Uccha) a 04°16' Libra"
            },
            {
                "type": "box",
                "box": [20, 435, 1240, 475],
                "color": (249, 226, 175, 255),
                "label": "💎 VÊNUS EM DOMICÍLIO (Swakshetra) a 25°48' Libra"
            }
        ])

        # 4. Screen 4: Houses & Sandhis Sripati
        print("📸 Capturing Screen 4: Casas & Sandhis...")
        page.click("#tab-houses")
        page.wait_for_timeout(500)
        s4_path = SCREENSHOTS_DIR / "04_houses_and_sandhis.png"
        page.screenshot(path=str(s4_path))
        annotate_image(s4_path, [
            {
                "type": "box",
                "box": [20, 310, 1240, 360],
                "color": (249, 226, 175, 255),
                "label": "CASA 11 (Labha Bhava) - Centro: 24°33' Libra"
            },
            {
                "type": "arrow",
                "start": (900, 220),
                "end": (760, 260),
                "color": (137, 180, 250, 255),
                "label": "Sripati Sandhis (Junções)"
            }
        ])

        # 5. Screen 5: Vimshottari Dasha Explorer
        print("📸 Capturing Screen 5: Vimshottari Dasha Explorer...")
        page.click("#tab-dashas")
        page.wait_for_timeout(500)
        s5_path = SCREENSHOTS_DIR / "05_vimshottari_dasha_timeline.png"
        page.screenshot(path=str(s5_path))
        annotate_image(s5_path, [
            {
                "type": "arrow",
                "start": (500, 190),
                "end": (450, 250),
                "color": (255, 60, 60, 255),
                "label": "MAHADASHA ATIVA: Rahu (2011-2029)"
            },
            {
                "type": "box",
                "box": [20, 425, 1240, 475],
                "color": (168, 85, 247, 255),
                "label": "⚡ SUBPERÍODO ATIVO HOJE: Rahu — Sol (17/01/2026 a 12/12/2026)"
            },
            {
                "type": "arrow",
                "start": (1100, 490),
                "end": (980, 490),
                "color": (59, 130, 246, 255),
                "label": "PRÓXIMO: Rahu — Lua (Inicia em ~30 dias)"
            }
        ])

        # 6. Screen 6: Navamsa D-9 Divisional Chart
        print("📸 Capturing Screen 6: Navamsa D-9...")
        page.click("#tab-navamsa")
        page.wait_for_timeout(500)
        s6_path = SCREENSHOTS_DIR / "06_navamsa_d9_divisional.png"
        page.screenshot(path=str(s6_path))
        annotate_image(s6_path, [
            {
                "type": "box",
                "box": [420, 280, 800, 400],
                "color": (203, 166, 247, 255),
                "label": "LUA D-9 EM LIBRA (THULA): Refinamento da Alma"
            },
            {
                "type": "arrow",
                "start": (950, 220),
                "end": (820, 250),
                "color": (166, 227, 161, 255),
                "label": "Lagna D-9 em Áries (Mesha)"
            }
        ])

        browser.close()
        print("✅ All Playwright screenshots captured, annotated and synced successfully!")


if __name__ == "__main__":
    run_playwright_e2e()
