# Clean Code Felsefesi

Amaç: Kod yazarken uygulanan yaklaşımı Robert C. Martin'in *Clean Code* kitabından türetmek ve zamanla geliştirmek. Kitapta geçmeyen tamamlayıcı kalıplar `◇` simgesiyle, ilgili kitap başlığının altında tutulur.
Omurga Kent Beck'in basit tasarım kurallarıdır: testler geçer → tekrar yok → niyet açık → en az öğe.
Bu kuralların altında SRP ve DIP/DI yatar.

## Dosyalar

| Dosya | Ne |
|---|---|
| `zihin-haritasi.md` | **Tek kaynak.** Bölüm → başlık → ilke, markmap uyumlu Markdown. |
| `zihin-haritasi.html` | Yalnız görüntüleyici; `.md`'yi okuyup çizer, içerik kopyalamaz. |
| `export_map.py` | `.md`'yi kitap okuyucusuna (`~/Desktop/3-kitap-ceviri/Clean Code/data/mindmap.js`) aktarır. |
| `kitap-disi-kartlar.json` | **Tek kaynak.** ◇ kitap dışı kalıpların kavram kartları; okuyucunun kart şeması (iki dilli, kötü/iyi kod, ipucu), kule senaryosu örnekleri. |
| `export_cards.py` | Kartları doğrular ve okuyucuya (`data/offbook.js`) aktarır. Haritadaki ◇ kalıplarla birebir eşleşmezse durur. |
| `tamam-tanimi.md` | **Tamam tanımı.** Bir görevin bittiğini söyleyen kontrol listesi. Kitabın her bölümünü başlık adıyla kapsar; kalıpların hangi ihtiyaçla geldiğini de söyler. Nesne yönelimli diller (şimdilik Python, Java) için ortak sözcüklerle yazılır; dile özgü karşılıklar sondaki "Dil eşlemesi" tablosundadır. Kitap standarttır, dile göre gevşetilmez. |
| `measure_code.py` + `measure/` | Listenin ölçülebilir maddelerini Python kodunda AST ile ölçer: `python3 measure_code.py <dosya ya da dizin>`. Çıktı alarmdır, her alarm okunarak karara bağlanır. Testleri: `python3 -m unittest discover -s tests -t .` |

Görmek için:

```bash
python3 -m http.server 8766 --bind 127.0.0.1
```

Sonra http://127.0.0.1:8766/zihin-haritasi.html adresini açın.

## Kitap okuyucusundaki harita

Okuyucunun üst barındaki 🧠 Harita düğmesi bu haritayı tam ekran açar. Okuyucu, haritayı bu klasörden değil kendi `data/mindmap.js` dosyasından okur. Bu yüzden `zihin-haritasi.md` her değiştiğinde aktarım çalıştırılır:

```bash
python3 export_map.py
```

`data/mindmap.js` üretilen bir dosyadır, okuyucu reposunda elle düzenlenmez.

## Kitap dışı kartlar

Okuyucunun üst barındaki ◇ Kalıplar düğmesi, haritadaki ◇ kalıpların kartlarını sağ çekmecede açar. Kaynak `kitap-disi-kartlar.json`'dır; değiştiğinde:

```bash
python3 export_cards.py
```

Haritaya yeni bir ◇ kalıp eklenirse kartı da yazılır; biri eksikse aktarım hangisinin eksik olduğunu söyleyerek durur. `related` alanındaki sayfalar okuyucuda var olmalıdır.

## Kaynak: kitabın kendisi

- **PDF:** `~/Desktop/3-kitap-ceviri/Clean Code/my_book.pdf`. Kitap sayfası ile PDF sayfası aynıdır (ofset 0).
- **LightRAG grafı:** `~/Desktop/3-kitap-ceviri/Clean Code/tools/_work/graph/lightrag`
  - Başlatmak: `./start_all.sh` (embedding proxy 9700, sunucu 9621). Durdurmak: `./stop_all.sh`.
  - Sorgu:

```bash
curl -s -X POST http://127.0.0.1:9621/query -H 'Content-Type: application/json' -d '{"query":"...","mode":"hybrid"}'
```

  - İndeks bütün kitabı içerir: 1-17. bölümler ve ekler (s.1-412). Dizin (s.413-431) bilerek dışarıdadır.
  - Girdi, okuyucunun çevrilmiş sayfalarındaki İngilizce metinden okuyucu reposundaki `tools/girdi_hazirla/hazirla.py` ile üretilir; kullanımı o klasörün README'sinde.
  - Kod listeleri de indekstedir. Sorgu bir listenin kodunu getirmezse (getirme sıralaması kodu her zaman seçmez) PDF'e bakılır.
  - Gateway kesintisinde belge "failed" kalır; `hazirla.py yeniden` önbellekteki çıkarımları kullanarak kaldığı yerden sürdürür.
  - İkinci bir sunucu açılırsa (`start_yeniden.sh`, 9622) `INPUT_DIR` ortam değişkeni `--input-dir` ile aynı klasörü göstermeli: sunucu yüklenen dosyayı `--input-dir`'e yazar, ayrıştırıcı `INPUT_DIR`'de arar.
  - Bölüm başlangıç sayfaları okuyucunun `progress.json` → `chapters` tablosundadır.

## Haritayı güncelleme kuralı

1. Önce kitaba sor: LightRAG ya da PDF. Kitapta olmayan bir öğe yalnız `◇` simgesiyle girer ve en ilgili kitap başlığının alt yaprağı olur (ayrı dal açılmaz). Biçimi `◇ ihtiyaç → KALIP`; aktarım betiği kalıbı buradan okur. Kitaptaki bir öğe `◇` taşımaz. Belirli bir başlığa oturmayan ◇ kalıp "Bağlantılar" dalındaki kalıp listesine girer.
2. Yaprak biçimi: `Başlık: ilke`, varsa eşik. Kitaptaki başlık adı korunur ki kaynağa geri dönülebilsin.
3. Dallar kitabın akışıyla küçükten büyüğe iner: isim → fonksiyon → sınıf → sistem → ortaya çıkış.
4. Eşikler (20 satır, 3 argüman, 200 satır) alarmdır, ölçüt değildir. Asıl soru sorumluluk ve niyettir.
5. Kalıplar ihtiyaç doğunca girer. Hangi ihtiyacın hangi kalıbı getirdiği "Bağlantılar" dalında durur.
