import requests
from app.rag import build_prompt 

def test_rag_system():
    fake_chunks = [
        "Öğrenciler istedikleri ülkede erasmus yapabilirler.", 
        "ÇAP yapabilmek için genel not ortalamasının en az 1.00 olması gerekir."
        ]
    question = "ÇAP yapabilmek için genel not ortalaması en az kaç olmalıdır?"

    # Deli gömleği oluşturma
    prompt = build_prompt(question, fake_chunks)

    # Arka planda ne oluştuğunu görmek için prompt'u yazdırıyoruz
    print(prompt)

    # Ollama api url'si (isteğin gideceği tam adres)
    url = "http://localhost:11434/api/generate"

    # payload = asıl hedef veri
    # pythonda bir sözlük (dictionary) requests kütüphanesi ile gönderildiğinde arka planda otomatik olarak "JSON" formatına (evrensel veri taşıma formatı) dönüşür.
    payload = {
        "model": "qwen3:4b-q4_K_M",
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(url, json=payload) # post fonksiyonu (postalamak) ile url'ye payload'u gönderiyoruz. json=payload ile payload'u json formatına çeviriyoruz.

    if response.status_code == 200: # 200 kodu her şey yolunda, işlem başarılı anlamına gelir
        result = response.json() # .json() fonksiyonu Evrensel Dilden (JSON) -> Python Diline Çevirir (tercüman)
        print(result.get("response")) # Ollama'nın resmi kullanma kılavuzunda şu kural yazar: "Eğer benden metin üretmemi isterseniz, size göndereceğim JSON paketinin içindeki asıl metni her zaman 'response' adını verdiğim bir etiketin içine koyacağım."
    else:
        print(f"Hata oluştu. Hata kodu: {response.status_code}") # .status_code fonksiyon değil , özelliktir(değişkendir). 

# bu kod pythona "bu dosyayı eğer ben terminalden çalıştırdıysam içindeki işlemleri başlat; ama başka bir dosya gelip bu dosyadan bir şeyler kopyalamak (import) isterse sessiz kal ve hiçbir şey yapma." der
if __name__ == "__main__": # __name__ = Bu etiket, dosyanın nasıl çalıştırıldığını takip etmek için kullanılır.
    test_rag_system()
# Eğer bu dosyanın gizli etiketi 'main' kelimesine eşitse (yani birisi doğrudan bu dosyayı terminalden çalıştırdıysa), o zaman içeri gir ve test_rag_system() fonksiyonunu ateşle.