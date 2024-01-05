# Binance Square'den alınmış haberlerin Olumlu yada olumsuz tahmini

## Genel Bakış

Bu proje, bir haber makalesi veri kümesi üzerinde duygu analizi uygulayan üç farklı makine öğrenimi modelini içerir: Naive Bayes, Destek Vektör Makinesi (SVM) ve Karar Ağacı. Amacımız, haber makalelerinin içeriğine dayanarak duygu (yeni etiketi) tahmin etmektir.

## Kullanılan Kütüphaneler

-Pandas<br/>
-NumPy<br/>
-Scikit-learn<br/>
-Pyplot<br/>
-Simplemma <br/>
-Binance <br/>
-BeautifulSoup <br/>

# VERİ SETİ'NİN OLUŞTURULMASI

Binance square'den web scarping yaparak veriler selenium kutuphanesi ile çekilmiştir. Bu verileri bir excel dosyasına kaydettik.Bazı verilerde etiketlenmiş coin isimleri'de vardı bu bizim işimize etiketleme kısmında yaradı.

<br/>
Veriler dinamik olarak binance'da yüklendiği için beatifulsoup dinamik sayfalarda işe yaramıyor bu yüzden selenium kullanarak gerçek bir tarayıcıda açıp verilerin gelmesini bekledik. <br/>

<br/>
<br/>

Simdi size verilerimizin örnek bir görüntüsünü gösterelim.<br/><br/>

### Örnek resim:<br/><br/>

![orenek_reism](https://github.com/asGenn/binanceDdi/assets/109176905/8144501b-37bf-4644-8b60-29f73ebb6449)

<br/>

Data setini oluştururken binanceden 3 saatte 2000 veri çekilmiştir ama bunları etiketlemek için yine o kadar saat gerekiyordu ondan doalyı biz 600 tanesini kullandık.Yaptığımız projede 2000 ile 600 arasında çok bir fark olmayacaktır. Sebebi ise haberlerin içerikleri genelde zaten birbirinden çok farklı ve kullandığımız etiketleme algoritmasının çok doğru çalıştığını tespit etmenin de bir yolu yoktur.

### Veri seti'nde Bulunan Olumlu Olumsuz Haber sayısı:<br/><br/>
![data_set_veri_sayisi](https://github.com/asGenn/binanceDdi/assets/109176905/08fde505-8c75-428b-89c9-371d8a12b918)

## buradaki -1 olumsuz haberi +1 ise olumlu haberi temsil etmektedir.
<br/>


<br/>

Veri seti'ndeki kolonlarımız aşağıdaki gibidir:<br/>
-Binance haber url'i.<br/>
-Haber başlığı<br/>
-Haber içeriği<br/>
-Haberde varsa etiketli coin sembolu.<br/>
-Haber tarihi.<br/>





# Haberlerin Temizlenmesi ve Lemmatization İşlemi<br/>

Veriseti oluşturulduktan sonra modelin daha iyi çalışması ve başarı oranının daha yüksek olması için haberlerin temizlenmesi gerekmektedir. Haberlerin içerisinde emojiler, noktalama işaretleri, stopwordsler, linkler gibi istenmeyen ve modelin başarısını düşürecek veriler haberler içerisinden temizleniyor. Daha sonra lemmatization (kelimelerin köklerinin alınması) işlemi yapılarak temiz ve kelimelerin köklerinden oluşan haberler elde ediliyor.
<br/><br/>

### Oluşturulan Temiz Haber Görseli<br/><br/>

![Ekran görüntüsü 2024-01-05 171858](https://github.com/asGenn/binanceDdi/assets/109176905/f38186a3-ecf7-4194-bea0-2b7d2d7ecead)
<br/><br/>

# Modelin Oluşturulması ve Haberlerin Kategorilendirilmesi<br/>

## Model Seçimi

Yapılacak kategorilendirme işleminin hangi modelde daha yüksek başarı oranı vereceğini tespit etmek amacıyla araştırma yapılıp aynı zamanda bazı modeller üzerinde de test edilmiştir. Başlangıç olarak 3 popüler model üzerinde denemeler yapılmıştır. Bu modeller Naive Bayes, DecitionTree ve Support Vector Machine modelidir. Veriseti üzerinde bu modellerin accuracy ve f1 score ları test edilmiştir. Projedeki test veriseti sonuçlarına bakıldığında:<br/>

![Ekran görüntüsü 2024-01-05 172230](https://github.com/asGenn/binanceDdi/assets/109176905/3187ee14-e2f3-4b3f-a5fc-f457d3c4203b)

<br/>
<br/>
Sonuçlar incelendiğinde gördüğümüz gibi başarı oranı düşüktür yane bu modelin her hangi bir tahminde kullanılması çokta iyi sonuçlar vermez ama unutmayalım ki yapmaya çalıştığımız iş bu kadar az veri ile yapılamaz.:<br/>


## Modelin Oluşturulmaya Başlanması

### Etiketleme

Etiketlemeyi yukarda anlattığımız gibi eğer habere etiketli bir coin var ise haberin yayınla tarihinden itirabaren 12 saat içerisinde nasıl bir değişiklik olduğunu hesaplıyoruz ve eğer yükseldiyse +1 düştüyse -1 diyoruz bütün coinlerin + ve - değerlerini toplayarak bir -1 ve +1 arasında bir değer buluyoruz buda bizim etiketimiz oluyor. eğer habere etiketli bir coin yok ise benim belirlediğim eth btc ve tethere bakıyoruz.<br/><br/>


<br/>
Verisetini parçalamak için train_test_split() fonksiyonu kullanılmıştır.<br/>

### Haberlerin Vektörel Matrisinin Çıkarılması

Haberler birer metin oldukları için bunları bilgisayarında iyi anladığı şeylere yanı sayılara dönüşüştürmemiz gerekiyor ben burda bu işlemi yapmak için tfıdf ve count vectorizer ile yapıyorum. <br/><br/>

### Modellerin Eğitilmesi

Daha önceden parçalanmış olan X_train ve y_train verileri Naive Bayes ve Support Vector Machine modeline gönderilerek modeller eğitilmiştir. Eğitim sonucunda modellerin accuracy ve f1 score değerleri hesaplanmıştır. Modelleri eğitmek için sklearn kütüphanesi kullanılmıştır.<br/><br/>

### Modellerin Başarısının Hesaplanması

Modelin başarısı hem train hem test verileri üzerinden Accuracy ve F1 score ile ölçülmüştür. Alınan sonuçlar aşağıda bulunmaktadır.<br/><br/>




# test
Ben burada modelimi teste sokmadım çünkü değerleri %50 ye çok yakın yane modelin vereceği tahmin yazı turadan çok da farklı olmayacaktır.

# Sonuç

Sonuç olarak haberlere bakılarak bir borsa tahmini yapacaksak bu haberin hangi coin hakkında olduğunu da bilmemiz gerekiyor. Unutmamamız gereken en önemli şeylerden biriside coinlerin genellikle haberlere göre şekillenmediğidir. Bu sonuçla ilgilenme sebebimiz modelimizin başarısını düşüren en önemli etken olmasıdır.Sonuç daha fazla veri ile yükselebilirdi ama dediğim gibi çok fazla veri gerekiyor ve bu verileri kısa yoldan almanın bir yolu da görünmüyor. Ama baktığımız zaman %63 lere kadar tahmin oranımızı çıkardık Naive bayes ile burda dikkat etmemiz gereken olay ise seçtiğimiz değerlerin bizim veri setimize overfitting etmiş olabileceğidir.Ama yine de en başarılı modelimiz NB'dir.
