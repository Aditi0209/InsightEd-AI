import time

from loader import load_documents
from chunker import create_chunks
from vs_qdrant import create_vector_store


start = time.time()

print("\nSTEP 1: Loading Documents")

documents = load_documents("data")

print(f"\nLoaded {len(documents)} pages")

print("\nSTEP 2: Chunking")

chunks = create_chunks(documents)

print(f"\nCreated {len(chunks)} chunks")

print("\nSTEP 3: Creating Vector Database")

create_vector_store(chunks)

end = time.time()

print("\n" + "=" * 50)
print("INGESTION COMPLETE")
print(f"Total Time: {end-start:.2f} seconds")
print("=" * 50)