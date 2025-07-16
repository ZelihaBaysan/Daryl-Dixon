# Internship Preparation 🚀

I'm currently preparing for my internship.

![daryl](./images/daryl-dixon.gif)



# Daryl Dixon 

Bu proje, büyük dil modelleri (Large Language Models - LLM) kullanarak doğal dil girdilerinden SQL sorguları üretmeyi ve bu sorguları veritabanında çalıştırmayı hedefleyen bir Python uygulamasıdır. Aynı zamanda embedding işlemlerini test etmek ve veri işleme süreçlerini geliştirmek için hazırlanmıştır.

---

## İçindekiler

* [Proje Hakkında](#proje-hakkında)
* [Özellikler](#özellikler)
* [Dosya Yapısı](#dosya-yapısı)
* [Kurulum ve Çalıştırma](#kurulum-ve-çalıştırma)
* [Kullanım](#kullanım)
* [Detaylı Açıklama](#detaylı-açıklama)
* [Geliştirme ve Katkı](#geliştirme-ve-katkı)
* [İletişim](#iletişim)

---

## Proje Hakkında

Bu proje, staj sürecinde pratik yapmak amacıyla geliştirilmiş, doğal dil komutlarını SQL sorgularına çeviren ve bu sorguları çalıştıran bir sistemdir. Aynı zamanda veritabanı işlemleri ve embedding tabanlı metin analizlerini test etmek için kullanılır.

---

## Özellikler

* Doğal dil girdilerini SQL sorgularına dönüştürme
* SQL sorgularını veritabanında çalıştırma
* Metin verileri için embedding işlemleri yapma ve test etme
* Veri ve görseller için organize klasör yapısı
* Kolayca geliştirilebilir ve genişletilebilir yapı

---

## Dosya Yapısı

```
/data/           - Projede kullanılan veri dosyaları  
/images/         - Proje ile ilgili görseller  
/storage/        - Çalışma sırasında oluşturulan dosyaların saklandığı yer  
llm_sql_query.py - Doğal dil sorgularını SQL sorgularına dönüştüren ana betik  
sql_query.py     - SQL sorgularını veritabanında çalıştıran betik  
test_embed.py    - Embedding işlemlerinin test edildiği dosya  
README.md        - Proje açıklaması ve kullanım bilgileri  
```

---

## Kurulum ve Çalıştırma

1. Python 3.7 veya üzeri sürümü kurulu olduğundan emin olun.
2. Gerekli Python paketlerini yükleyin:

```bash
pip install -r requirements.txt
```

3. Projeyi klonlayın veya indirin:

```bash
git clone https://github.com/ZelihaBaysan/Daryl-Dixon.git
cd Daryl-Dixon
```

4. Betikleri çalıştırarak proje fonksiyonlarını test edebilirsiniz.

---

## Kullanım

* `llm_sql_query.py` dosyasını kullanarak doğal dilde yazılmış sorguları SQL sorgularına çevirebilirsiniz.
* `sql_query.py` dosyasıyla SQL sorgularını veritabanında çalıştırabilir, sonuçları görebilirsiniz.
* `test_embed.py` dosyası ile embedding fonksiyonlarını test edebilirsiniz.

---

## Detaylı Açıklama

### llm\_sql\_query.py

Bu betik, OpenAI gibi büyük dil modellerinden yararlanarak doğal dilde verilen sorguları uygun SQL sorgularına dönüştürür. Böylece kullanıcıların veritabanı sorgulama bilgisi olmadan da işlem yapmaları mümkün olur.

### sql\_query.py

Çevrilen SQL sorgularını yerel veya uzak bir veritabanına gönderir ve sorgu sonuçlarını döner. Bu sayede veriler üzerinde doğrudan işlem yapılabilir.

### test\_embed.py

Metin verilerini sayısal vektörlere dönüştüren embedding işlemlerini test eder. Bu, metinlerin makine öğrenmesi modellerinde kullanılmasını sağlar.



