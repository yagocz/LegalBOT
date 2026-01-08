
import fitz  # PyMuPDF
import re
import json
import os
from pathlib import Path
from typing import List, Dict

# Directories
BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "data" / "pdfs"
OUTPUT_FILE = BASE_DIR / "data" / "legal_knowledge.json"

def clean_text(text: str) -> str:
    """Clean extracted text: remove multiple spaces, fixes hyphenation"""
    # Fix hyphenation at line breaks (e.g. "constitu-\nción" -> "constitución")
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    # Replace newlines with spaces for continuity
    text = text.replace('\n', ' ')
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def detect_category(text: str) -> str:
    """Simple keyword-based category detection"""
    text_lower = text.lower()
    keywords = {
        "laboral": ["trabajo", "despido", "remuneración", "empleador", "cts", "vacaciones"],
        "consumidor": ["indecopi", "consumidor", "proveedor", "producto", "servicio", "garantía"],
        "familia": ["alimentos", "divorcio", "hijo", "cónyuge", "matrimonio", "tutela"],
        "civil": ["contrato", "arrendamiento", "deudor", "acreedor", "propiedad", "compraventa"],
        "penal": ["delito", "pena", "cárcel", "fiscalía", "culpable", "sentencia"],
        "tributario": ["sunat", "tributo", "impuesto", "renta", "igv"],
        "empresas": ["sociedad", "accionista", "eirl", "sac", "directorio", "gerente"]
    }
    
    scores = {cat: 0 for cat in keywords}
    for cat, words in keywords.items():
        for word in words:
            scores[cat] += text_lower.count(word)
    
    # Return category with max score, or 'general' if all are 0
    max_cat = max(scores, key=scores.get)
    return max_cat if scores[max_cat] > 0 else "general"

def chunk_by_articles(text: str, source: str) -> List[Dict]:
    """Strategy A: Split by 'Artículo X' pattern"""
    # Regex for "Artículo 1", "Artículo 1.", "ARTÍCULO 1", "Art. 1"
    pattern = r"(?:ART[ÍI]CULO|Art\.)\s+(\d+[°º]?\.?)"
    
    parts = re.split(pattern, text, flags=re.IGNORECASE)
    
    if len(parts) < 3:
        return [] # Strategy failed
    
    chunks = []
    # parts[0] is preamble, then it alternates: [num, content, num, content...]
    # We skip preamble for now or treat as separate chunk
    
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            art_num = parts[i].strip(" .°º")
            content = clean_text(parts[i+1])
            
            if len(content) < 20: continue # Skip empty/noise
            
            chunks.append({
                "id": f"{source}-art-{art_num}",
                "ley": source.replace(".pdf", ""),
                "numero_ley": "",
                "articulo": f"Artículo {art_num}",
                "titulo": "", # Hard to extract reliably without more structure
                "texto": content,
                "libro": "",
                "categoria": detect_category(content),
                "jurisdiction": "Peru"
            })
    return chunks

def chunk_sliding_window(text: str, source: str, chunk_size=1000, overlap=100) -> List[Dict]:
    """Strategy B: Robust fallback - Sliding window"""
    chunks = []
    cleaned_text = clean_text(text)
    
    total_len = len(cleaned_text)
    start = 0
    chunk_idx = 1
    
    while start < total_len:
        end = min(start + chunk_size, total_len)
        
        # Try to find a sentence break to end the chunk cleanly
        if end < total_len:
            last_period = cleaned_text.rfind('.', start, end)
            if last_period != -1 and last_period > start + chunk_size * 0.7:
                end = last_period + 1
        
        chunk_text = cleaned_text[start:end].strip()
        
        if len(chunk_text) > 50:
            chunks.append({
                "id": f"{source}-part-{chunk_idx}",
                "ley": source.replace(".pdf", ""),
                "numero_ley": "",
                "articulo": f"Parte {chunk_idx}",
                "titulo": "Extracto del documento",
                "texto": chunk_text,
                "libro": "",
                "categoria": detect_category(chunk_text),
                "jurisdiction": "Peru"
            })
            chunk_idx += 1
            
        start = end - overlap if end < total_len else end
        
    return chunks

def process_pdfs():
    print(f"📂 Scanning {PDF_DIR}...")
    
    if not PDF_DIR.exists():
        print(f"❌ Directory not found: {PDF_DIR}")
        return
        
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No PDF files found.")
        return

    all_data = []
    
    for pdf_path in pdf_files:
        print(f"📄 Processing {pdf_path.name}...")
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            
            # Hybrid Strategy
            # 1. Try Article splitting
            chunks = chunk_by_articles(full_text, pdf_path.name)
            
            # 2. If valid chunks found (>1), use them. Else fallback to sliding window.
            # Using >1 because sometimes a document mentions "Artículo X" once in a reference, not as a header.
            if len(chunks) > 1:
                print(f"   ✅ Extracted {len(chunks)} articles.")
            else:
                print(f"   ⚠️ Structured extraction failed. Using sliding window.")
                chunks = chunk_sliding_window(full_text, pdf_path.name)
                print(f"   ✅ Created {len(chunks)} text chunks.")
            
            all_data.extend(chunks)
            doc.close()
            
        except Exception as e:
            print(f"   ❌ Error processing {pdf_path.name}: {e}")

    # Save
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n💾 Saved {len(all_data)} items to {OUTPUT_FILE}")
    
    # Category summary
    categories = {}
    for item in all_data:
        cat = item['categoria']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Summary:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}")

if __name__ == "__main__":
    process_pdfs()
