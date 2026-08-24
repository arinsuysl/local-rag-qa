Büyük Dil Modellerinde (LLM) Quantization (Sıkıştırma) Analizi
Quantization Neden VRAM/RAM Kullanımını Düşürür?
Büyük Dil Modelleri, milyarlarca "parametre" (ağırlık) adı verilen sayısal değerden oluşur. Standart bir model eğitildiğinde bu değerler 32-bit (FP32) veya 16-bit (FP16/BF16) kayan noktalı (float) sayılar olarak belleğe kaydedilir.

Quantization işlemi, bu parametreleri matematiksel olarak yuvarlayarak daha düşük bit değerlerine sahip tam sayılara (8-bit, 4-bit vb.) dönüştürür. Tıpkı yüksek çözünürlüklü bir RAW fotoğrafı, görsel kaliteyi çok bozmadan JPEG formatına sıkıştırmak gibidir. Her bir parametrenin bellekte kapladığı veri boyutu küçüldüğünde, modelin tamamının ihtiyaç duyduğu toplam VRAM/RAM miktarı da doğrudan (bazen 4'te 1 oranında) azalır.

Formatlar Arasındaki Temel Farklar
FP16 / BF16 (16-bit Kayan Nokta - Float):

Özellik: Modelin "saf" veya orijinaline en yakın halidir. BF16 (Brain Float 16), daha geniş bir sayısal aralık sunarken; FP16 daha yüksek hassasiyet sunar.

Kullanım: En yüksek zeka ve kaliteyi arayan, yeterli VRAM'e (örneğin 24GB+) sahip sistemler veya bulut sunucuları için temel standarttır.

Q8_0 (8-bit Quantization):

Özellik: Parametrelerin 8-bitlik tam sayılara (Integer) yuvarlandığı formattır.

Kullanım: FP16'ya göre bellek kullanımını tam yarı yarıya düşürür. Modelin mantıksal yeteneklerinde ölçülebilir bir kayıp neredeyse hiç yaşanmaz. Sunucu kalitesine çok yakın sonuçlar elde etmek için "güvenli liman"dır.

Q4_K_M (4-bit K-Quant Medium):

Özellik: GGUF altyapısında kullanılan çok akıllı, asimetrik bir sıkıştırma yöntemidir. Modelin çıktısını en çok etkileyen kritik (attention) katmanlarını daha yüksek bitlerde (örneğin 6-bit) bırakırken, önemsiz katmanları agresif bir şekilde 4-bite sıkıştırır.

Kullanım: Son kullanıcı bilgisayarları için "altın standarttır". Devasa bellek tasarrufu sağlar.

Doğruluk (Accuracy) ve Hız (Speed) Üzerindeki Etkileri
1. Doğruluğa Etkisi (Accuracy):
Sıkıştırma oranı arttıkça (bit düştükçe), yuvarlama hatalarından dolayı modelin kelime dağarcığında ve mantıksal çıkarım yeteneğinde ufak düşüşler başlar.

FP16/BF16 ve Q8_0: Çıktı kalitesinde ve mantıksal testlerde (kod yazma, karmaşık matematik) neredeyse sıfır kayıp yaşanır.

Q4_K_M: Günlük sohbetlerde ve metin özetlemelerinde orijinal modelden farksızdır. Ancak çok ince teknik detaylarda veya uzun bağlamlı mantık zincirlerinde hafif halüsinasyonlara (yanlış bilgi üretmeye) meyledebilir. Yine de kayıp/kazanç oranı en yüksek (optimum) formattır.

2. Hıza Etkisi (Speed - Tokens Per Second):
Büyük Dil Modelleri çalışırken genellikle işlemci gücünden ziyade bellek bant genişliğine (memory bandwidth) takılırlar (darboğaz yaşarlar).

Quantization, veriyi küçülttüğü için RAM/VRAM'den işlemciye veri aktarımı çok daha hızlı gerçekleşir.

Eğer ekran kartınızın veya işlemcinizin bellek hızı yavaşsa, Q4_K_M formatındaki bir model, FP16'ya göre çok daha yüksek bir hızda (saniyede üretilen kelime sayısı) çalışacaktır. Sıkıştırılmış veriyi anlık olarak açmak (dequantize) ekstra ufak bir işlemci gücü istese de, veri yolundan kazanılan devasa zaman bu açığı fazlasıyla kapatır.
