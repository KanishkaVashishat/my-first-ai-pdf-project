from pdf_utils import chunk_text

sample = "Hello " * 300

chunks = chunk_text(sample)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {len(chunk)} characters")