from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):

    print("\nStarting Chunking...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Total Chunks Created: {len(chunks)}")

    return chunks


if __name__ == "__main__":

    from loader import load_documents

    docs = load_documents("data")

    chunks = create_chunks(docs)

    print("\nSample Chunk Metadata:")
    print(chunks[0].metadata)

    print("\nSample Chunk:")
    print(chunks[0].page_content[:300])