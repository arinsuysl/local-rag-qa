from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import requests
from app.rag import build_prompt
import pymupdf
import time # latency (süre ölçümü) için
import logging # loglama = kayıt tutmak
from app.embeddings import generate_embedding_for_query
from app.vector_store import search_similar_chunks

# loglama ayarlarını başlatıyoruz
logging.basicConfig(
    level=logging.INFO, # Bana INFO ve ondan daha ciddi olan (WARNING, ERROR, CRITICAL) tüm mesajları göster. Ancak kafamı şişirmemek için gereksiz DEBUG detaylarını ekrana basma
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# FastAPI uygulamamızı başlatıyoruz
app = FastAPI(
    title = "Yerel RAG API"
)

class QueryRequest(BaseModel):
    question: str

# GET /health endpoint'i
@app.get("/health")
def health_check():
    return{
        "status": "online",
        "message": "RAG API sorunsuz çalışıyor."
    }

@app.post("/query")
def ask_question(request: QueryRequest):
    start_time = time.time()
    logging.info(f"Yeni soru geldi: {request.question}")
    # 1. Kullanıcının sorusunu (query) alıp 384 boyutlu vektöre çevir
    query_vector = generate_embedding_for_query(request.question)
        
    # 2. Bu vektörü Qdrant veritabanına gönder ve anlamsal olarak en çok benzeyen 3 metin parçasını getir
    search_results = search_similar_chunks(query_vector, top_k=3)
        
    # 3. Qdrant'tan dönen o karmaşık objeleri, bizim temiz API formatımıza dönüştür
    real_sources = []
    for point in search_results:
        real_sources.append({
            "document": point.payload.get("document_name", "Bilinmeyen"),
            "page": point.payload.get("page", 0),
            "chunk_id": point.payload.get("chunk_id", "Bilinmeyen"),
            "score": round(point.score, 4),  # Vektör benzerlik skoru
            "text": point.payload.get("text", "")
        })

    context_texts = []

    for text in real_sources:
        context_texts.append(text["text"])

    prompt = build_prompt(request.question, context_texts)

    url = "http://host.docker.internal:11434/api/generate"
    payload = {"model": "qwen3:4b-q4_K_M", 
               "prompt": prompt,
               "stream": False # cevapları tek seferde alıyoruz, harf harf değil
     }
    # güvenlik ve hata yönetimi için try-except bloğu ekliyoruz
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            ai_answer = result.get("response")
            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000) # milisaniye cinsinden
            logging.info(f"Latency: {latency_ms} ms")

            clean_sources = []

            for src in real_sources:
                clean_sources.append({
                    "document": src["document"],
                    "page": src["page"],
                    "chunk_id": src["chunk_id"],
                    "score": src["score"]
                })

            return {
                "answer": ai_answer,
                "sources": clean_sources,
                "latency_ms": latency_ms
            }

        else:
            logging.error(f"Ollama Hatası: {response.status_code}")
            return {
                "error": f"Ollama API hatası: {response.status_code}"
            }

    except Exception as e:
        logging.error(f"Bağlantı hatası: {str(e)}")
        return {
            "error": "Ollama API isteği sırasında bir hata oluştu."
        }


@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    # 1. Dosyanın dijital ağırlığını (baytlarını) okuyup hafızaya alıyoruz
    file_content = await file.read()
    
    # 2. PyMuPDF ile bu baytları sanal bir PDF belgesi olarak açıyoruz
    pdf_document = pymupdf.open(stream=file_content, filetype="pdf")
    
    # 3. PDF'in kaç sayfa olduğunu buluyoruz
    num_pages = len(pdf_document)
    
    # 4. Sistemin çalıştığını kanıtlamak için şimdilik sadece 1. sayfanın metnini çekelim
    first_page_text = ""
    if num_pages > 0:
        first_page_text = pdf_document[0].get_text()
        
    return {
        "filename": file.filename,
        "total_pages": num_pages,
        "preview_text": first_page_text[:200] + "...", # Ekrana sığması için ilk 200 karakteri gösteriyoruz
        "message": "PDF başarıyla parçalandı ve okundu!"
    }