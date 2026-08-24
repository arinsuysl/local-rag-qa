from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Qdrant'a bağlan
client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "mini_rag_documents"

print("--- YENİ KOLEKSİYON OLUŞTURULUYOR ---")

# Koleksiyonu 384 boyut (E5 modeline uygun) ve Cosine kuralıyla sıfırdan kuruyoruz
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

print(f"'{COLLECTION_NAME}' koleksiyonu başarıyla ve tertemiz bir şekilde oluşturuldu!")