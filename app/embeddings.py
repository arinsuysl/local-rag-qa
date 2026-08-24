from sentence_transformers import SentenceTransformer

# 384 boyutlu vektör üreten modelimizi yüklüyoruz
MODEL_NAME = "intfloat/multilingual-e5-small"
print(f"Embedding modeli yükleniyor: {MODEL_NAME}...")
embedding_model = SentenceTransformer(MODEL_NAME)

def generate_embeddings_for_chunks(chunks):
    """
    Gelen chunk listesini alır, E5 kuralına göre 'passage: ' ön eki ekler
    ve 384 boyutlu vektörlerini üretir.
    """
    # E5 model kuralı: Doküman parçalarının başına 'passage: ' eklenmelidir
    prepared_texts = [f"passage: {chunk['text']}" for chunk in chunks]
    
    # Vektör üretimi (HuggingFace üzerinden otomatik indirilir ve hesaplanır)
    embeddings = embedding_model.encode(prepared_texts, show_progress_bar=True)

    # Üretilen vektörleri ilgili chunk objesinin içine ekliyoruz
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist() # Numpy array'ini listeye çeviriyoruz

    print(f"Başarılı: {len(chunks)} adet chunk için 384 boyutlu vektörler üretildi.")
    return chunks

def generate_embedding_for_query(query: str) -> list:
    """
    Kullanıcının sorusunu alır, E5 kuralına göre 'query: ' ön eki ekler
    ve Qdrant'ta arama yapmak üzere tek bir vektör (liste) döndürür.
    """
    prepared_query = f"query: {query}"
    # Qdrant list formatında beklediği için tolist() yapıyoruz
    return embedding_model.encode(prepared_query).tolist()

# Test senaryosu
if __name__ == "__main__":
    sample_chunks = [{
        "chunk_id": "test_p1_c0",
        "text": "Altınbaş Üniversitesi Erasmus değişim programı başvuru şartları.",
        "metadata": {"document_name": "test.pdf", "page": 1, "chunk_id": "test_p1_c0"}
    }]
    
    result = generate_embeddings_for_chunks(sample_chunks)
    vector = result[0]["embedding"]
    print(f"Üretilen Vektör Boyutu: {len(vector)}") # 384 olmalı
    print(f"Vektörden Örnek Sayılar (İlk 5): {vector[:5]}")