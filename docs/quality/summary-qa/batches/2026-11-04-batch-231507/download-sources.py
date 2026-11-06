"""Download the publisher-authored source documents missing from this QA batch."""
from pathlib import Path
import hashlib
import json
import fitz
import requests

base = Path(__file__).parent / "source-discovery"
base.mkdir(exist_ok=True)
sources = {
    "dead-last-rules-v2": {
        "url": "https://cs.uwaterloo.ca/~dtompkin/archive/dtlib/base/Dead%20Last.pdf",
        "authority": "Smirk & Dagger publisher-authored booklet, university-hosted mirror; page 4 includes Rules 2.0 zero-survivor erratum",
    },
    "obsession-universal-rules": {
        "url": "https://www.dropbox.com/scl/fi/7nubc87hf9fxrt41nhhqd/Obsession_Rulebook_8.5x11_20251217-Reduced.pdf?dl=1&rlkey=tzgpw5zjx2sm9he4ijm1pgpka&st=bfceqfr0",
        "authority": "Kayenta Games publisher download linked from https://www.kayentapublishing.com/",
    },
    "obsession-corrigendum-1.0": {
        "url": "https://www.dropbox.com/scl/fi/lhjravzt68s6s8pnd07gy/Universal-Rules-Corrigendum-1.0-10.6.2026.pdf?dl=1&rlkey=hjg4bp4mhk3subhoxat2e9049&st=oql9k58v",
        "authority": "Kayenta Games publisher download linked from https://www.kayentapublishing.com/",
    },
}
results = {}
for name, info in sources.items():
    try:
        response = requests.get(info["url"], timeout=50)
        response.raise_for_status()
        content = response.content
        if not content.startswith(b"%PDF"):
            raise ValueError("Response is not a PDF")
        pdf = base / f"{name}.pdf"
        pdf.write_bytes(content)
        document = fitz.open(pdf)
        extracted = "\n".join(
            f"--- Page {i + 1} ---\n" + page.get_text(sort=True)
            for i, page in enumerate(document)
        )
        text_path = base / f"{name}.txt"
        text_path.write_text(extracted)
        results[name] = {
            **info,
            "pdf": str(pdf.resolve()),
            "text": str(text_path.resolve()),
            "pages": len(document),
            "bytes": len(content),
            "pdf_sha256": hashlib.sha256(content).hexdigest(),
            "text_sha256": hashlib.sha256(text_path.read_bytes()).hexdigest(),
        }
    except Exception as error:
        results[name] = {**info, "error": str(error)}
    print(json.dumps({name: results[name]}), flush=True)
    (base / "provenance.json").write_text(json.dumps(results, indent=2) + "\n")
