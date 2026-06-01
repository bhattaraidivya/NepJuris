from pipeline.extractor import extract_document
from pipeline.chunker import chunk_text


print("🔥 PIPELINE TEST STARTED")


# Fake catalog entry (simulate real system)
doc = {
    "file_path": "data/raw/constitution_en.pdf",
    "extraction_type": "text"
}


# STEP 1: Extract text
text = extract_document(doc)

print("\n===== EXTRACTION DONE =====")
print("Text length:", len(text))
print("\nSample text:\n")
print(text[:500])


# STEP 2: Chunk text
chunks = chunk_text(text)

print("\n===== CHUNKING DONE =====")
print("Total chunks:", len(chunks))

print("\nSample chunk:\n")
print(chunks[0] if chunks else "No chunks generated")