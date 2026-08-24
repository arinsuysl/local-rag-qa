import time
from app.embeddings import embedding_model
from app.vector_store import search_similar_chunks

# 1. Kendi PDF'lerinin içeriğine uygun, cevabı belgelerde olan bir soru yaz
soru = "Sanat başarı bursu kimlere verilir?"

# E5 modeli kuralı: Arama yaparken başına 'query: ' ekliyoruz
hazirlanan_soru = f"query: {soru}"
soru_vektoru = embedding_model.encode([hazirlanan_soru])[0].tolist()

print(f"SORU: '{soru}'\n")

# 2. Top-K Testleri (K=3, K=5 ve K=10 için süre ve sonuç ölçümü)
for k_degeri in [3, 5, 10]:
    print(f"=== TOP-K = {k_degeri} TESTİ ===")
    
    baslangic_zamani = time.time()
    # Qdrant'tan belirlediğimiz K değeri kadar sonuç istiyoruz
    sonuclar = search_similar_chunks(soru_vektoru, top_k=k_degeri)
    bitis_zamani = time.time()
    
    gecen_sure_ms = (bitis_zamani - baslangic_zamani) * 1000
    
    print(f"Arama Süresi (Latency): {gecen_sure_ms:.2f} milisaniye")
    print(f"Getirilen Sonuç Sayısı: {len(sonuclar)}")
    
    if sonuclar:
        # En yüksek skorlu 1. sonucu göster
        print(f"1. Sıra (En Alakalı) - Skor {sonuclar[0].score:.4f}:")
        print(f"   Metin: {sonuclar[0].payload.get('text', '')[:120]}...\n")
        
        # Eğer K kadar sonuç döndüyse, en sonuncu (en düşük skorlu) sonucu da göster
        if len(sonuclar) > 1:
            son_sira = len(sonuclar)
            print(f"{son_sira}. Sıra (En Az Alakalı) - Skor {sonuclar[-1].score:.4f}:")
            print(f"   Metin: {sonuclar[-1].payload.get('text', '')[:120]}...")
            
    print("-" * 50 + "\n")