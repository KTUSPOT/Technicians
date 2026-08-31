"""
generate_qr.py

Generates one printable QR code sticker per lab equipment item.
Each QR encodes ONLY the equipment_id (e.g. "EQ001") — kept simple
so the scanning app just does a Firestore lookup on that ID.

Usage:
    python generate_qr.py

Output:
    qr_codes/EQ001.png
    qr_codes/EQ002.png
    ...
    qr_codes/all_qr_codes.pdf   (printable sheet, optional)
"""

import os
import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

# Option A: hardcode your equipment list here
EQUIPMENT_LIST = [
    {"id": "EQ001", "name": "Dell Monitor 24-inch", "lab": "CS Lab 2"},
    {"id": "EQ002", "name": "HP Projector",          "lab": "CS Lab 1"},
    {"id": "EQ003", "name": "Desktop PC - Unit 5",   "lab": "CS Lab 2"},
    # Add more equipment here, or use Option B below
]

# Option B: load from a CSV instead (uncomment to use)
# CSV format expected: id,name,lab
#
# def load_from_csv(path="equipment.csv"):
#     items = []
#     with open(path, newline="", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             items.append({"id": row["id"], "name": row["name"], "lab": row["lab"]})
#     return items
#
# EQUIPMENT_LIST = load_from_csv()

OUTPUT_DIR = "qr_codes"
MAKE_PRINT_SHEET = True  # set False to skip the combined PDF sheet


# ---------------------------------------------------------------------------
# QR GENERATION
# ---------------------------------------------------------------------------

def generate_single_qr(equipment_id: str, name: str, lab: str, output_dir: str) -> str:
    """Generate one labeled QR code PNG for a single equipment item."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(equipment_id)  # encode ONLY the ID string
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Add a text label below the QR code so it's identifiable physically
    label_height = 60
    canvas = Image.new("RGB", (qr_img.width, qr_img.height + label_height), "white")
    canvas.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()

    label_line1 = f"{equipment_id}"
    label_line2 = f"{name} ({lab})"
    draw.text((10, qr_img.height + 5), label_line1, fill="black", font=font)
    draw.text((10, qr_img.height + 28), label_line2, fill="black", font=font)

    out_path = os.path.join(output_dir, f"{equipment_id}.png")
    canvas.save(out_path)
    return out_path


def generate_all(equipment_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    generated_paths = []
    for item in equipment_list:
        path = generate_single_qr(item["id"], item["name"], item["lab"], output_dir)
        generated_paths.append(path)
        print(f"Generated: {path}")
    return generated_paths


# ---------------------------------------------------------------------------
# OPTIONAL: COMBINE INTO A PRINTABLE PDF SHEET
# ---------------------------------------------------------------------------

def build_print_sheet(image_paths, output_pdf="qr_codes/all_qr_codes.pdf"):
    """
    Lays multiple QR PNGs onto a grid on A4-sized pages using reportlab,
    so you can print one sheet instead of individual images.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas as pdf_canvas
        from reportlab.lib.units import mm
    except ImportError:
        print("reportlab not installed — skipping PDF sheet. "
              "Run: pip install reportlab")
        return

    page_w, page_h = A4
    margin = 15 * mm
    cell_w = 55 * mm
    cell_h = 65 * mm
    cols = int((page_w - 2 * margin) // cell_w)
    rows = int((page_h - 2 * margin) // cell_h)
    per_page = cols * rows

    c = pdf_canvas.Canvas(output_pdf, pagesize=A4)

    for idx, img_path in enumerate(image_paths):
        pos_on_page = idx % per_page
        if pos_on_page == 0 and idx != 0:
            c.showPage()

        col = pos_on_page % cols
        row = pos_on_page // cols

        x = margin + col * cell_w
        y = page_h - margin - (row + 1) * cell_h

        c.drawImage(img_path, x, y, width=cell_w - 5 * mm, height=cell_h - 5 * mm,
                    preserveAspectRatio=True, anchor='c')

    c.save()
    print(f"\nPrintable sheet saved to: {output_pdf}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Generating QR codes for {len(EQUIPMENT_LIST)} equipment item(s)...\n")
    paths = generate_all(EQUIPMENT_LIST, OUTPUT_DIR)

    if MAKE_PRINT_SHEET:
        build_print_sheet(paths)

    print(f"\nDone. {len(paths)} QR code(s) saved in '{OUTPUT_DIR}/'.")
