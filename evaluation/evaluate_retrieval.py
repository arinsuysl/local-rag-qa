import json
import time
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# 1. Ayarlar ve Sabitler
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "mini_rag_documents" #
EMBEDDING_MODEL = "intfloat/multilingual-e5-small" #
EVAL_FILE = "evaluation/questions.json"

def run_evaluation():
    print("Sistem bileşenleri yükleniyor (Qdrant & Model)...")
    client = QdrantClient(url=QDRANT_URL)
    model = SentenceTransformer(EMBEDDING_MODEL)

    # 50 soruluk veri setini okuma
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        evaluation_data = json.load(f)

    total_questions = len(evaluation_data)
    hits_at_1, hits_at_3, hits_at_5 = 0, 0, 0
    total_latency = 0

    print(f"Toplam {total_questions} soru değerlendiriliyor...\n")

    for item in evaluation_data:
        question = item["question"]
        expected_doc = item["expected_document"] #
        
        # E5 modeli kuralı: Sorgulara 'query: ' ön eki eklenmelidir
        query_text = f"query: {question}"
        
        start_time = time.time()
        
        # 1. Soruyu vektöre (embedding) çevir
        query_vector = model.encode(query_text).tolist()
        
        # 2. Qdrant'ta Top-5 araması yap (semantic search)
        search_response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=5
        )
        # Gelen cevabın içinden sadece bulduğu sonuçları (points) alıyoruz
        search_results = search_response.points
        
        # Süreyi hesapla
        latency = time.time() - start_time
        total_latency += latency

        # 3. Gelen sonuçların doküman isimlerini sırasıyla listele
        # Geliştirme aşamasında 'document_name' metadata alanını kullandığını varsayıyoruz[cite: 1]
        retrieved_docs = [hit.payload.get("document_name") for hit in search_results]

        # 4. Metrikleri Kontrol Et (Recall)[cite: 1]
        if expected_doc in retrieved_docs[:1]:
            hits_at_1 += 1
        if expected_doc in retrieved_docs[:3]:
            hits_at_3 += 1
        if expected_doc in retrieved_docs[:5]:
            hits_at_5 += 1

    # Sonuç Raporunu Ekrana Yazdır
    print("-" * 40)
    print("🎯 RETRIEVAL DEĞERLENDİRME SONUÇLARI 🎯")
    print("-" * 40)
    print(f"Toplam Test Edilen Soru: {total_questions}")
    print(f"Recall@1:  {hits_at_1 / total_questions:.2f}  ({hits_at_1}/{total_questions})")
    print(f"Recall@3:  {hits_at_3 / total_questions:.2f}  ({hits_at_3}/{total_questions})")
    print(f"Recall@5:  {hits_at_5 / total_questions:.2f}  ({hits_at_5}/{total_questions})")
    print(f"Ortalama Gecikme (Latency): {total_latency / total_questions:.3f} saniye")
    print("-" * 40)

if __name__ == "__main__":
    run_evaluation()