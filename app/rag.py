def build_prompt(question: str, context_chunks: list) -> str: # çıktı string
    context_text = "\n\n".join(context_chunks) # chunkları aralarında birer satır (\n\n) olacak şekilde paragraf haline getirme
    prompt = f"""SİSTEM:
Sen sadık bir doküman asistanısın. Yalnızca aşağıda verilen KAYNAKLAR bölümündeki metinlere dayanarak cevap ver.
Eğer sorunun cevabı verilen kaynaklarda yoksa, kesinlikle bilgi uydurma ve kendi hafızanı kullanma. Sadece şu cümleyi söyle: "Bu bilgi verilen dokümanlarda bulunamadı."
Cevabın sonunda kullandığın kaynakları belirt.

KAYNAKLAR:
{context_text}

SORU:
{question}"""

    return prompt