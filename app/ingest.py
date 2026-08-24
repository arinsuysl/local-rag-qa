import os
import pymupdf
from app.embeddings import embedding_model
from app.vector_store import upsert_chunks_to_qdrant

# Yönergedeki hedef klasör yapısı
PDF_KLASORU = "sample_documents"

def pdf_oku_ve_parcala(klasor_yolu, chunk_size=800, overlap=150):
    tum_chunklar = []
    
    # Klasördeki tüm .pdf dosyalarını listele
    pdf_dosyalari = [f for f in os.listdir(klasor_yolu) if f.endswith('.pdf')]
    
    if not pdf_dosyalari:
        print(f"Hata: '{klasor_yolu}' klasöründe PDF bulunamadı!")
        return tum_chunklar

    for dosya_adi in pdf_dosyalari:
        dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
        print(f"İşleniyor: {dosya_adi}...")
        
        doc = pymupdf.open(dosya_yolu)
        
        for sayfa_no, sayfa in enumerate(doc, start=1):
            metin = sayfa.get_text()
            if not metin.strip():
                continue
            
            baslangic = 0
            while baslangic < len(metin):
                bitis = baslangic + chunk_size
                chunk_metni = metin[baslangic:bitis].strip()
                
                if chunk_metni:
                    chunk_verisi = {
                        "text": chunk_metni,
                        "metadata": {
                            "document_name": dosya_adi,
                            "page": sayfa_no,
                            "chunk_id": f"{dosya_adi}_p{sayfa_no}_c{baslangic}"
                        }
                    }
                    tum_chunklar.append(chunk_verisi)
                
                baslangic += (chunk_size - overlap)
        
        doc.close()
        
    return tum_chunklar

if __name__ == "__main__":
    print("--- ADIM 1: PDF OKUMA VE PARÇALAMA ---")
    chunk_listesi = pdf_oku_ve_parcala(PDF_KLASORU)
    print(f"Toplam {len(chunk_listesi)} adet parça (chunk) oluşturuldu.\n")
    
    if chunk_listesi:
        print("--- ADIM 2: E5 MODELİ İLE VEKTÖR OLUŞTURMA ---")
        metinler = [chunk["text"] for chunk in chunk_listesi]
        
        # E5 model kuralı: Dokümanlar 'passage: ' ön ekiyle gömülür
        hazirlanan_metinler = [f"passage: {metin}" for metin in metinler]
        vektorler = embedding_model.encode(hazirlanan_metinler).tolist()
        
        for i, chunk in enumerate(chunk_listesi):
            chunk["embedding"] = vektorler[i]
            
        print("--- ADIM 3: QDRANT VERİTABANINA YÜKLEME ---")
        upsert_chunks_to_qdrant(chunk_listesi)
        
        print("\nTüm dokümanlar başarıyla Qdrant'a indekslendi!")