from qdrant_client import QdrantClient

# Qdrant'a doğrudan bağlanıyoruz
client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "mini_rag_documents"

# Hata payını sıfırlamak için doğrudan PDF'te yazan spesifik kelimeleri arıyoruz
aranan_kelimeler = ["heykel", "sinema", "klasik batı müziği"]

print("--- QDRANT VERİTABANI İÇİNDE HAM METİN ARAMASI ---")

# Veritabanındaki ilk 1000 chunk'ı vektörsüz (sadece metin olarak) çekiyoruz
kayitlar, _ = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=1000,
    with_payload=True,
    with_vectors=False
)

bulunan_chunklar = []

# Çekilen tüm chunk'ların içinde kelime kelime arama yapıyoruz
for kayit in kayitlar:
    metin = kayit.payload.get("text", "").lower()
    
    # Eğer aradığımız kelimelerden herhangi biri metinde geçiyorsa yakala
    if any(kelime in metin for kelime in aranan_kelimeler):
        bulunan_chunklar.append(kayit)

print(f"Aranan kelimeler toplam {len(bulunan_chunklar)} farklı parçada (chunk) bulundu!\n")

# Bulunan sonuçları ekrana yazdır
for i, kayit in enumerate(bulunan_chunklar, 1):
    print(f"=== BULGU {i} ===")
    print(f"Metin: {kayit.payload.get('text')}")
    print(f"Hangi Sayfa/Dosya: {kayit.payload.get('metadata')}\n")