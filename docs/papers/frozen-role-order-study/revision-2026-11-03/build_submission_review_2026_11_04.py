"""Rebuild *review* Word/PDF from public 2026-11-04 Markdown and existing figures.

Never reads video, model, labels, caches or Windows experimental assets.
No upload or automatic submission; final target-journal template still requires
author-driven visual QA and real author metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "manuscript-submission-review-2026-11-04.md"
STEM = "manuscript-submission-review-2026-11-04"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=HERE, check=True, timeout=180)


def qa_source(text: str) -> dict:
    chinese = re.search(r"^\*\*摘要\*\*　(.+)$", text, re.M)
    english = re.search(r"^\*\*Abstract\*\*　(.+)$", text, re.M)
    refs = [int(x) for x in re.findall(r"^\[(\d+)\] ", text, re.M)]
    assert chinese and 200 <= len(chinese.group(1)) <= 300
    assert english and len(english.group(1).split()) >= 100
    assert refs == list(range(1, 12)), refs
    for phrase in ("-1.52", "17.67%", "12.33%", "50Salads", "VIDHALLUC"):
        # negative sign in manuscript discussion can use Unicode minus
        if phrase == "-1.52":
            assert "-1.52" in text or "−1.52" in text
        else:
            assert phrase in text
    for fig in ("paired-seeds.png", "conditional-intervals.png"):
        assert (HERE / "figures" / fig).is_file(), fig
    return {"chinese_abstract_chars": len(chinese.group(1)),
            "english_abstract_words": len(english.group(1).split()),
            "formally_published_references": len(refs)}


def make() -> dict:
    assert SOURCE.is_file()
    src = SOURCE.read_text(encoding="utf-8")
    audit = qa_source(src)
    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc is required")
    from docx import Document
    from docx.shared import Pt
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    output_docx = HERE / f"{STEM}.docx"
    output_pdf = HERE / f"{STEM}.pdf"
    if output_docx.exists() or output_pdf.exists():
        raise FileExistsError("Review deliverables already exist; do not overwrite")
    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)
        intermediate = tdir / "draft.docx"
        cmd = ["pandoc", str(SOURCE), "--from", "markdown+tex_math_dollars",
               "--to", "docx", "--standalone", "--resource-path", str(HERE),
               "-o", str(intermediate)]
        # Old Word is used for reusable styles, never for obsolete content.
        reference_doc = HERE / "manuscript.docx"
        if reference_doc.exists():
            cmd += ["--reference-doc", str(reference_doc)]
        run(cmd)
        doc = Document(intermediate)
        assert len(doc.tables) == 2, f"expected two editable tables, got {len(doc.tables)}"
        assert len(doc.inline_shapes) >= 2, "expected the two published summary figures"
        if "Normal" in doc.styles:
            st = doc.styles["Normal"]
            st.font.size = Pt(10.5)
            st.font.name = "Liberation Serif"
            f = st.element.get_or_add_rPr().find(qn("w:rFonts"))
            if f is None:
                f = OxmlElement("w:rFonts")
                st.element.get_or_add_rPr().insert(0, f)
            f.set(qn("w:eastAsia"), "Noto Serif CJK SC")
        doc.core_properties.author = ""
        doc.core_properties.last_modified_by = ""
        doc.core_properties.title = "冻结特征视频问答中的角色差分效应（投稿审阅版）"
        doc.save(output_docx)
    audit.update({"docx": output_docx.name,
                  "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  "editable_tables": 2,
                  "embedded_figures": len(doc.inline_shapes),
                  "review_copy_not_official_template": True})
    if shutil.which("libreoffice"):
        with tempfile.TemporaryDirectory() as td:
            run(["libreoffice", "-env:UserInstallation=file:///" + td.replace("\\", "/"),
                 "--headless", "--convert-to", "pdf", "--outdir", td,
                 str(output_docx)])
            pdf_tmp = Path(td) / (output_docx.stem + ".pdf")
            if pdf_tmp.exists():
                shutil.copyfile(pdf_tmp, output_pdf)
                audit["pdf"] = output_pdf.name
            else:
                audit["pdf"] = "NOT_GENERATED"
    else:
        audit["pdf"] = "NOT_GENERATED"
    (HERE / "build-submission-review-receipt.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-review-only", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(make(), ensure_ascii=False, indent=2))
