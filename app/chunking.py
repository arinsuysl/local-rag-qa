def create_chunks_from_documents(documents, chunk_size=500, overlap=100):
    """
    ingest.py'den gelen sayfa sayfa metinleri alır,
    500 karakterlik parçalara böler ve her parçaya metadata ekler.
    """
    all_chunks = []

    for doc in documents:
        doc_name = doc.get("document_name", "bilinmeyen_dokuman")
        page_num = doc.get("page_number", 0)
        text = doc.get("text", "")

        # Eğer metin chunk boyutundan kısaysa doğrudan tek parça yap
        if len(text) <= chunk_size:
            chunk_id = f"{doc_name}_p{page_num}_c0"
            all_chunks.append({
                "chunk_id": chunk_id,
                "text": text,
                "metadata": {
                    "document_name": doc_name,
                    "page": page_num,
                    "chunk_id": chunk_id
                }
            })
            continue

        # Metni belirlenen chunk_size ve overlap değerlerine göre kaydırarak böl
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunk_id = f"{doc_name}_p{page_num}_c{chunk_index}"
            
            all_chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    "document_name": doc_name,
                    "page": page_num,
                    "chunk_id": chunk_id
                }
            })

            chunk_index += 1
            # Örtüşme (overlap) payı kadar geriden devam et
            start += (chunk_size - overlap)

    print(f"Toplam {len(all_chunks)} adet chunk (metin parçası) oluşturuldu.")
    return all_chunks

# Test senaryosu
if __name__ == "__main__":
    test_docs = [{
        "document_name": "erasmus.pdf",
        "page_number": 1,
        "text": "Altınbaş Üniversitesi Erasmus Programı Başvuru Yönergesi. " * 20
    }]
    chunks = create_chunks_from_documents(test_docs)
    print("Örnek Chunk Metadata:", chunks[0]["metadata"])
    print("Örnek Chunk İçeriği (İlk 100 Krk):", chunks[0]["text"][:100])