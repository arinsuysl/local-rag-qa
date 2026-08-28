import streamlit as st
import requests

# sayfa ayarları
st.set_page_config(page_title="RAG Asistanı", page_icon=":rocket:", layout="centered")

# başlık
st.title("🤖 Yerel RAG Doküman Asistanı")
st.markdown("Dokümanlarınıza dayalı, uydurmayan yapay zeka asistanı.")

# API Adresimiz (FastAPI'nin çalıştığı adres)
API_URL = "http://api:8000/query"

# kullanıcıdan soru alma kutusu
question = st.text_input("Sorunuzu buraya yazın:", placeholder="Örn: Güz döneminde ders ekle-bırak haftası hangi tarihler arasındadır?")

# buton
if st.button("Soru Sor", type="primary"):
    if question.strip() == "":
        st.warning("Lütfen bir soru girin.")
    else:
        with st.spinner("Kaynak taranıyor ve cevap üretiliyor..."):
            try:
                payload = {"question": question}
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success("Cevap başarıyla alındı!")
                    st.write(data.get("answer"))
                    st.divider()
                    st.info(f" Yanıt süresi: {data.get('latency_ms')} ms")
                    st.subheader("📚 Kullanılan Kaynaklar:")
                    sources = data.get("sources", [])
                    if sources:
                        for src in sources:
                            st.caption(f"🔹 **Belge:** {src.get('document')} | **Sayfa:** {src.get('page')} | **Güven Skoru:** {src.get('score')}")
                    else:
                        st.caption("Herhangi bir kaynak bulunamadı.")
                else:
                    st.error(f"Sunucu Hatası: {response.status_code}")
                    
            except Exception as e:
                st.error(f"API'ye bağlanılamadı. Hata: {str(e)}")
                st.info("İpucu: Arka planda Uvicorn (FastAPI) sunucusunun çalıştığından emin olun.")
