"""Recover publisher-authored PDFs for the queued classic El Grande/Dune games."""
from pathlib import Path
import hashlib
import json
import re
import fitz
import requests

base = Path(__file__).parent / "source-discovery"
sources = {
    "el-grande-publisher-rules": "https://board-game-rules.com/wp-content/uploads/2025/01/el-grande_Official-Rules.pdf",
    "dune-imperium-rules": "https://d19y2ttatozxjp.cloudfront.net/pdfs/DUNE_IMPERIUM_Rules_2020_10_26.pdf",
    "dune-imperium-uprising-rules": "https://dwd-web.s3.us-west-2.amazonaws.com/pdfs/DUNE_IMPERIUM_UPRISING_Main_Rulebook_23-10-12.pdf",
    "dune-imperium-official-faq-2025-01-13": "https://d19y2ttatozxjp.cloudfront.net/pdfs/DUNE_IMPERIUM_FAQ_25-1-13.pdf",
    "dune-imperium-uprising-supplements": "https://d19y2ttatozxjp.cloudfront.net/pdfs/DUNE_IMPERIUM_UPRISING_Rules_Supplements_23-10-12.pdf",
}
results = {}
for name, url in sources.items():
    try:
        response = requests.get(url, timeout=45)
        response.raise_for_status()
        assert response.content.startswith(b"%PDF"), "Response is not a PDF"
        path = Path("source_pdfs") / f"{name}.pdf"
        if path.exists():
            assert path.read_bytes() == response.content, "Existing PDF differs; preserve it"
        else:
            path.write_bytes(response.content)
        document = fitz.open(path)
        extracted = "\n".join(f"--- PDF Page {i+1} ---\n" + page.get_text(sort=True) for i, page in enumerate(document))
        text_path = base / f"{name}.txt"
        text_path.write_text(extracted)
        results[name] = {"url": url, "pdf": str(path.resolve()), "text": str(text_path.resolve()), "pages": len(document), "pdf_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "text_sha256": hashlib.sha256(text_path.read_bytes()).hexdigest()}
    except Exception as error:
        results[name] = {"url": url, "error": str(error)}
    print(json.dumps({name: results[name]}), flush=True)
    (base / "queued-source-provenance.json").write_text(json.dumps(results, indent=2) + "\n")

try:
    response = requests.get("https://direwolfdigital.com/dune-imperium/resources/", timeout=35)
    response.raise_for_status()
    (base / "dire-wolf-resources.html").write_text(response.text)
    print("Publisher resource index saved; the assigned English PDFs were located in its links.")
except Exception as error:
    print("Publisher resource index:", str(error))
