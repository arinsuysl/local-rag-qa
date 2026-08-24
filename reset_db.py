from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "mini_rag_documents"

try:
    client.delete_collection(collection_name=COLLECTION_NAME)
    print("Eski koleksiyon başarıyla silindi. Qdrant tertemiz!")
except Exception as e:
    print(f"Koleksiyon zaten boş veya silinmiş: {e}")