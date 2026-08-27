from qdrant_client import QdrantClient
from rank_bm25 import BM25Okapi
import numpy as np
import re

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "mini_rag_documents"

print("Vektör veritabanından dokümanlar çekiliyor...")
records, _ = client.scroll(
    collection_name=COLLECTION_NAME, 
    limit=2000, 
    with_payload=True
)

corpus = [record.payload["text"] for record in records]
metadata = [record.payload for record in records]

# 1. Türkçe Dolgu Kelimeleri (Stop-words) Listesi
STOP_WORDS = {"hangi", "tarihler", "arasında", "planlanmıştır", "ne", "zaman", "bir", "ve", "ile", "için", "bu", "şu", "o", "da", "de", "mı", "mi", "daha", "en"}

# 2. Metin Temizleme Fonksiyonu
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Noktalama işaretlerini kaldır
    words = text.split()
    return [word for word in words if word not in STOP_WORDS]

# Veritabanını temizle ve indeksle
tokenized_corpus = [clean_text(doc) for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)

# 3. İnatçı Soruyu Temizle ve Test Et
query = "Üniversitenin mezuniyet töreni hangi tarihler arasında planlanmıştır?"
print(f"\nSoru: {query}")

tokenized_query = clean_text(query)
print(f"Filtrelenmiş Soru Kelimeleri: {tokenized_query}")

# 4. Sonuçları Getir
doc_scores = bm25.get_scores(tokenized_query)
top_indices = np.argsort(doc_scores)[::-1][:3]

print("\n🎯 GELİŞMİŞ BM25 ARAMA SONUÇLARI 🎯")
print("-" * 50)
for i in top_indices:
    doc_name = metadata[i].get('document_name', 'Bilinmiyor')
    print(f"Doküman: {doc_name} | Skor: {doc_scores[i]:.2f}")
    print(f"İçerik Önizleme: {corpus[i][:100]}...\n")