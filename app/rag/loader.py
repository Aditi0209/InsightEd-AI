import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader
)


def get_loader(file_path):

    if file_path.endswith(".pdf"):
        return PyPDFLoader(file_path)

    elif file_path.endswith(".docx"):
        return UnstructuredWordDocumentLoader(file_path)

    elif file_path.endswith(".txt"):
        return TextLoader(file_path)

    elif file_path.endswith(".md"):
        return UnstructuredMarkdownLoader(file_path)

    return None


def load_documents(data_path):

    documents = []

    total_files = 0

    supported_formats = (
        ".pdf",
        ".docx",
        ".txt",
        ".md"
    )

    for subject in os.listdir(data_path):

        subject_path = os.path.join(data_path, subject)

        if not os.path.isdir(subject_path):
            continue

        for file in os.listdir(subject_path):

            if not file.endswith(supported_formats):
                continue

            total_files += 1

            print(f"Loading: {subject}/{file}")

            file_path = os.path.join(subject_path, file)

            loader = get_loader(file_path)

            if loader is None:
                continue

            docs = loader.load()

            chapter = os.path.splitext(file)[0]

            file_type = os.path.splitext(file)[1].replace(".", "")

            for doc in docs:

                doc.metadata["subject"] = subject
                doc.metadata["chapter"] = chapter
                doc.metadata["file_type"] = file_type

            documents.extend(docs)

    print("\n" + "=" * 50)
    print(f"Total Files Loaded: {total_files}")
    print(f"Total Pages/Documents Loaded: {len(documents)}")
    print("=" * 50)

    return documents


if __name__ == "__main__":

    docs = load_documents("data")

    print("\nSample Metadata:")
    print(docs[0].metadata)

    print("\nSample Content:")
    print(docs[0].page_content[:300])