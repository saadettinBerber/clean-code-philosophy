# Tamam tanımı (Definition of Done)

Bir görev, bu listedeki bütün maddeler işaretlendiğinde biter. Bitince commit atılır ve push edilir.
Kaynak kitabın kendisidir ve kitap **standarttır**: kural dile ya da alışkanlığa göre gevşetilmez, istisna yalnız kitabın kendi verdiği istisnadır. Kitap 2026-09-25'te PDF ve LightRAG üzerinden, dört alt ajanla bölüm bölüm okundu. Madde sonundaki parantez maddenin kaynağını verir: bölüm ve kitaptaki başlık adı, varsa Bl.17'deki koku kodu.

- **[ö] Ölçülebilir:** AST ya da bir araçla mekanik olarak denetlenir (`measure_code.py`). Sonuç yalnız bir **alarmdır**, her alarm okunarak karara bağlanır.
- **[o] Okuma:** Kararı yargı verir; kod okunarak cevaplanır.

**Eşik alarmdır, ölçüt değildir.**
- Fonksiyonda hedef 2-4 satırdır, 20 satır tavandır.
- 200 satırlık sınıf yalnız bir alarmdır. Kitaptaki SuperDashboard beş metotluk küçük bir sınıftır, ama iki işi vardır. Asıl ölçü sorumluluktur.

---

## 0 · Süreç: her görevde bu sırayla

1. [ ] Davranışı sabitleyen testler değişiklikten önce vardı. Yoksa önce onlar yazıldı. (Bl.14 · On Incrementalism; Bl.16 · First, Make It Work)
2. [ ] Kod önce kaba yazıldı, sonra testler yeşil tutularak arıtıldı: bölme, yeniden adlandırma, tekrar silme, yeniden sıralama. Kimse ilk seferde temiz yazamaz. (Bl.3 · How Do You Write Functions Like This?; Bl.12 · Rules 2-4)
3. [ ] Değişiklik küçük adımlarla yapıldı, her adımdan sonra bütün takım yeşildi. Büyük yeniden tasarım yapılmadı. (Bl.14 · On Incrementalism; Bl.1 · The Grand Redesign in the Sky)
4. [ ] "Çalışıyor" noktasında durulmadı. Karmaşa oluştuğu anda temizlendi, "sonra"ya bırakılmadı: sonra, hiç demektir. (Bl.1 · Bad Code; Bl.10 · SRP; Bl.14 · Conclusion)
5. [ ] Geçici eklenip çıkarılan kod kalıntı bırakmadı. (Bl.14 · Rubik küpü; G9, F4)
6. [ ] `measure_code.py` değişen dosyalarda çalıştı. Her ALARM "gerçek, düzeltildi" ya da "yanlış pozitif, çünkü…" diye karara bağlandı. [ö]
7. [ ] Aşağıdaki bölümler okundu; bulgular haritadaki başlık adıyla yazıldı.
8. [ ] Davranış değiştiyse gerçek çıktı (ör. EPUB) üretildi ve beklenen fark görüldü. Yeniden düzenlemeyse eski kodla karşılaştırıldı, fark çıkmadı. Fark çıktıysa önce o farkı gösteren birim testi yazıldı. (CLAUDE.md; T6)
9. [ ] Commit atomik: tek değişiklik, tek cümlelik Türkçe mesaj, gövde yok. Mesaja "ve" giriyorsa commit bölündü. Boy Scout temizliği ayrı bir commit oldu.

**Durma koşulu:** Bir madde sağlanamıyorsa, bir alarm için karar verilemiyorsa ya da kullanıcının vermesi gereken bir tasarım kararı çıktıysa commit atılmaz, kullanıcıya sorulur.

---

## 1 · Temiz Kod (Bl.1)
- [ ] Dokunulan her dosya bulunduğundan biraz daha temiz bırakıldı: bir ad iyileşti, bir fonksiyon bölündü, küçük bir tekrar kalktı ya da bir bileşik `if` sadeleşti. Önceki ölçümlere göre hiçbir değer kötüleşmedi. (Bl.1 · The Boy Scout Rule) [ö]
- [ ] Bilet numarası taşımayan TODO/FIXME yok. (Bl.1 · Bad Code; Bl.4 · TODO Comments) [ö]
- [ ] "Zaten kötüydü" diye bırakılan kırık cam yok. (Bl.1 · What Is Clean Code? — Stroustrup) [o]
- [ ] Her üretim modülünün testi var; testi olmayan kod temiz değildir. Bir işi yapmanın tek yolu var, API en küçük hâlinde. (Bl.1 · Dave Thomas) [ö/o]
- [ ] Birden çok yerde yapılan aynı iş, küçük ve basit bir soyutlamaya sarıldı. Genel bir API kurulmadı, yalnız gereken biçimler sunuldu. (Bl.1 · Jeffries) [o]
- [ ] Her rutin "aşağı yukarı beklendiği gibi" çıkıyor; kod düzyazı gibi okunuyor, spekülatif kod yok. (Bl.1 · Cunningham, Booch) [o]
- [ ] Kitaptan bilerek sapılan yer varsa gerekçesi CLAUDE.md'de yazılı. (Bl.1 · Schools of Thought) [o]
- [ ] Okuyucu için yazıldı; okuma/yazma oranı 10:1'den büyüktür. (Bl.1 · We Are Authors) [o]

## 2 · Anlamlı İsimler (Bl.2, N1-N7)
- [ ] Her ad neden var olduğunu, ne yaptığını ve nasıl kullanıldığını söylüyor; yorum istemiyor. Ölçü birimi adda (`elapsed_days`). (Bl.2 · Use Intention-Revealing Names; N1) [o] Satır sonu yorumlu atamalar [ö] ile yakalanır.
- [ ] Anlamlı indis ya da değer (`x[0] == 4`) adlı bir sabite ya da niyet gösteren bir metoda (`cell.is_flagged()`) dönüştü. (Bl.2 · Use Intention-Revealing Names; G25) [ö]
- [ ] Yanıltıcı ad yok: `account_list` bir `set` değil. Kap türü ada yazılmıyor. `l`, `O` ve `I` tek başına ad olarak kullanılmıyor. Az farkla benzeyen ad çiftleri yok. (Bl.2 · Avoid Disinformation) [ö]
- [ ] Yalnız yorumlayıcıyı susturmak için yapılmış ayrım yok: `a1/a2`, `klass`, gürültü sözcükler (`Info`, `Data`, `Object`, `the_`, `NameString`). Hangisinin çağrılacağı belirsiz kardeşler yok (`get_account` / `get_accounts` / `get_account_info`). (Bl.2 · Make Meaningful Distinctions) [ö]
- [ ] Ad sesli okunup tartışılabiliyor. (Bl.2 · Use Pronounceable Names) [o]
- [ ] Ad uzunluğu kapsamla orantılı. Tek harfli ad yalnız kapsamı 5 satırı aşmayan yerel değişkende kullanılıyor; modül düzeyinde ve parametrede kullanılmıyor. Aranacak her sabit adlı. (Bl.2 · Use Searchable Names; N5, G25) [ö]
- [ ] Adda kodlama yok: Hungarian (`str_`, `lst`), `m_`, `I` önekli arayüz, alt sistem öneki. Bir şey kodlanacaksa arayüz değil uygulama kodlanır. (Bl.2 · Avoid Encodings; N6) [ö]
- [ ] Okuyucu hiçbir adı zihninde başka bir şeye çevirmek zorunda değil. Döngü sayacı dışında tek harfli ad yok. (Bl.2 · Avoid Mental Mapping) [ö]
- [ ] Sınıf adı bir isim ya da isim öbeği. Adında `Manager`, `Processor`, `Data`, `Info` ya da `Super` yok; kısa ve kesin bir ad verilemiyorsa sınıf büyüktür. (Bl.2 · Class Names; Bl.10) [ö]
- [ ] Metot adı bir fiil ya da fiil öbeği. `is_`, `has_` ve `can_` ile başlayan adlar bool döndürüyor. Birden çok kurucu biçimi gerekiyorsa adlı `@classmethod` fabrikası (`from_…`) var. (Bl.2 · Method Names; G20) [ö]
- [ ] Espri, argo ya da kültüre bağlı ad yok. (Bl.2 · Don't Be Cute) [o]
- [ ] Bir kavram için tek sözcük kullanılıyor: `get`, `fetch`, `retrieve`, `load` bir arada değil. `manager` ile `controller` da öyle. (Bl.2 · Pick One Word per Concept; G11) [ö]
- [ ] Aynı sözcük iki anlamda kullanılmıyor: değer birleştiren `add` başka, koleksiyona öğe koyan `append`/`insert` başka. (Bl.2 · Don't Pun) [o]
- [ ] Teknik kavramda çözüm alanının adı (algoritma, kalıp: `AccountVisitor`, `JobQueue`), alan kavramında problem alanının adı kullanılıyor. Projenin ortak dili adlarda görünüyor. (Bl.2 · Use Solution/Problem Domain Names; N3) [o]
- [ ] Tek başına eksik kalan ad (`state`, `number`) bir sınıfın ya da modülün içine yerleşerek bağlam kazandı. Önek eklemek son çaredir. Uzun bir fonksiyonda birlikte gezen değişkenler bir sınıfın alanları oldu. (Bl.2 · Add Meaningful Context) [o/ö]
- [ ] Gereksiz bağlam yok: her sınıfa proje öneki eklenmiyor, paket adı sınıf adında tekrar etmiyor. (Bl.2 · Don't Add Gratuitous Context; N6) [ö]
- [ ] Ad uygulamayı değil soyutlama düzeyini söylüyor: `dial(phone_number)` yerine `connect(locator)`. (N2) [o]
- [ ] İç içe fonksiyonların adları farkı belirsizliksiz söylüyor. (N4) [o]
- [ ] Ad yan etkiyi söylüyor: nesneyi yaratıp döndüren fonksiyon `get_x` değil `create_or_return_x`. (N7) [ö] `get_`/`is_` ile başlayıp atama ya da G/Ç yapan fonksiyonlar aranır.
- [ ] Daha iyi bir ad bulununca değiştirildi. (Bl.2 · Final Words) [o]

## 3 · Fonksiyonlar (Bl.3, F1-F4)

**Boyut ve yapı**
- [ ] Fonksiyon küçük: hedef 2-4 satır. 4'ü aşan fonksiyona bakılır, 20 satır tavandır. (Bl.3 · Small!) [ö]
- [ ] `if`, `else` ve `while` blokları tek satır; o satır adı iyi seçilmiş bir çağrı. Girinti en fazla 1-2 düzey. (Bl.3 · Blocks and Indenting) [ö]
- [ ] Fonksiyon tek iş yapıyor. İçinden, uygulamasını yeniden söylemekten öte bir ad taşıyan başka bir fonksiyon çıkarılamıyor. "TO paragrafı" testinden geçiyor. (Bl.3 · Do One Thing; G30) [o]
- [ ] Gövde boş satırla ya da başlık yorumuyla bölümlere ayrılmıyor. (Bl.3 · Sections within Functions) [ö]
- [ ] Tek soyutlama düzeyi: `get_html()` ile `.append("\n")` aynı fonksiyonda değil. (Bl.3 · One Level of Abstraction; G34, G6) [o]
- [ ] Stepdown kuralı: çağıran üstte, çağrılan hemen altında; kod yukarıdan aşağı bir hikâye gibi okunuyor. (Bl.3 · The Stepdown Rule; Bl.5 · Vertical Ordering; G10) [ö]
- [ ] Ad ne yaptığını söylüyor; modüldeki adlar tutarlı bir hikâye kuruyor. (Bl.3 · Use Descriptive Names; G20) [o]

**Argümanlar**
- [ ] Argüman sayısı 0'dan (niladic, ideal) başlayarak 1'e (monadic) ve 2'ye (dyadic) çıkıyor. 3 argümandan (triadic) kaçınılır, gerekçe ister. 3'ten fazlası (polyadic) kullanılmaz. `self` ve `cls` sayılmaz; `*args` ve `**kwargs` birer argüman sayılır. (Bl.3 · Function Arguments; F1) [ö: 3 alarm, 4 ve üzeri ihlal]
- [ ] Tek argümanlı fonksiyon üç biçimden birine uyuyor:
  - soru sorar (`exists(x) -> bool`),
  - dönüştürür (girdi aynı kalsa bile yeni değer döndürür),
  - olaydır (`None` döner ve bunu adından belli eder).

  (Bl.3 · Common Monadic Forms) [ö/o]
- [ ] Bayrak argümanı yok: bool parametre fonksiyonu ikiye böler. Davranış seçen `mode="..."` dizgesi ya da enum da aynı koku. (Bl.3 · Flag Arguments; F3, G15) [ö]
- [ ] İki argümanın doğal bir sırası ve uyumu var (`Point(x, y)`). Yoksa bir argüman düşürüldü. Kitap bunun üç yolunu verir: fonksiyonu argümanın metodu yapmak, argümanı alana çevirmek ya da argümanı yapıcıda alan bir sınıf çıkarmak (`FieldWriter`). (Bl.3 · Dyadic Functions) [o]
- [ ] Birlikte gezen argümanlar, adını hak eden bir kavrama sarıldı (`Circle(center: Point, radius)`). Aynı parametre çifti iki ya da daha fazla fonksiyonda geçiyorsa bu bir adaydır. (Bl.3 · Argument Objects) [ö]
- [ ] Fonksiyon adı argümanla bir fiil/isim çifti kuruyor (`write_field(name)`). Sıra belirsizse yalnız anahtar sözcükle verilen argümanlar kullanılıyor; bunlar da argüman sayısına girer. (Bl.3 · Verbs and Keywords) [o]

**Yan etki, CQS, hata**
- [ ] Adın söylemediği bir yan etki yok. Zamansal bağ kaçınılmazsa hem adda hem argüman zincirinde görünüyor. (Bl.3 · Have No Side Effects; N7, G31) [ö/o]
- [ ] Çıktı argümanı yok: parametre üzerinde `p.x =`, `p.append(...)` ya da `p.update(...)` yapılmıyor. Durum değişecekse bu, sahibi olan nesnenin metodudur. (Bl.3 · Output Arguments; F2) [ö]
- [ ] Komut ile sorgu ayrı: bir fonksiyon hem durum değiştirip hem değer döndürmüyor. (Bl.3 · Command Query Separation) [ö]
- [ ] Hata kodu ya da başarı bool'u döndürülmüyor, istisna fırlatılıyor. (Bl.3 · Prefer Exceptions to Returning Error Codes) [ö]
- [ ] `try` gövdesi ve `except` gövdesi ayrı fonksiyonlarda. Hatayı yöneten fonksiyon başka iş yapmıyor: `try` ilk deyim, `except` sonrasında bir şey yok. (Bl.3 · Extract Try/Catch Blocks; Error Handling Is One Thing) [ö]
- [ ] Herkesin içe aktardığı merkezi bir hata kodu enum'u yok; yeni hata, yeni bir istisna alt sınıfıdır. (Bl.3 · The Error.java Dependency Magnet) [ö]
- [ ] Tekrar yok. (Bl.3 · Don't Repeat Yourself; G5) [ö]
- [ ] Küçük fonksiyonda erken `return` serbest; tek giriş-tek çıkış ancak büyük fonksiyonda aranır. (Bl.3 · Structured Programming) [ö]
- [ ] Çağrılmayan fonksiyon silindi. (F4) [ö]

**Tür dallanması**
- [ ] Bir tür için tek switch var: `if/elif`, `match`, `isinstance` zinciri ya da sözlükle dağıtım. O da fabrikanın dibinde durup polimorfik nesne üretiyor. Aynı ayırıcıya bakan ikinci bir dallanma alarmdır. (Bl.3 · Switch Statements; G23) [ö]

## 4 · Yorumlar (Bl.4, C1-C5)
- [ ] Her yorumdan önce kodla anlatmak denendi: yorumlanan koşul niyet gösteren bir fonksiyona, yorumlanan ifade açıklayıcı bir ara değişkene dönüştü. (Bl.4 · Explain Yourself in Code; Don't Use a Comment When You Can Use a Function or a Variable; G19, G28) [ö/o]
- [ ] Kalan yorum şu iyi türlerden biri:
  - lisansa kısa gönderme (Legal),
  - NEDEN'i anlatan niyet açıklaması (Explanation of Intent),
  - değiştirilemeyen koddaki belirsizliğin açıklaması, doğruluğu ayrıca denetlenmiş olarak (Clarification),
  - sonuç uyarısı (Warning of Consequences),
  - bilet numaralı TODO,
  - önemsiz görünen ama önemli bir ayrıntıyı vurgulama (Amplification).

  (Bl.4 · Good Comments) [o]
- [ ] Uyarı yapıya çevrilebiliyorsa çevrildi: yorumla kapatılmış test yerine `@unittest.skip("neden")`. (Bl.4 · Warning of Consequences; G27) [ö]
- [ ] Gerekli yorum yazılmış değil: bariz olanı tekrarlayan ya da yalnız imzayı sayan yorum ve docstring yok. (Bl.4 · Redundant, Noise, Mandated Comments; C3) [ö]
- [ ] Yorumda değişiklik günlüğü, yazar ya da tarih yok; bunlar sürüm kontrolünün işi. (Bl.4 · Journal Comments, Attributions and Bylines; C1) [ö]
- [ ] Yoruma alınmış kod yok. (Bl.4 · Commented-Out Code; C5) [ö]
- [ ] `# ----` gibi afiş yorumu, `# end if` gibi kapanış yorumu ya da yorumda HTML yok. (Bl.4 · Position Markers, Closing Brace Comments, HTML Comments) [ö]
- [ ] Yorum yalnız yanındaki kodu anlatıyor: sistemin uzak bir yerini, tarihçeyi ya da ilgisiz ayrıntıyı anlatmıyor. Yorumla kod arasındaki bağ açık. (Bl.4 · Nonlocal Information, Too Much Information, Inobvious Connection) [o]
- [ ] Anlamı için başka modüle bakmak gerektiren yorum yok. Gövdesi yalnız yorum ya da `pass` olan `except` yok; bu aynı zamanda yutulan istisnadır. (Bl.4 · Mumbling) [ö]
- [ ] Dışa açık API'nin docstring'i iyi. `_` ile başlayan iç fonksiyonlarda `Args:`/`Returns:` gibi biçimsel docstring yok. (Bl.4 · Javadocs in Public APIs / in Nonpublic Code, Function Headers) [ö]
- [ ] Değişen kodun yanındaki yorum hâlâ doğru; yanlış yorum, hiç yorum olmamasından kötüdür. (Bl.4 · Misleading Comments; C2) [o]
- [ ] Yazmaya değen yorum kısa, dilbilgisi doğru ve bariz olmayanı söylüyor. (C4) [o]

## 5 · Biçimlendirme (Bl.5, G10, G24)
- [ ] Biçim kuralı bir araçla uygulanıyor; ekibin tek bir kuralı var. **Bu depoda henüz bir araç yapılandırması yok.** (Bl.5 · Team Rules; G24) [ö]
- [ ] Dosya boyu tipik olarak 200 satır civarında, 500'ün altında. Bu bir alarmdır: 200'ün altında kalmak tek sorumluluğu kanıtlamaz. (Bl.5 · Vertical Formatting) [ö]
- [ ] Gazete düzeni: modül adı tek başına yeterli, üstte genel kavram, aşağı indikçe ayrıntı. (Bl.5 · The Newspaper Metaphor) [ö/o]
- [ ] Kavramlar boş satırla ayrılıyor; birbirine sıkı bağlı satırlar yoğun duruyor. (Bl.5 · Vertical Openness, Vertical Density) [ö]
- [ ] Yerel değişken ilk kullanımının hemen üstünde, özel fonksiyon ilk çağrısının hemen altında. Örnek değişkenleri yalnız `__init__`'te atanıyor. (Bl.5 · Vertical Distance, Variable Declarations, Dependent Functions; G10) [ö]
- [ ] Aynı işin türevlerini yapan fonksiyonlar yan yana duruyor. (Bl.5 · Conceptual Affinity) [ö/o]
- [ ] Satırlar kısa: 100-120 karakter kabul edilebilir, ötesi özensizliktir. (Bl.5 · Horizontal Formatting) [ö]
- [ ] Sütun hizası yok; hizalanmak istenen uzun liste, sınıfın bölünmesi gerektiğini gösterir. Tek satıra sıkıştırılmış `if`/`def` ya da `lambda` ataması yok. (Bl.5 · Horizontal Alignment, Breaking Indentation, Dummy Scopes) [ö]
- [ ] Bilinen bir sabit alt düzeye gömülmemiş; bilindiği yerden argümanla aşağı iniyor. (G35) [ö/o]

## 6 · Nesneler ve Veri Yapıları (Bl.6, G14, G36)
- [ ] Beklenen değişiklik adlandırıldı ve biçim buna göre seçildi:
  - yeni **tür** bekleniyorsa: nesne + polimorfizm,
  - yeni **işlem** bekleniyorsa: veri yapısı + fonksiyon.

  (Bl.6 · Data/Object Anti-Symmetry) [o]
- [ ] Sınıf alanlarını erişimcilerle dışarı itmiyor, verinin özünü işleyen soyut bir arayüz sunuyor ("galon" değil "kalan yakıt yüzdesi"). Düşünmeden eklenmiş getter/setter yok; birlikte değişen değerler tek bir işlemle ayarlanıyor. (Bl.6 · Data Abstraction; G8) [ö]
- [ ] **Melez yok.** Aynı sınıf hem açık durum hem anlamlı davranış taşımıyor; melez hem yeni türü hem yeni işlemi zorlaştırır. (Bl.6 · Hybrids; G14) [ö]
  - **Açık durum (A):** `_` ile başlamayan alan, yalnız `return self._x` yapan property ya da getter, yalnız `self._x = v` yapan setter.
  - **Anlamlı davranış (B):** erişimci olmayan, bir deyimden uzun ya da başkasını çağıran ya da durum değiştiren public metot.
  - **Kural:** A > 0 ve B > 0 ise melez adayıdır. Başka modüller bu sınıfın alanlarını okuyup karar veriyorsa melezlik gerçektir.
- [ ] Demeter: metot yalnız dört şeyle konuşuyor: `self`, kendi kurduğu nesne, argümanı ve kendi alanı. Bir çağrının dönen değeri üzerinde yeni bir çağrı yapmıyor. (Bl.6 · The Law of Demeter; G36) [ö]
- [ ] Tren kazası yok (`a.b().c().d()`). Zinciri ara değişkenlere bölmek ihlali gidermez; iş nesneye taşınır: `ctxt.create_scratch_file_stream(name)`. Demeter veri yapılarına uygulanmaz. (Bl.6 · Train Wrecks, Hiding Structure) [ö/o]
- [ ] Metot başka bir nesnenin verisiyle kendi verisinden çok uğraşmıyor (feature envy). (G14) [ö]
- [ ] Veri taşıyıcı DTO davranışsız: `@dataclass`/`NamedTuple` üzerinde metot yok. Yalnız görünüş için yazılmış "bean" property'leri yok. (Bl.6 · Data Transfer Objects) [ö]
- [ ] Active Record'a (kaydet/yükle metotlu veri yapısı) iş kuralı konmamış; iş kuralı ayrı bir nesnede. (Bl.6 · Active Record) [ö]
- [ ] "Her şey nesnedir" efsanesine direnildi; saf veri zorla nesneye sarılmadı. (Bl.6) [o]

**Fonksiyon yazıp geçilmedi: sınıf tasarlandı.** Dil fonksiyona izin verir diye tasarım fonksiyona bırakılmaz. Kitabın sınıfa götüren işaretleri aranır:
- [ ] Aynı değişken fonksiyondan fonksiyona elden ele taşınmıyor. Birlikte gezen argümanlar bir sınıfın alanı oldu, fonksiyonlar onun metotları oldu. (Bl.2 · Add Meaningful Context: `GuessStatisticsMessage`; Bl.3 · Dyadic Functions: `FieldWriter`; Bl.10 · Cohesion) [ö: aynı parametre adı bir modülde 3 ya da daha fazla fonksiyonda geçiyorsa alarm]
- [ ] Tür üzerine dallanma, sözlükle dağıtım (`{"code": _sides, …}`) biçiminde bile olsa, sistemde tek yerde duruyor: bir fabrikanın dibinde (`Block.of` gibi). Davranış tür başına bir sınıfta. (Bl.3 · Switch Statements; G23) [ö: değerleri fonksiyon olan dizge anahtarlı sözlük alarmdır]
- [ ] Prosedürel biçim ancak Bl.6'nın gerekçesiyle seçildi: türler gerçekten sabit, yeni işlemler bekleniyor ve tür dallanması tek yerde. Bu gerekçe modülün belge dizgisinde yazılı; yazılı değilse varsayılan nesnedir. [o]
- [ ] Modül düzeyindeki fonksiyonlar ortak bir kavram etrafında toplanıyorsa o kavram sınıf oldu. Bir modül, adını hak eden bir nesnenin dağılmış metotlarından ibaret değil. (Bl.10 · Classes Should Be Small!, Cohesion) [o]

## 7 · Hata Yönetimi (Bl.7)
- [ ] Hata dönüş koduyla değil istisnayla bildiriliyor. (Bl.7 · Use Exceptions Rather Than Return Codes) [ö]
- [ ] İstisna fırlatabilen kodda önce `try` kapsamı çizildi. `except` programı tutarlı bir durumda bırakıyor. Önce istisnayı bekleyen bir test yazıldı (`assertRaises`). (Bl.7 · Write Your Try-Catch-Finally Statement First) [ö/o]
- [ ] Alt düzeyin istisna türü (`OSError`, kütüphane hataları) üst katmanlara sızmıyor; sınırda alan istisnasına çevriliyor. (Bl.7 · Use Unchecked Exceptions) [ö]
- [ ] İstisna bağlam taşıyor: mesajı başarısız olan işlemi söylüyor, `raise … from e` zinciri korunuyor. (Bl.7 · Provide Context with Exceptions) [ö]
- [ ] İstisna sınıfları çağıranın onları nasıl yakalayacağına göre tanımlandı. Ayrı bir sınıf yalnız biri yakalanırken öbürünün geçmesi istenince açılıyor. Üçüncü taraf istisnaları sarmalayıcıda tek bir türe çevriliyor. (Bl.7 · Define Exception Classes in Terms of a Caller's Needs) [ö]
- [ ] İş mantığında istisna akış denetimi için kullanılmıyor; özel durumu SPECIAL CASE nesnesi karşılıyor. (Bl.7 · Define the Normal Flow) [ö/o]
- [ ] `None` döndürülmüyor: istisna, boş koleksiyon ya da özel durum nesnesi döndürülüyor. `None` döndüren dış API sarmalanıyor. (Bl.7 · Don't Return Null) [ö]
- [ ] `None` argüman olarak geçilmiyor. (Bl.7 · Don't Pass Null) [ö]
- [ ] İstisna yutulmuyor: `except: pass` ya da yalnız loglayıp susan dal yok. (Bl.4 · Mumbling; G4) [ö]

## 8 · Sınırlar (Bl.8)
- [ ] Ham `dict` ya da dış kütüphane nesnesi sistemde elden ele dolaşmıyor; bir sınıfın ya da küçük bir ailenin içinde kalıyor. Public API sınır türü döndürmüyor ve almıyor. Dış paketi içe aktaran modül sayısı en az. (Bl.8 · Using Third-Party Code; Clean Boundaries) [ö]
- [ ] Sarmalayıcı uygulamanın ihtiyacına göre daraltıldı. Kitap "her Map'i sarmala" demez, "dolaştırma" der; tek yerde kalan kullanım sarmalanmaz. (Bl.8) [o]
- [ ] Dış API öğrenme testleriyle keşfedildi. Bu testler kütüphanenin yeni sürümünde yeniden koşuluyor. Gerçek PDF açan testler yalnız öğrenme testleridir. (Bl.8 · Exploring and Learning Boundaries, Learning Tests Are Better Than Free) [ö]
- [ ] Belirsiz ya da henüz var olmayan alt sistem için kendi dilimizde bir arayüz (`Protocol`) tanımlandı. Gerçek API ona ADAPTER ile bağlanıyor, testte bir Fake kullanılıyor. (Bl.8 · Using Code That Does Not Yet Exist) [ö/o]

## 9 · Birim Testleri (Bl.9, T1-T9)
- [ ] Üretim kodundan önce başarısız bir test yazıldı; test ve kod aynı commit'te. (Bl.9 · The Three Laws of TDD) [ö/o]
- [ ] Test kodu üretim koduyla aynı temizlik ölçütlerinden geçti; `measure_code.py` `tests/` üzerinde de koştu. (Bl.9 · Keeping Tests Clean) [ö]
- [ ] Her test BUILD-OPERATE-CHECK düzeninde. İlgisiz ayrıntı, alan diliyle adlandırılmış yardımcılara gizlendi; bu test dili yeniden düzenlemeden doğdu, baştan tasarlanmadı. (Bl.9 · Clean Tests, Domain-Specific Testing Language) [ö/o]
- [ ] Testte yalnız bellek ve işlemci verimliliği gevşeyebilir; temizlik gevşemez. (Bl.9 · A Dual Standard) [o]
- [ ] Test başına tek kavram var ve assert sayısı en az. Test adı o kavramı söylüyor. (Bl.9 · One Assert per Test, Single Concept per Test) [ö/o]
- [ ] F.I.R.S.T. (Bl.9 · F.I.R.S.T.; T9):
  - Fast: milisaniyede koşar; 100 ms'yi aşan test alarmdır.
  - Independent: sıra değişince de geçer.
  - Repeatable: PDF'e, Java'ya, `~/Desktop`'a, saate ya da tohumsuz rastgeleliğe bağlı değil.
  - Self-Validating: her testin assert'i var, `print` yok.
  - Timely: kodla birlikte yazıldı.

  [ö]
- [ ] Testler üretim nesnelerinin `_private` üyelerine dokunmuyor. (Bl.10 · Encapsulation) [ö]
- [ ] Bozulabilecek her şey test edildi. Önemsiz görünen testler atlanmadı. Atlanan her testin gerekçesi, gereksinim hakkında bir soru olarak yazıldı: `skip("soru: …")`. (T1, T3, T4) [ö/o]
- [ ] Kapsam aracı değişen dosyalarda koştu, çalışmayan dallar incelendi. (T2, T8) [ö]
- [ ] Sınırın iki yanı ayrı testlerle sınandı. Bulunan hatanın çevresi sıkı test edildi; başarısızlık örüntüsüne bakıldı. (T5, T6, T7; G3) [o]
- [ ] Bütün testler tek komutla koşuyor: `python3 -m unittest discover -s tests`. (E2) [ö]

## 10 · Sınıflar (Bl.10)
- [ ] Sınıf içi düzen şöyle: sabitler, sınıf değişkenleri, `__init__`, public metotlar; her public metodun yardımcısı onun hemen arkasında. (Bl.10 · Class Organization) [ö]
- [ ] **Sorumluluk sayısı bir.** Sınıfın boyu ne olursa olsun şunlar bakılır:
  - Metotlar kullandıkları alanlara ve birbirini çağırmalarına göre kümelenir; birbirine hiç dokunmayan iki küme, iki değişme nedeni adayıdır.
  - Sınıf "eğer, ve, veya, ama" kullanmadan yaklaşık 25 sözcükle anlatılabiliyor mu?

  (Bl.10 · Classes Should Be Small!, SRP) [ö/o]
- [ ] Uyum yüksek: alan sayısı az ve her metot alanların çoğunu kullanıyor. Alanların bir kısmını yalnız birkaç metot paylaşıyorsa bu, çıkarılmak isteyen bir sınıfın işaretidir. (Bl.10 · Cohesion, Maintaining Cohesion Results in Many Small Classes) [ö]
- [ ] Bir değişken yalnız argüman taşımamak için alana yükseltilmemiş. `__init__` dışında atanan alan yok. (Bl.10 · Maintaining Cohesion; G31) [ö]
- [ ] Yalnız bir public metoda hizmet eden özel yardımcı kümesi yok; varsa bu bir bölme adayıdır. (Bl.10 · Organizing for Change) [ö]
- [ ] Yeni tür eklemek var olan sınıfları açmıyor, yalnız yeni bir sınıf ekliyor (OCP). Ama mantıksal olarak tamam olan ve dokunulmayan sınıf "ileride lazım olur" diye bölünmedi; tasarımı değiştirmenin tetiği gerçek bir değişikliktir. (Bl.10 · Organizing for Change) [ö/o]
- [ ] Sınıf somut ayrıntıya değil soyutlamaya bağlı; değişen ya da yavaş bağımlılık yapıcıdan veriliyor, testte bir sahteyle değiştirilebiliyor. (Bl.10 · Isolating from Change, DIP) [ö]
- [ ] Yalnız kapsam için açılmış, bütün metotları static olan sınıf yok; kapsam için sınıf açılmaz, fonksiyonlar modülde durur. (Bl.10; G18) [ö]

## 11 · Sistemler (Bl.11)
- [ ] Kurulum ile kullanım ayrı. Nesne bağımlılığını kendisi kurmuyor ve aramıyor, yapıcıdan alıyor (DI). Bağlama işi tek bir yerde yapılıyor: `main` ya da `for_project` fabrikası. Hiçbir modül `main`'i içe aktarmıyor. (Bl.11 · Separate Constructing a System from Using It, Separation of Main, Dependency Injection) [ö]
- [ ] Gömülü tembel kurulum yok (`if self._x is None: self._x = Somut()`). Tembellik ancak ölçülmüş bir ihtiyaçla gelir. (Bl.11 · LAZY INITIALIZATION eleştirisi) [ö]
- [ ] Service locator (global kayıt sözlüğü, adla arama) DI'ın yerine kullanılmıyor. (Bl.11 · Dependency Injection) [ö]
- [ ] Nesnenin **ne zaman** kurulacağına uygulama, **nasıl** kurulacağına fabrika karar veriyor; fabrika dışarıdan veriliyor. (Bl.11 · Factories) [o]
- [ ] Alan nesneleri POJO: diski, çerçeveyi ya da dış kütüphaneyi bilmiyor. G/Ç kenarda. (Bl.11 · Scaling Up) [ö]
- [ ] Kesişen kaygılar (günlükleme, önbellek, yeniden deneme) alan koduna dağılmadan dekoratörle ya da sarmalayıcıyla tek bir yerde ekleniyor. Monkeypatch, `sys.meta_path` ya da metaclass gibi görünmez büyü yok. Sarmalayıcı sarmaladığı koddan karmaşık değil. (Bl.11 · Cross-Cutting Concerns, Java Proxies, Pure Java AOP) [ö/o]
- [ ] Önden büyük tasarım yapılmadı. Karar son sorumlu ana kadar ertelendi. Yeni standart ya da kütüphane gösterilebilir bir değer kattığı için eklendi. (Bl.11 · Test Drive the System Architecture, Optimize Decision Making, Use Standards Wisely) [o]
- [ ] Üst düzey kod alanın diliyle okunuyor. (Bl.11 · Systems Need Domain-Specific Languages; N2) [o]
- [ ] Çalışabilecek en basit şey yapıldı. (Bl.11 · Conclusion) [o]

## 12 · Ortaya Çıkış: Beck'in dört kuralı (Bl.12)
- [ ] **Kural 1:** Bütün testler geçiyor; kırmızıyken push yok. Test yazmak zorlaştıysa bu bir tasarım sinyali sayıldı (SRP, DI) ve kapsülleme gevşetilmedi. [ö/o]
- [ ] **Kural 2:** Tekrar yok.
  - Birebir aynı blok bir fonksiyona çıkarıldı.
  - Benzer satırlar önce birbirine benzetilip sonra ortaklaştırıldı.
  - Uygulama tekrarı kaldırıldı: aynı gerçeği iki durum izlemiyor (`is_empty` / `size`).
  - Çıkarılan küçük yardımcı başka bir sınıfa aitse oraya taşındı.
  - Aynı iskelet tek adımda ayrışıyorsa iskelet tek yerde.

  (Bl.12 · No Duplication; G5) [ö/o]
- [ ] **Kural 3:** Niyet açık: iyi adlar, küçük fonksiyon ve sınıflar, standart kalıp adları, örnekle belgeleyen testler. İkinci bir okuma yapıldı. (Bl.12 · Expressive) [o]
- [ ] **Kural 4:** Dogma yüzünden açılmış sınıf ya da metot yok. Tek gerçekleştirimi olan ve testte sahtesi de bulunmayan `Protocol`/`ABC` yok. Bu kural 1-3 ile çatışırsa geri çekilir. (Bl.12 · Minimal Classes and Methods) [ö]

## 13 · Eşzamanlılık (Bl.13): yalnız eşzamanlı kod içeren görevde
- [ ] Eşzamanlılık gerçekten gerekli: bölüşülecek bir bekleme payı var, "her zaman hızlandırır" efsanesine dayanılmadı. (Bl.13 · Why Concurrency?, Myths) [o]
- [ ] Eşzamanlılık kodu iş mantığından ayrı. Paylaşılan veri az ve kapsüllü. Kopya kullanılabilecekse kopya kullanıldı. Thread'ler kendi verisiyle çalışıyor. (Bl.13 · Concurrency Defense Principles) [ö/o]
- [ ] Hazır yapılar kullanıldı (`queue.Queue`, executor). Kilitsiz bir oku-değiştir-yaz (`self.n += 1`) yok. Kilitli bölümler küçük ve iç içe değil. (Bl.13 · Know Your Library, Keep Synchronized Sections Small) [ö]
- [ ] Problem bilinen bir modele uyduruldu (Producer-Consumer, Readers-Writers, Dining Philosophers). Aynı nesne üzerinde art arda yapılan çağrılar için kilitleme stratejisi seçildi: istemci kilitler, sunucu kilitler ya da uyarlanmış sunucu. (Bl.13 · Know Your Execution Models, Beware Dependencies Between Synchronized Methods) [o]
- [ ] Düzgün kapanma baştan tasarlandı: `join`/`get` için zaman aşımı ya da kuyruğa kapanma işareti var; `CancelledError` yutulmuyor. (Bl.13 · Writing Correct Shut-Down Code Is Hard) [ö]
- [ ] Önce thread'siz kod çalıştırıldı. Thread sayısı ayarlanabilir, bağımlılıklar değiştirilebilir. Arada bir düşen test "bir defalık" sayılmadı. Stres ve zorlama testleri birim takımında değil, ayrı bir koşuda. (Bl.13 · Testing Threaded Code) [ö/o]

## 14-16 · Artımlı İyileştirme ve vaka incelemeleri
- [ ] Yeni bir tür eklemek yalnız yeni sınıf ve fabrikada bir dal gerektiriyor. Her yeni tür N ayrı yere dokunmayı gerektirmeye başlayınca özellik eklemek durduruldu, önce yeniden düzenlendi. (Bl.14 · So I Stopped) [ö/o]
- [ ] Eski ve yeni yapı bir süre yan yana yaşatıldı, eskiler tek tek silindi. (Bl.14) [o]
- [ ] Yeniden düzenleme sırasında gerekirse bir önceki adım geri alındı; yeniden düzenleme deneme-yanılmayla yakınsar. (Bl.15) [o]
- [ ] +1/-1 hesabı tek bir adlı değişkende (G33). Olumsuz koşul yok (G29). Karmaşık koşul adlı bir fonksiyona çıktı (G28). [ö]
- [ ] Taban sınıf türevlerini tanımıyor (G7); türev yaratma işi fabrikada. Sabit grupları davranış taşıyan bir `Enum`'a dönüştü (J3). [ö]
- [ ] Yalnız testlerin çağırdığı üretim kodu, testiyle birlikte silindi. (Bl.16) [ö]
- [ ] Kod küçüldüğü için düşen kapsam yüzdesi gerileme sanılmadı. (Bl.16) [o]

## 17 · Kalan koku kodları (başka bölümde geçmeyenler)
- [ ] G1: Kaynak dosyadaki ikinci dil (HTML, CSS, SQL) en az ve en dar yerde. EPUB ve HTML üreten modüller için geçerli. [ö]
- [ ] G2: Adından beklenen bariz davranış uygulanmış. [o]
- [ ] G4: Emniyet kapatılmamış: `# noqa`, `# type: ignore`, susturulmuş uyarı, silinmiş test yok. [ö]
- [ ] G6: Kod doğru soyutlama düzeyinde; taban sınıfta ayrıntı yok. [o]
- [ ] G8: Arayüz dar: public üye, alan ve sabit sayısı az. [ö]
- [ ] G9 ve G12: Ölü kod, kullanılmayan import ya da değişken, boş yapıcı yok. [ö]
- [ ] G13: Genel bir sabit ya da enum kolaylık olsun diye özel bir sınıfa gömülmemiş. [o]
- [ ] G16, G19: Niyet gizlenmemiş; karmaşık hesap açıklayıcı ara değişkenlere bölünmüş. [o]
- [ ] G17: Kod, okuyucunun arayacağı yerde. [o]
- [ ] G18: `@staticmethod` yalnız polimorfik olma ihtimali olmayan saf fonksiyonda kullanılmış; şüphede örnek metodu seçilmiş. Bilinçli prosedürel modül fonksiyonu bu kokuya girmez. [ö]
- [ ] G21: Algoritma anlaşıldı; `if` ve bayrak yamasıyla "çalışır" hâle getirilmedi. [o]
- [ ] G22: Mantıksal bağımlılık fiziksel: gereken bilgi açıkça isteniyor, hakkında varsayım yapılmıyor. [o]
- [ ] G26: Kesin: para için `float` yok, "ilk eşleşme tektir" varsayımı yok. [ö/o]
- [ ] G27: Karar gelenekle değil yapıyla zorlanıyor (ABC, Protocol). [o]
- [ ] G32: Yapı keyfi değil; dışarıdan kullanılan sınıf başka bir sınıfın içine gömülmemiş. [ö/o]
- [ ] J1: Import listesi kısa, modül az şeye bağımlı. J2: Sabitler kalıtımla alınmıyor. J3: Anlamlı sabit grupları davranış taşıyan enum. [ö]
- [ ] E1: Proje tek adımda kuruluyor. [ö]

---

## Tasarım kalıpları ne zaman gelir?

**Genel ilke:** Kalıpların çoğu tekrarı kaldırmanın bilinen yollarıdır (G5). Kalıp ancak şunlardan biri doğunca gelir:
- kural 1-3'ten birinin somut ihlali: test yazılamıyor, tekrar var, niyet okunmuyor,
- sınıfı gerçekten açmaya zorlayan bir değişiklik.

**Frenler:**
- BDUF yapılmaz (Bl.11).
- En az öğe (Bl.12, kural 4).
- Bl.9'daki açık ret örneği: TEMPLATE METHOD "küçük bir sorun için fazla mekanizma" bulunup geri çevrilir.

**Adlandırma:** Kalıp uygulandıysa adı sınıf adında görünür (N3). Uygulanmadıysa kalıp adı kullanılmaz; aksi yanıltıcı olur.

| İhtiyaç / koku | Kalıp | Kitapta | Gelmemeli |
|---|---|---|---|
| Aynı tür dallanması birden çok yerde (G23, G5); taban sınıf türevini yaratıyor (G7) | ABSTRACT FACTORY + polimorfizm, tek switch | Bl.3 · Switch; Bl.11 · Factories; Bl.16 · DayDateFactory | Türler sabit, işlemler çoğalıyorsa (Bl.6): switch ya da prosedür yeter |
| Sabit türlere sık yeni işlem | VISITOR | Bl.6 dipnot 1 | Türler sık değişiyorsa; bedeli yapıyı prosedürele geri çevirmesidir |
| Aynı iskelet, bir adım farklı (üst düzey tekrar) | TEMPLATE METHOD | Bl.12 · No Duplication; G5 | Tek kopya varken; Bl.9'daki ret örneği |
| Satırları değil algoritması benzeyen kod | STRATEGY | G5 | Tek algoritma varsa |
| Normal akışı bölen `None` ya da istisna | SPECIAL CASE (NULL OBJECT, boş koleksiyon) | Bl.7 · Define the Normal Flow | Durum gerçekten bir hataysa istisna fırlatılır |
| Yabancı ya da henüz yazılmamış API; değiştirilemeyen sunucuya kilit eklemek | ADAPTER (+ seam ve Fake) | Bl.8; Bl.13 · Adapted Server | Sınır nesnesi tek yerde kalıyorsa gereksiz katman olur |
| Geniş dış arayüz sisteme yayılıyor | Sarmalayıcı sınıf (FACADE niteliğinde) | Bl.8 · Using Third-Party Code | "Her Map sarmalanmaz" |
| Kesişen kaygıyı POJO'ya dokunmadan eklemek | PROXY, iç içe DECORATOR | Bl.11 | Vekil karmaşası kodu kirletiyorsa; tek katmanda |
| Kurulum kullanıma karışmış | Separation of Main + DI | Bl.11 | DI kapsayıcısı gereksiz; service locator yarım bir çözüm |
| Pahalı kurulum | LAZY INITIALIZATION | Bl.11 | Ölçülmüş ihtiyaç yoksa; gömülü hâli SRP'yi ve test edilebilirliği bozar |
| Static API'yi koruyup uygulamayı değiştirilebilir tutmak | SINGLETON + DECORATOR + ABSTRACT FACTORY | Bl.16 | DI mümkünse; küresel durum testleri bağımlı kılar |
| Ağır ya da yavaş bağımlılık testi kırıyor | TEST DOUBLE / Fake / stub (DIP) | Bl.10, Bl.11, Bl.13 | Hızlı, saf ve değişmeyen bağımlılık için |
| Birlikte gezen argümanlar | Argüman nesnesi (VALUE OBJECT) | Bl.3 · Argument Objects | Doğal ikili (`Point(x, y)`) zaten tek kavramsa |
| Opak hesap | EXPLAINING TEMPORARY VARIABLE | Bl.16; G19 | — |
| Alan ile kod arasında iletişim boşluğu | DSL, test için alan dili | Bl.9, Bl.11 | Tek kullanım varsa |
| Paylaşılan kaynak | Producer-Consumer ve diğer modeller; client- veya server-based locking | Bl.13 | Bekleme payı yoksa eşzamanlılık hiç gerekmez |
| Davranış taşıyan sabit grubu | `Enum` + davranış | Bl.16; J3 | — |

---


## Haritaya eklenecekler (kitapta var, haritada yok)
Harita güncelleme kuralına göre, "önce kitaba sor" adımı bu okumayla yapıldı. Eklenmesi kullanıcı onayı bekliyor:
- **Bl.1:** LeBlanc yasası; Dave Thomas'ın "testi olmayan kod temiz değildir"; Jeffries'in erken basit soyutlaması.
- **Bl.2:** N2, N4, N7, G11; ölçü birimi adda; "add yerine append/insert".
- **Bl.3:** tek iş testi (içinden ad çıkarılabiliyor mu); tek argümana indirmenin üç yolu.
- **Bl.4:** yanlış yorumun hiç yorum olmamasından kötü olduğu.
- **Bl.5:** otomatik biçim aracı; 100-120 satır genişliği; Variable Declarations; G35.
- **Bl.6:** Demeter'in dört maddesi; zinciri bölmenin ihlali gidermediği; melez tanımı; VISITOR'ın bedeli.
- **Bl.7:** try'ın bir işlem olması; ayrı istisna sınıfının tek gerekçesi.
- **Bl.8:** sınır türü public API'ye çıkmaz; öğrenme testleri yeni sürümde yeniden koşulur.
- **Bl.9:** test dili yeniden düzenlemeden doğar; çifte standardın sınırı.
- **Bl.10:** alana yükseltilen değişken; tek public metoda hizmet eden yardımcılar; "tamamsa dokunma".
- **Bl.11:** LAZY INITIALIZATION eleştirisi; service locator; "en basit şey".
- **Bl.12:** uygulama tekrarı; ifadenin dört aracı.
- **Bl.13-16:** eşzamanlılık test maddeleri; Ek A; kapsam dersleri; DayDateFactory ve G7.
- **Bl.17:** G1, T7-T8, G5'in üç biçimi, "liste bir değer sistemidir".
