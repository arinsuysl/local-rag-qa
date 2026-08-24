from app.chunking import create_chunks_from_documents
from app.embeddings import generate_embeddings_for_chunks, embedding_model
from app.vector_store import upsert_chunks_to_qdrant, search_similar_chunks

# 1. Örnek bir doküman metni oluşturuyoruz
test_docs = [{
    "document_name": "erasmus_test.pdf",
    "page_number": 1,
    "text": "Altınbaş Üniversitesi Erasmus başvuru şartları: Öğrencilerin genel not ortalaması (GANO) en az 2.20 olmalıdır. Başvurular online sistem üzerinden yapılır."
}]

# 2. Metni chunk'lara bölüyoruz
print("\n--- 1. ADIM: Chunk İşlemi ---")
chunks = create_chunks_from_documents(test_docs)

# 3. Chunk'ları 384 boyutlu vektörlere dönüştürüyoruz
print("\n--- 2. ADIM: Embedding Üretimi ---")
embedded_chunks = generate_embeddings_for_chunks(chunks)

# 4. Vektörleri metadata ile birlikte Qdrant'a yüklüyoruz (Upsert)
print("\n--- 3. ADIM: Qdrant'a Kayıt ---")
upsert_chunks_to_qdrant(embedded_chunks)

# 5. CLI Üzerinden Arama Testi (Semantic Search)
print("\n--- 4. ADIM: Arama (Retrieval) Testi ---")
soru = "Erasmus başvurusu için not ortalaması kaç olmalıdır?"
print(f"Sorulan Soru: '{soru}'")

# Yönerge kuralı: e5-small modelinde sorgulara 'query: ' ön eki eklenmelidir
hazirlanan_soru = f"query: {soru}" 
soru_vektoru = embedding_model.encode([hazirlanan_soru])[0].tolist()

# Vektörel arama yapıyoruz (En iyi 1 sonucu getir)
sonuclar = search_similar_chunks(soru_vektoru, top_k=1)

print("\n--- BULUNAN EN ALAKALI SONUÇ ---")
for sonuc in sonuclar:
    print(f"Benzerlik Skoru: {sonuc.score:.4f}")
    print(f"Kaynak Dosya: {sonuc.payload['document_name']} (Sayfa {sonuc.payload['page']})")
    print(f"Bulunan Metin: {sonuc.payload['text']}")