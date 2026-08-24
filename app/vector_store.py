from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid

# Qdrant'a bağlanıyoruz (Docker üzerinde 6333 portundan yayın yapıyor)
client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "mini_rag_documents"

def init_vector_db():
    """
    Koleksiyon yoksa, e5-small modeline uygun (384 boyut, Cosine metrik) yeni bir koleksiyon oluşturur.
    """
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=384,  # multilingual-e5-small modelimizin ürettiği boyut
                distance=models.Distance.COSINE
            )
        )
        print(f"'{COLLECTION_NAME}' koleksiyonu Qdrant üzerinde başarıyla oluşturuldu.")
    else:
        print(f"'{COLLECTION_NAME}' koleksiyonu sistemde zaten mevcut.")

def upsert_chunks_to_qdrant(chunks):
    """
    Chunk ve embedding listesini alır, payload (metadata + text) ile birlikte Qdrant'a kaydeder.
    """
    points = []
    for i, chunk in enumerate(chunks):
        # Qdrant'a göndereceğimiz paketi (payload) hazırlıyoruz
        # Hem metadataları (sayfa, dosya adı) alıyoruz hem de asıl metni (text) ekliyoruz
        payload_data = chunk["metadata"].copy()
        payload_data["text"] = chunk["text"]
        
        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()),  # Her parçaya evrensel olarak benzersiz bir ID atar
                vector=chunk["embedding"],
                payload=payload_data
            )
        )
    
    # Qdrant'a toplu halde yüklüyoruz
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"Başarılı: {len(points)} adet vektör Qdrant'a yüklendi.")

def search_similar_chunks(query_vector, top_k=5):
    """
    Soru vektörüne anlamsal olarak en çok benzeyen Top-K adet chunk'ı getirir.
    """
    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    )
    # Yeni versiyonda sonuçlar 'points' isimli bir liste içinde dönüyor
    return search_result.points

# Basit bir bağlantı testi
if __name__ == "__main__":
    init_vector_db()