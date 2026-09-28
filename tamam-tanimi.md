# Tamam tanımı (Definition of Done)

Bir görev, bu listedeki bütün maddeler işaretlendiğinde biter. Bitince commit atılır ve push edilir.
Kaynak kitabın kendisidir ve kitap **standarttır**: kural dile ya da alışkanlığa göre gevşetilmez, istisna yalnız kitabın kendi verdiği istisnadır. Kitap 2026-09-25'te PDF ve LightRAG üzerinden, dört alt ajanla bölüm bölüm okundu. Madde sonundaki parantez maddenin kaynağını verir: bölüm ve kitaptaki başlık adı, varsa Bl.17'deki koku kodu.

- **[ö] Ölçülebilir:** AST ya da bir araçla mekanik olarak denetlenir (`measure_code.py`). Sonuç yalnız bir **alarmdır**, her alarm okunarak karara bağlanır.
- **[o] Okuma:** Kararı yargı verir; kod okunarak cevaplanır.

**Dil.** Liste nesne yönelimli diller içindir; şimdilik Python ve Java. Maddeler bu dillerin ortak sözcükleriyle yazılır: sınıf, nesne, alan, yapıcı, erişim düzeyi, arayüz, istisna, null. Örnek adlar kitabın Java yazımıyla verilir ki kaynağa dönülebilsin. Her kavramın dildeki karşılığı sondaki **Dil eşlemesi** tablosundadır. Yeni bir dil o tabloya sütun olarak girer, maddeler değişmez. Kitap her dilde standarttır.
- Bir dilde karşılığı olmayan madde tabloda "uygulanmaz" diye yazılır ve nedeni verilir; sessizce atlanmaz.
- Ölçüm aracı yalnız Python için var (`measure_code.py`). Aracı olmayan dilde [ö] maddeler okunarak denetlenir.

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
6. [ ] Ölçüm aracı değişen dosyalarda çalıştı. Her ALARM "gerçek, düzeltildi" ya da "yanlış pozitif, çünkü…" diye karara bağlandı. Aracı olmayan dilde [ö] maddeler tek tek okundu. [ö]
7. [ ] Aşağıdaki bölümler okundu; bulgular haritadaki başlık adıyla yazıldı.
8. [ ] Davranış değiştiyse gerçek çıktı (ör. EPUB) üretildi ve beklenen fark görüldü. Yeniden düzenlemeyse eski kodla karşılaştırıldı, fark çıkmadı. Fark çıktıysa önce o farkı gösteren birim testi yazıldı. (CLAUDE.md; T6)
9. [ ] Commit atomik: tek değişiklik, tek cümlelik Türkçe mesaj, gövde yok. Mesaja "ve" giriyorsa commit bölündü. Boy Scout temizliği ayrı bir commit oldu.

**Durma koşulu:** Bir madde sağlanamıyorsa, bir alarm için karar verilemiyorsa ya da kullanıcının vermesi gereken bir tasarım kararı çıktıysa commit atılmaz, kullanıcıya sorulur.

---

## 1 · Temiz Kod (Bl.1)
- [ ] Dokunulan her dosya bulunduğundan biraz daha temiz bırakıldı: bir ad iyileşti, bir fonksiyon bölündü, küçük bir tekrar kalktı ya da bir bileşik `if` sadeleşti. Önceki ölçümlere göre hiçbir değer kötüleşmedi. (Bl.1 · The Boy Scout Rule) [ö]
- [ ] Her TODO/FIXME tarandı ve yapılabilen kapatıldı. Kalan TODO, işin neden şimdi yapılamadığını ve kodun ne olacağını söylüyor. TODO, kötü kodu bırakmanın bahanesi değildir; "sonra" hiç gelmez. (Bl.1 · Bad Code; Bl.4 · TODO Comments) [ö]
- [ ] "Zaten kötüydü" diye bırakılan kırık cam yok. (Bl.1 · What Is Clean Code? — Stroustrup) [o]
- [ ] Her üretim modülünün ya da sınıfının testi var; testi olmayan kod temiz değildir. Bir işi yapmanın tek yolu var, API en küçük hâlinde. (Bl.1 · Dave Thomas) [ö/o]
- [ ] Birden çok yerde yapılan aynı iş, küçük ve basit bir soyutlamaya sarıldı. Genel bir API kurulmadı, yalnız gereken biçimler sunuldu. (Bl.1 · Jeffries) [o]
- [ ] Her rutin "aşağı yukarı beklendiği gibi" çıkıyor; kod düzyazı gibi okunuyor, spekülatif kod yok. (Bl.1 · Cunningham, Booch) [o]
- [ ] Kitaptan bilerek sapılan yer varsa gerekçesi CLAUDE.md'de yazılı. (Bl.1 · Schools of Thought) [o]
- [ ] Okuyucu için yazıldı; okuma/yazma oranı 10:1'den büyüktür. (Bl.1 · We Are Authors) [o]

## 2 · Anlamlı İsimler (Bl.2, N1-N7)
- [ ] Her ad neden var olduğunu, ne yaptığını ve nasıl kullanıldığını söylüyor; yorum istemiyor. Ölçü birimi adda (`elapsedTimeInDays`). (Bl.2 · Use Intention-Revealing Names; N1) [o] Satır sonu yorumlu atamalar [ö] ile yakalanır.
- [ ] Anlamlı indis ya da değer (`x[0] == 4`) adlı bir sabite ya da niyet gösteren bir metoda (`cell.isFlagged()`) dönüştü. (Bl.2 · Use Intention-Revealing Names; G25) [ö]
- [ ] Yanıltıcı ad yok: `accountList` gerçekten bir liste. Kap türü ada yazılmıyor. `l`, `O` ve `I` tek başına ad olarak kullanılmıyor. Az farkla benzeyen ad çiftleri yok. (Bl.2 · Avoid Disinformation) [ö]
- [ ] Yalnız derleyiciyi ya da yorumlayıcıyı susturmak için yapılmış ayrım yok: `a1/a2`, `klass`, gürültü sözcükler (`Info`, `Data`, `Object`, `theZork`, `NameString`). Hangisinin çağrılacağı belirsiz kardeşler yok (`getActiveAccount` / `getActiveAccounts` / `getActiveAccountInfo`). (Bl.2 · Make Meaningful Distinctions) [ö]
- [ ] Ad sesli okunup tartışılabiliyor. (Bl.2 · Use Pronounceable Names) [o]
- [ ] Ad uzunluğu kapsamla orantılı. Tek harfli ad yalnız kapsamı 5 satırı aşmayan yerel değişkende kullanılıyor; alanda, sabitte, modül düzeyinde ve parametrede kullanılmıyor. Aranacak her sabit adlı. (Bl.2 · Use Searchable Names; N5, G25) [ö]
- [ ] Adda kodlama yok: tür adı ya da Hungarian (`phoneString`, `strName`), üye öneki (`m_`), `I` önekli arayüz, alt sistem öneki. Bir şey kodlanacaksa arayüz değil uygulama kodlanır. (Bl.2 · Avoid Encodings; N6) [ö]
- [ ] Okuyucu hiçbir adı zihninde başka bir şeye çevirmek zorunda değil. Döngü sayacı dışında tek harfli ad yok. (Bl.2 · Avoid Mental Mapping) [ö]
- [ ] Sınıf adı bir isim ya da isim öbeği. Adında `Manager`, `Processor`, `Data`, `Info` ya da `Super` yok; kısa ve kesin bir ad verilemiyorsa sınıf büyüktür. (Bl.2 · Class Names; Bl.10) [ö]
- [ ] Metot adı bir fiil ya da fiil öbeği. `is`, `has` ve `can` ile başlayan adlar bool döndürüyor. Birden çok kurucu biçimi gerekiyorsa argümanı anlatan adlı bir statik fabrika metodu var (`Complex.FromRealNumber(23.0)`); dil izin veriyorsa karşılık gelen yapıcılar gizlenerek fabrika zorunlu kılındı. (Bl.2 · Method Names; G20) [ö]
- [ ] Espri, argo ya da kültüre bağlı ad yok. (Bl.2 · Don't Be Cute) [o]
- [ ] Bir kavram için tek sözcük kullanılıyor: `get`, `fetch`, `retrieve`, `load` bir arada değil. `manager` ile `controller` da öyle. (Bl.2 · Pick One Word per Concept; G11) [ö]
- [ ] Aynı sözcük iki anlamda kullanılmıyor: değer birleştiren `add` başka, koleksiyona öğe koyan `append`/`insert` başka. (Bl.2 · Don't Pun) [o]
- [ ] Teknik kavramda çözüm alanının adı (algoritma, kalıp: `AccountVisitor`, `JobQueue`), alan kavramında problem alanının adı kullanılıyor. Projenin ortak dili adlarda görünüyor. (Bl.2 · Use Solution/Problem Domain Names; N3) [o]
- [ ] Tek başına eksik kalan ad (`state`, `number`) bir sınıfın ya da modülün içine yerleşerek bağlam kazandı. Önek eklemek son çaredir. Uzun bir fonksiyonda birlikte gezen değişkenler bir sınıfın alanları oldu. (Bl.2 · Add Meaningful Context) [o/ö]
- [ ] Gereksiz bağlam yok: her sınıfa proje öneki eklenmiyor, paket adı sınıf adında tekrar etmiyor. (Bl.2 · Don't Add Gratuitous Context; N6) [ö]
- [ ] Ad uygulamayı değil soyutlama düzeyini söylüyor: `dial(phoneNumber)` yerine `connect(locator)`. (N2) [o]
- [ ] İç içe fonksiyonların adları farkı belirsizliksiz söylüyor. (N4) [o]
- [ ] Ad yan etkiyi söylüyor: nesneyi yaratıp döndüren fonksiyon `getOos` değil `createOrReturnOos`. (N7) [ö] `get`/`is` ile başlayıp atama ya da G/Ç yapan fonksiyonlar aranır.
- [ ] Daha iyi bir ad bulununca değiştirildi. (Bl.2 · Final Words) [o]

## 3 · Fonksiyonlar (Bl.3, F1-F4)

**Boyut ve yapı**
- [ ] Fonksiyon küçük: hedef 2-4 satır. 4'ü aşan fonksiyona bakılır, 20 satır tavandır. (Bl.3 · Small!) [ö]
- [ ] `if`, `else` ve `while` blokları tek satır; o satır adı iyi seçilmiş bir çağrı. Girinti en fazla 1-2 düzey. (Bl.3 · Blocks and Indenting) [ö]
- [ ] Fonksiyon tek iş yapıyor. İçinden, uygulamasını yeniden söylemekten öte bir ad taşıyan başka bir fonksiyon çıkarılamıyor. "TO paragrafı" testinden geçiyor. (Bl.3 · Do One Thing; G30) [o]
- [ ] Gövde boş satırla ya da başlık yorumuyla bölümlere ayrılmıyor. (Bl.3 · Sections within Functions) [ö]
- [ ] Tek soyutlama düzeyi: `getHtml()` ile `.append("\n")` aynı fonksiyonda değil. (Bl.3 · One Level of Abstraction; G34, G6) [o]
- [ ] Stepdown kuralı: çağıran üstte, çağrılan hemen altında; kod yukarıdan aşağı bir hikâye gibi okunuyor. (Bl.3 · The Stepdown Rule; Bl.5 · Vertical Ordering; G10) [ö]
- [ ] Ad ne yaptığını söylüyor; modüldeki adlar tutarlı bir hikâye kuruyor. Ad, birimi ve nesneyi değiştirip değiştirmediğini de söylüyor: `date.add(5)` değil; yerinde değiştiren `addDaysTo`, yeni değer döndüren `daysLater` ya da `plusDays` (Bl.16). Ne yaptığını anlamak için gövdeye ya da belgeye bakmak gerekiyorsa ad değişti ya da iş daha iyi adlı fonksiyonlara bölündü. (Bl.3 · Use Descriptive Names; G20) [o]

**Argümanlar**
- [ ] Argüman sayısı 0'dan (niladic, ideal) başlayarak 1'e (monadic) ve 2'ye (dyadic) çıkıyor. 3 argümandan (triadic) kaçınılır, gerekçe ister. 3'ten fazlası (polyadic) kullanılmaz. Alıcı nesne sayılmaz. Değişken sayılı argüman listesi bir argüman sayılır ve sınır onunla birlikte geçerlidir: `triad(String name, int count, Integer... args)` üçlüdür. Karşılıkları Dil eşlemesinde. (Bl.3 · Function Arguments; F1) [ö: 3 alarm, 4 ve üzeri ihlal]
- [ ] Tek argümanlı fonksiyon üç biçimden birine uyuyor:
  - soru sorar (`boolean fileExists("MyFile")`),
  - dönüştürür (girdi aynı kalsa bile yeni değer döndürür),
  - olaydır (değer döndürmez ve bunu adından belli eder).

  (Bl.3 · Common Monadic Forms) [ö/o]
- [ ] Bayrak argümanı yok: bool parametre fonksiyonu ikiye böler. Davranış seçen dizge, tamsayı ya da enum argümanı da aynı koku; çok sayıda fonksiyon, davranış seçen tek fonksiyondan iyidir. Çıktı biçimini seçen bayrak da ayrı fonksiyonlara bölündü (Bl.16 · `monthCodeToString` → `toString`, `toShortString`). (Bl.3 · Flag Arguments; F3, G15) [ö]
- [ ] İki argümanın doğal bir sırası ve uyumu var (`Point(x, y)`). Yoksa bir argüman düşürüldü. Kitap bunun üç yolunu verir: fonksiyonu argümanın metodu yapmak, argümanı alana çevirmek ya da argümanı yapıcıda alan bir sınıf çıkarmak (`FieldWriter`). (Bl.3 · Dyadic Functions) [o]
- [ ] Birlikte gezen argümanlar, adını hak eden bir kavrama sarıldı (`makeCircle(Point center, double radius)`). Aynı parametre çifti iki ya da daha fazla fonksiyonda geçiyorsa bu bir adaydır. (Bl.3 · Argument Objects) [ö]
- [ ] Fonksiyon adı argümanla bir fiil/isim çifti kuruyor (`writeField(name)`). Sıra belirsizse argümanların adı fonksiyon adına yazılıyor: anahtar sözcük biçimi (`assertExpectedEqualsActual(expected, actual)`). (Bl.3 · Verbs and Keywords) [o]

**Yan etki, CQS, hata**
- [ ] Adın söylemediği bir yan etki yok. Zamansal bağ kaçınılmazsa hem adda hem argüman zincirinde görünüyor. (Bl.3 · Have No Side Effects; N7, G31) [ö/o]
- [ ] Çıktı argümanı yok: argümanın alanına atanmıyor, içine öğe eklenmiyor. Durum değişecekse bu, sahibi olan nesnenin metodudur: `appendFooter(report)` değil `report.appendFooter()`. (Bl.3 · Output Arguments; F2) [ö]
- [ ] Komut ile sorgu ayrı: bir fonksiyon hem durum değiştirip hem değer döndürmüyor. (Bl.3 · Command Query Separation) [ö]
- [ ] Hata kodu ya da başarı bool'u döndürülmüyor, istisna fırlatılıyor. (Bl.3 · Prefer Exceptions to Returning Error Codes) [ö]
- [ ] `try` gövdesi ve yakalama bloğu ayrı fonksiyonlarda. Hatayı yöneten fonksiyon başka iş yapmıyor: `try` ilk deyim, yakalama ve `finally` bloklarından sonra bir şey yok. (Bl.3 · Extract Try/Catch Blocks; Error Handling Is One Thing) [ö]
- [ ] Herkesin içe aktardığı merkezi bir hata kodu enum'u yok; yeni hata, yeni bir istisna alt sınıfıdır. (Bl.3 · The Error.java Dependency Magnet) [ö]
- [ ] Tekrar yok. (Bl.3 · Don't Repeat Yourself; G5) [ö]
- [ ] Küçük fonksiyonda erken `return` serbest; tek giriş-tek çıkış ancak büyük fonksiyonda aranır. (Bl.3 · Structured Programming) [ö]
- [ ] Çağrılmayan fonksiyon silindi; sürüm kontrolü onu hatırlar, silmekten korkulmaz. Kullanılmadığı "Find Usages" gibi bir araçla görülür. Yalnız ikizinin çağırdığı fonksiyon onunla birleştirildi (`getMonths`). (Bl.16; F4) [ö]

**Tür dallanması**
- [ ] Bir tür için tek switch var: `switch`, `if/else` zinciri, tür sınaması zinciri ya da tabloyla dağıtım. O da fabrikanın dibinde durup polimorfik nesne üretiyor. Aynı ayırıcıya bakan ikinci bir dallanma alarmdır. (Bl.3 · Switch Statements; G23) [ö]

## 4 · Yorumlar (Bl.4, C1-C5)
- [ ] Her yorumdan önce kodla anlatmak denendi: yorumlanan koşul niyet gösteren bir fonksiyona, yorumlanan ifade açıklayıcı bir ara değişkene dönüştü. (Bl.4 · Explain Yourself in Code; Don't Use a Comment When You Can Use a Function or a Variable; G19, G28) [ö/o]
- [ ] Kalan yorum şu iyi türlerden biri:
  - lisansa kısa gönderme (Legal),
  - NEDEN'i anlatan niyet açıklaması (Explanation of Intent),
  - değiştirilemeyen koddaki belirsizliğin açıklaması, doğruluğu ayrıca denetlenmiş olarak (Clarification),
  - sonuç uyarısı (Warning of Consequences),
  - nedenini ve kodun ne olacağını söyleyen TODO (TODO Comments),
  - önemsiz görünen ama önemli bir ayrıntıyı vurgulama (Amplification).

  (Bl.4 · Good Comments) [o]
- [ ] Uyarı yapıya çevrilebiliyorsa çevrildi: yorumla kapatılmış test yerine test çatısının gerekçeli atlama işareti (`@Ignore("neden")`). (Bl.4 · Warning of Consequences; G27) [ö]
- [ ] Gerekli yorum yazılmış değil: bariz olanı tekrarlayan ya da yalnız imzayı sayan yorum ve belge yorumu yok. (Bl.4 · Redundant, Noise, Mandated Comments; C3) [ö]
- [ ] Yorumda başka bir kayıt sisteminin bilgisi yok: değişiklik günlüğü, yazar, son değişiklik tarihi, hata kaydı numarası. Bunlar sürüm kontrolünün ve hata takip sisteminin işi. Yorum, kod ve tasarım üzerine teknik nottur. Lisans ve telif yorumu kalır. (Bl.4 · Journal Comments, Attributions and Bylines; Bl.16; C1) [ö]
- [ ] Yoruma alınmış kod yok. (Bl.4 · Commented-Out Code; C5) [ö]
- [ ] `// Actions //////` gibi afiş yorumu, `} // while` gibi kapanış yorumu ya da yorumda HTML yok. (Bl.4 · Position Markers, Closing Brace Comments, HTML Comments) [ö]
- [ ] Yorum yalnız yanındaki kodu anlatıyor: sistemin uzak bir yerini, tarihçeyi ya da ilgisiz ayrıntıyı anlatmıyor. Yorumla kod arasındaki bağ açık. (Bl.4 · Nonlocal Information, Too Much Information, Inobvious Connection) [o]
- [ ] Anlamı için başka modüle bakmak gerektiren yorum yok. Gövdesi boş ya da yalnız yorum olan yakalama bloğu yok; bu aynı zamanda yutulan istisnadır. (Bl.4 · Mumbling) [ö]
- [ ] Dışa açık API'nin belge yorumu iyi. Dışa açık olmayan iç fonksiyonlarda `@param`/`@return` gibi biçimsel belge yorumu yok. (Bl.4 · Javadocs in Public APIs / in Nonpublic Code, Function Headers) [ö]
- [ ] Değişen kodun yanındaki yorum hâlâ doğru; eskiyen yorum hemen güncellendi ya da silindi. Kodun değişecek ayrıntısını anlatan, eskimeye yatkın yorum hiç yazılmadı. Yanlış yorum, hiç yorum olmamasından kötüdür. (Bl.4 · Misleading Comments; Bl.16; C2) [o]
- [ ] Yazmaya değen yorum iyi yazılmış: kısa, dolaşmadan, dilbilgisi ve noktalaması doğru, bariz olmayanı söylüyor. (C4) [o]

## 5 · Biçimlendirme (Bl.5, G10, G24)
- [ ] Biçim kuralı bir araçla uygulanıyor; ekibin tek bir kuralı var. **Bu depoda henüz bir araç yapılandırması yok.** (Bl.5 · Team Rules; G24) [ö]
- [ ] Dosya boyu tipik olarak 200 satır civarında, 500'ün altında. Bu bir alarmdır: 200'ün altında kalmak tek sorumluluğu kanıtlamaz. (Bl.5 · Vertical Formatting) [ö]
- [ ] Gazete düzeni: dosya adı tek başına yeterli, üstte genel kavram, aşağı indikçe ayrıntı. (Bl.5 · The Newspaper Metaphor) [ö/o]
- [ ] Kavramlar boş satırla ayrılıyor; birbirine sıkı bağlı satırlar yoğun duruyor. (Bl.5 · Vertical Openness, Vertical Density) [ö]
- [ ] Yerel değişken ilk kullanımının hemen üstünde, özel fonksiyon ilk çağrısının hemen altında. Döngü denetim değişkeni döngü deyiminin içinde bildiriliyor. Alanlar tek ve bilinen bir yerde bildiriliyor. Sıkı ilişkili kavramları dosyalara dağıtan protected alan yok. (Bl.5 · Vertical Distance, Variable Declarations, Dependent Functions; G10) [ö]
- [ ] Aynı işin türevlerini yapan fonksiyonlar yan yana duruyor. (Bl.5 · Conceptual Affinity) [ö/o]
- [ ] Satırlar kısa: 100-120 karakter kabul edilebilir, ötesi özensizliktir. (Bl.5 · Horizontal Formatting) [ö]
- [ ] Sütun hizası yok; hizalanmak istenen uzun liste, sınıfın bölünmesi gerektiğini gösterir. Kapsam tek satıra sıkıştırılmıyor: `if` ya da fonksiyon gövdesi başlığıyla aynı satırda değil. Boş gövde kendi satırında ve girintili. (Bl.5 · Horizontal Alignment, Breaking Indentation, Dummy Scopes) [ö]
- [ ] Bilinen bir sabit alt düzeye gömülmemiş; bilindiği yerden argümanla aşağı iniyor. (G35) [ö/o]

## 6 · Nesneler ve Veri Yapıları (Bl.6, G14, G36)
- [ ] Beklenen değişiklik adlandırıldı ve biçim buna göre seçildi:
  - yeni **tür** bekleniyorsa: nesne + polimorfizm,
  - yeni **işlem** bekleniyorsa: veri yapısı + fonksiyon.

  (Bl.6 · Data/Object Anti-Symmetry) [o]
- [ ] Sınıf alanlarını erişimcilerle dışarı itmiyor, verinin özünü işleyen soyut bir arayüz sunuyor ("galon" değil "kalan yakıt yüzdesi"). Düşünmeden eklenmiş getter/setter yok; birlikte değişen değerler tek bir işlemle ayarlanıyor. (Bl.6 · Data Abstraction; G8) [ö]
- [ ] **Melez yok.** Aynı sınıf hem açık durum hem anlamlı davranış taşımıyor; melez hem yeni türü hem yeni işlemi zorlaştırır. (Bl.6 · Hybrids; G14) [ö]
  - **Açık durum (A):** dışa açık alan, yalnız alanı döndüren erişimci (getter ya da property), yalnız alana atayan değiştirici (setter). Bağımlılık enjeksiyonu setter'ı sayılmaz: atadığı alan başka metotlarda işbirlikçi olarak çağrılıyor ve onu döndüren bir erişimci yok. Böyle bir setter durumu dışarı açmaz, işbirlikçiyi içeri alır.
  - **Anlamlı davranış (B):** erişimci olmayan, bir deyimden uzun ya da başkasını çağıran ya da durum değiştiren public metot. Dilin protokol metotları ve adlı kurucular sayılmaz.
  - **Kural:** A > 0 ve B > 0 ise melez adayıdır. Başka modüller bu sınıfın alanlarını okuyup karar veriyorsa melezlik gerçektir.
- [ ] Demeter: metot yalnız dört şeyle konuşuyor: kendi nesnesi, kendi kurduğu nesne, argümanı ve kendi alanı. Bir çağrının dönen değeri üzerinde yeni bir çağrı yapmıyor. (Bl.6 · The Law of Demeter; G36) [ö]
- [ ] Tren kazası yok (`a.b().c().d()`). Zinciri ara değişkenlere bölmek ihlali gidermez; iş nesneye taşınır: `ctxt.createScratchFileStream(classFileName)`. Demeter veri yapılarına uygulanmaz. (Bl.6 · Train Wrecks, Hiding Structure) [ö/o]
  - **Ölçüm nesnenin kökenine bakar.** Başka birinin döndürdüğü nesne, ister zincirde ister yerel bir adda dursun, yabancıdır. İki yazılış her zaman aynı kararı alır.
  - **Dost sayılan kurulan nesneler:**
    - sınıf kuruluşu;
    - ölçülen kaynakların fabrikaları: ad önce çağıranın kendi modülünde ve sınıfında çözülür, belirsiz ad alarm verir;
    - yeni nesne kuran standart kütüphane çağrıları. Kitabın `createScratchFileStream` çözümü de nesneye yeni bir nesne kurdurur;
    - bir tablodan seçilen sınıfla kurma: değerlerinin hepsi sınıf olan tablo, seçim varsayılanı da sınıfsa. Tek switch fabrikanın dibinde durur (Bl.3 · Switch Statements).
  - **Ölçümün bilerek görmedikleri okuma maddesidir:** yabancıyı argümanla bir yardımcıya verip orada çağırmak, alana koymak. Bunlar ihlali gidermez, yalnız yerini değiştirir. Koleksiyon öğesi (döngü öğesi, açılan demet) veri yapısına erişimdir.
- [ ] Metot başka bir nesnenin verisiyle kendi verisinden çok uğraşmıyor (feature envy); kıskandığı sınıfa taşındı (Bl.16 · `monthCodeToQuarter` → `Month.quarter()`). Kendi sınıfının türünden argüman alıp onu işleyen örnek metodu da kendi sınıfını kıskanır, gerçek örnek metodu yapıldı (Bl.16 · `getEndOfCurrentMonth`). İstisna, taşımanın tasarımı bozduğu yerdir: raporun biçim dizgesi çalışan sınıfına taşınmaz, çünkü çalışanı rapor biçimine bağlar (SRP, OCP, CCP). Bu gerekli bir kötülüktür. (G14) [ö/o]
- [ ] Veri taşıyıcı DTO (açık alanlı, fonksiyonsuz) davranışsız: üzerinde metot yok. Yalnız görünüş için yazılmış "bean" property'leri yok. (Bl.6 · Data Transfer Objects) [ö]
- [ ] Active Record'a (kaydet/yükle metotlu veri yapısı) iş kuralı konmamış; iş kuralı ayrı bir nesnede. (Bl.6 · Active Record) [ö]
- [ ] "Her şey nesnedir" efsanesine direnildi; saf veri zorla nesneye sarılmadı. (Bl.6) [o]

**Fonksiyon yazıp geçilmedi: sınıf tasarlandı.** Dil fonksiyona izin verir diye tasarım fonksiyona bırakılmaz. Kitabın sınıfa götüren işaretleri aranır:
- [ ] Aynı değişken fonksiyondan fonksiyona elden ele taşınmıyor. Birlikte gezen argümanlar bir sınıfın alanı oldu, fonksiyonlar onun metotları oldu. (Bl.2 · Add Meaningful Context: `GuessStatisticsMessage`; Bl.3 · Dyadic Functions: `FieldWriter`; Bl.10 · Cohesion) [ö: aynı parametre adı bir dosyada 3 ya da daha fazla fonksiyonda geçiyorsa alarm]
- [ ] Tür üzerine dallanma, tabloyla dağıtım (anahtarı tür kodu, değeri fonksiyon olan eşleme) biçiminde bile olsa, sistemde tek yerde duruyor: bir fabrikanın dibinde (`DayDateFactory` gibi). Davranış tür başına bir sınıfta. (Bl.3 · Switch Statements; G23) [ö: değerleri fonksiyon olan dizge anahtarlı eşleme alarmdır]
- [ ] Prosedürel biçim ancak Bl.6'nın gerekçesiyle seçildi: türler gerçekten sabit, yeni işlemler bekleniyor ve tür dallanması tek yerde. Bu gerekçe modülün ya da sınıfın baş belge yorumunda yazılı; yazılı değilse varsayılan nesnedir. [o]
- [ ] Sınıf dışı fonksiyonlar (Java'da tümü static sınıfın metotları) ortak bir kavram etrafında toplanıyorsa o kavram sınıf oldu. Bir modül, adını hak eden bir nesnenin dağılmış metotlarından ibaret değil. (Bl.10 · Classes Should Be Small!, Cohesion) [o]

## 7 · Hata Yönetimi (Bl.7)
- [ ] Hata dönüş koduyla değil istisnayla bildiriliyor. (Bl.7 · Use Exceptions Rather Than Return Codes) [ö]
- [ ] İstisna fırlatabilen kodda önce `try` kapsamı çizildi. Yakalama bloğu programı tutarlı bir durumda bırakıyor. Önce istisnayı bekleyen bir test yazıldı; test geçince yakalanan tür, fırlatılan gerçek türe daraltıldı. (Bl.7 · Write Your Try-Catch-Finally Statement First) [ö/o]
- [ ] Alt düzeyin istisna türü (G/Ç hataları, kütüphane hataları) üst katmanlara sızmıyor; sınırda alan istisnasına çevriliyor. (Bl.7 · Use Unchecked Exceptions) [ö]
- [ ] Uygulamanın kendi istisnaları denetimsiz. Denetimli istisna alt düzeyden imzalar boyunca yayılmıyor; kritik bir kütüphane yazılmıyorsa kullanılmıyor. Dilde denetimli istisna yoksa madde uygulanmaz. (Bl.7 · Use Unchecked Exceptions) [ö]
- [ ] İstisna bağlam taşıyor: mesajı başarısız olan işlemi söylüyor, özgün istisna neden (cause) olarak zincirde korunuyor. (Bl.7 · Provide Context with Exceptions) [ö]
- [ ] İstisna sınıfları çağıranın onları nasıl yakalayacağına göre tanımlandı. Ayrı bir sınıf yalnız biri yakalanırken öbürünün geçmesi istenince açılıyor. Üçüncü taraf istisnaları sarmalayıcıda tek bir türe çevriliyor. (Bl.7 · Define Exception Classes in Terms of a Caller's Needs) [ö]
- [ ] İş mantığında istisna akış denetimi için kullanılmıyor; özel durumu SPECIAL CASE nesnesi karşılıyor. (Bl.7 · Define the Normal Flow) [ö/o]
- [ ] Null döndürülmüyor: istisna, boş koleksiyon ya da özel durum nesnesi döndürülüyor. Null döndüren dış API sarmalanıyor. (Bl.7 · Don't Return Null) [ö]
- [ ] Null argüman olarak geçilmiyor. (Bl.7 · Don't Pass Null) [ö]
- [ ] İstisna yutulmuyor: boş yakalama bloğu ya da yalnız loglayıp susan dal yok. (Bl.4 · Mumbling) [ö]

## 8 · Sınırlar (Bl.8)
- [ ] Ham eşleme (`Map`) ya da dış kütüphane nesnesi sistemde elden ele dolaşmıyor; bir sınıfın ya da küçük bir ailenin içinde kalıyor. Public API sınır türü döndürmüyor ve almıyor. Dış pakete başvuran dosya sayısı en az. (Bl.8 · Using Third-Party Code; Clean Boundaries) [ö]
- [ ] Sarmalayıcı uygulamanın ihtiyacına göre daraltıldı. Kitap "her Map'i sarmala" demez, "dolaştırma" der; tek yerde kalan kullanım sarmalanmaz. (Bl.8) [o]
- [ ] Dış API öğrenme testleriyle keşfedildi. Bu testler kütüphanenin yeni sürümünde yeniden koşuluyor. Gerçek dış kaynağa dokunan testler yalnız öğrenme testleridir. Öğrenme gerekmese bile sınır, arayüzü üretim kodunun kullandığı gibi kullanan giden sınır testleriyle destekleniyor. (Bl.8 · Exploring and Learning Boundaries, Learning Tests Are Better Than Free) [ö]
- [ ] Belirsiz ya da henüz var olmayan alt sistem için kendi dilimizde bir arayüz tanımlandı. Gerçek API ona ADAPTER ile bağlanıyor, testte bir Fake kullanılıyor. (Bl.8 · Using Code That Does Not Yet Exist) [ö/o]

## 9 · Birim Testleri (Bl.9, T1-T9)
- [ ] Üretim kodundan önce başarısız bir test yazıldı; test ve kod aynı commit'te. (Bl.9 · The Three Laws of TDD) [ö/o]
- [ ] Test kodu üretim koduyla aynı temizlik ölçütlerinden geçti; ölçüm aracı test kodunda da koştu. (Bl.9 · Keeping Tests Clean) [ö]
- [ ] Her test BUILD-OPERATE-CHECK düzeninde. İlgisiz ayrıntı, alan diliyle adlandırılmış yardımcılara gizlendi; bu test dili yeniden düzenlemeden doğdu, baştan tasarlanmadı. (Bl.9 · Clean Tests, Domain-Specific Testing Language) [ö/o]
- [ ] Testte yalnız bellek ve işlemci verimliliği gevşeyebilir; temizlik gevşemez. (Bl.9 · A Dual Standard) [o]
- [ ] Test başına tek kavram var ve assert sayısı en az. Test adı o kavramı söylüyor. (Bl.9 · One Assert per Test, Single Concept per Test) [ö/o]
- [ ] F.I.R.S.T. (Bl.9 · F.I.R.S.T.; T9):
  - Fast: milisaniyede koşar; 100 ms'yi aşan test alarmdır (eşik kitapta yok, bizim alarmımız).
  - Independent: sıra değişince de geçer.
  - Repeatable: her ortamda koşar; dosya sistemindeki gerçek dosyalara, dış süreçlere, ağa, saate ya da tohumsuz rastgeleliğe bağlı değil.
  - Self-Validating: her testin assert'i var; sonuç konsola yazılıp gözle okunmuyor.
  - Timely: kodla birlikte yazıldı.

  [ö]
- [ ] Testler üretim nesnelerinin özel (private) üyelerine dokunmuyor. Test için erişim düzeyi gevşetmek son çaredir: önce gizliliği koruyan yol aranır, bulunamazsa yalnız aynı paketteki teste açılır. (Bl.10 · Encapsulation) [ö]
- [ ] Bozulabilecek her şey test edildi. Önemsiz görünen testler atlanmadı. Atlanan her testin gerekçesi, gereksinim hakkında bir soru olarak yazıldı: `@Ignore("soru: …")`. (T1, T3, T4) [ö/o]
- [ ] Kapsam aracı değişen dosyalarda koştu, çalışmayan dallar incelendi. (T2, T8) [ö]
- [ ] Sezgiye güvenilmedi: her sınır koşulu, köşe durumu ve istisna arandı; sınırın iki yanı ayrı testlerle sınandı. Bulunan hatanın çevresi sıkı test edildi; başarısızlık örüntüsüne bakıldı. (T5, T6, T7; G3) [o]
- [ ] Bütün testler tek komutla koşuyor; komut Dil eşlemesinde. (E2) [ö]

## 10 · Sınıflar (Bl.10)
- [ ] Sınıf içi düzen şöyle: sabitler, sınıf değişkenleri, alanlar, public metotlar; her public metodun yardımcısı onun hemen arkasında. Public alan yok; varsa gerekçesi yazılı. (Bl.10 · Class Organization) [ö]
- [ ] **Sorumluluk sayısı bir.** Sınıfın boyu ne olursa olsun şunlar bakılır:
  - Metotlar kullandıkları alanlara ve birbirini çağırmalarına göre kümelenir; birbirine hiç dokunmayan iki küme, iki değişme nedeni adayıdır.
  - Sınıf "eğer, ve, veya, ama" kullanmadan yaklaşık 25 sözcükle anlatılabiliyor mu?

  (Bl.10 · Classes Should Be Small!, SRP) [ö/o]
- [ ] Uyum yüksek: alan sayısı az ve her metot alanların çoğunu kullanıyor. Alanların bir kısmını yalnız birkaç metot paylaşıyorsa bu, çıkarılmak isteyen bir sınıfın işaretidir. (Bl.10 · Cohesion, Maintaining Cohesion Results in Many Small Classes) [ö]
- [ ] Argüman taşımamak için alana yükseltilen değişkenler uyumu düşürdüyse, onları paylaşan metotlar yeni bir sınıfa çıkarıldı. Her alan yapıcıda doğuyor; bir metotta ilk kez atanıp yalnız yardımcılarca okunan taşıyıcı alan yok. (Bl.10 · Maintaining Cohesion Results in Many Small Classes; G31) [ö]
- [ ] Yalnız bir public metoda hizmet eden özel yardımcı kümesi yok; varsa bu bir bölme adayıdır. (Bl.10 · Organizing for Change) [ö]
- [ ] Yeni tür eklemek var olan sınıfları açmıyor, yalnız yeni bir sınıf ekliyor (OCP). Ama mantıksal olarak tamam olan ve dokunulmayan sınıf "ileride lazım olur" diye bölünmedi; tasarımı değiştirmenin tetiği gerçek bir değişikliktir. (Bl.10 · Organizing for Change) [ö/o]
- [ ] Sınıf somut ayrıntıya değil soyutlamaya bağlı; değişen ya da yavaş bağımlılık dışarıdan (yapıcı ya da setter ile) veriliyor, testte bir sahteyle değiştirilebiliyor. (Bl.10 · Isolating from Change, DIP) [ö]
- [ ] Dil sınıf dışı fonksiyona izin veriyorsa yalnız kapsam için açılmış, bütün metotları static olan sınıf yok; fonksiyonlar modülde durur. İzin vermiyorsa tümü static sınıf modülün karşılığıdır (`PrimeGenerator`). (Bl.10; G18) [ö]

## 11 · Sistemler (Bl.11)
- [ ] Kurulum ile kullanım ayrı. Nesne bağımlılığını kendisi kurmuyor ve aramıyor; tamamen edilgen. Bağımlılık yapıcı argümanıyla, setter ile ya da ikisiyle veriliyor (DI). Bağlama işi tek bir yerde yapılıyor: giriş noktası (`main`) ya da onun çağırdığı kurulum fabrikası. Uygulama giriş noktasını bilmiyor; bağımlılık okları `main`'den uzağa gider. (Bl.11 · Separate Constructing a System from Using It, Separation of Main, Dependency Injection) [ö]
- [ ] Setter ile verilen bağımlılık kitabın öbür kurallarını bozmuyor. Kitap iki yolu da tanır (s.157), ama setter şu kuralları bozmaya açıktır:
  - Nesne setter çağrılmadan çalışamıyorsa bu gizli bir zamansal bağdır. Zorunlu bağımlılık yapıcıdan verilir. Setter, yapıcının kurduğu çalışır bir varsayılanı değiştirmek içindir. (G31 · Hidden Temporal Couplings)
  - Alan yine yapıcıda doğuyor, setter yalnız değerini değiştiriyor. (Bl.5 · Variable Declarations)
  - Varsayılan null değil. Anlamlı bir varsayılan gerçekleştirim ya da SPECIAL CASE nesnesi kullanılıyor. (Bl.7 · Don't Pass Null, Define the Normal Flow)
  - Enjekte edilen alanı döndüren bir getter yok. İşbirlikçi dışarı verilirse Demeter zinciri başlar, sınıf da melez olur. (Bl.6 · Hybrids, The Law of Demeter)

  (Bl.11 · Dependency Injection) [ö/o]
- [ ] Gömülü tembel kurulum yok (`if (service == null) service = new MyServiceImpl(...);`). Tembellik ancak ölçülmüş bir ihtiyaçla gelir. (Bl.11 · LAZY INITIALIZATION eleştirisi) [ö]
- [ ] Service locator (global kayıt sözlüğü, adla arama) DI'ın yerine kullanılmıyor. (Bl.11 · Dependency Injection) [ö]
- [ ] Nesnenin **ne zaman** kurulacağına uygulama, **nasıl** kurulacağına fabrika karar veriyor; fabrika dışarıdan veriliyor. (Bl.11 · Factories) [o]
- [ ] Alan nesneleri düz nesne (POJO): diski, çerçeveyi ya da dış kütüphaneyi bilmiyor. Çerçeve türünden türemiyor, çerçevenin yaşam döngüsü metotlarını uygulamıyor, iş metodunda bağımlılık aramıyor. G/Ç kenarda. Çerçevenin eşleme bilgisi (Java `@Entity`) eşleme sık değişmiyorsa sınıfta kalabilir; tam düz nesne için dış yapılandırmaya taşınır. (Bl.11 · Scaling Up, Pure Java AOP Frameworks, EJB3) [ö]
- [ ] Kesişen kaygılar (günlükleme, önbellek, yeniden deneme) alan koduna dağılmadan, hedef kod elle değiştirilmeden sarmalayıcıyla (DECORATOR, PROXY) tek bir yerde ekleniyor. Sarmalayıcı sarmaladığı koddan karmaşık değil; kitap vekil kodunun hacmini ve karmaşıklığını temiz kodun önünde engel sayar. Bu eleştiriden türeyen bir yasak da var (kitapta açıkça yok): çalışma anında sınıf ya da modül yamama, özel yükleyici ya da sınıf üreten gizli mekanizma gibi görünmez büyü yok. (Bl.11 · Cross-Cutting Concerns, Java Proxies, Pure Java AOP) [ö/o]
- [ ] Önden büyük tasarım yapılmadı. Karar son sorumlu ana kadar ertelendi. Yeni standart ya da kütüphane gösterilebilir bir değer kattığı için eklendi. (Bl.11 · Test Drive the System Architecture, Optimize Decision Making, Use Standards Wisely) [o]
- [ ] Üst düzey kod alanın diliyle okunuyor. (Bl.11 · Systems Need Domain-Specific Languages; N2) [o]
- [ ] Çalışabilecek en basit şey yapıldı. (Bl.11 · Conclusion) [o]

## 12 · Ortaya Çıkış: Beck'in dört kuralı (Bl.12)
- [ ] **Kural 1:** Bütün testler geçiyor; kırmızıyken push yok. Test yazmak zorlaştıysa bu bir tasarım sinyali sayıldı (SRP, DI) ve kapsülleme gevşetilmedi. [ö/o]
- [ ] **Kural 2:** Tekrar yok.
  - Birebir aynı blok bir fonksiyona çıkarıldı.
  - Benzer satırlar önce birbirine benzetilip sonra ortaklaştırıldı.
  - Uygulama tekrarı kaldırıldı: aynı gerçeği iki durum izlemiyor (`isEmpty` / `size`).
  - Çıkarılan küçük yardımcı başka bir sınıfa aitse oraya taşındı.
  - Aynı iskelet tek adımda ayrışıyorsa iskelet tek yerde.
  - Aynı koşulları sınayan `switch`/`if` zinciri birden çok yerde tekrarlanmıyor; yerini polimorfizm aldı (G23).
  - Satırları değil algoritması benzeyen modüller TEMPLATE METHOD ya da STRATEGY ile ortaklaştı.
  - Her fonksiyonda tekrarlanan geçerlilik denetimi, değeri taşıyan bir türle (enum) kalktı (Bl.16 · `Month`).

  (Bl.12 · No Duplication; G5) [ö/o]
- [ ] **Kural 3:** Niyet açık: iyi adlar, küçük fonksiyon ve sınıflar, standart kalıp adları, örnekle belgeleyen testler. İkinci bir okuma yapıldı. (Bl.12 · Expressive) [o]
- [ ] **Kural 4:** Dogma yüzünden açılmış sınıf ya da metot yok. Tek gerçekleştirimi olan ve testte sahtesi de bulunmayan arayüz ya da soyut sınıf yok. Alan ile davranış dogma yüzünden veri sınıflarına ve davranış sınıflarına ayrılmadı. Bu kural 1-3 ile çatışırsa geri çekilir. (Bl.12 · Minimal Classes and Methods) [ö]

## 13 · Eşzamanlılık (Bl.13): yalnız eşzamanlı kod içeren görevde
- [ ] Eşzamanlılık gerçekten gerekli: bölüşülecek bir bekleme payı var, "her zaman hızlandırır" efsanesine dayanılmadı. (Bl.13 · Why Concurrency?, Myths) [o]
- [ ] Eşzamanlılık kodu iş mantığından ayrı. Paylaşılan veri az ve kapsüllü. Kopya kullanılabilecekse kopya kullanıldı. Thread'ler kendi verisiyle çalışıyor. (Bl.13 · Concurrency Defense Principles) [ö/o]
- [ ] Hazır yapılar kullanıldı: iş parçacığı güvenli koleksiyon, kuyruk, executor. Korumasız bir oku-değiştir-yaz (`++lastIdUsed`) yok. İş parçacığı güvenli olmayan kütüphane sınıfları paylaşılmadı. Kilitli bölümler küçük ve iç içe değil. (Bl.13 · Know Your Library, Keep Synchronized Sections Small) [ö]
- [ ] Problem bilinen bir modele uyduruldu (Producer-Consumer, Readers-Writers, Dining Philosophers). Aynı nesne üzerinde art arda yapılan çağrılar için kilitleme stratejisi seçildi: istemci kilitler, sunucu kilitler ya da uyarlanmış sunucu. Tek tek güvenli çağrılardan kurulan bileşik işlem (`containsKey` + `put`) güvenli sayılmadı; tek bir atomik çağrı (`putIfAbsent`) ya da kilit kullanıldı. (Bl.13 · Know Your Execution Models, Beware Dependencies Between Synchronized Methods) [o]
- [ ] Düzgün kapanma baştan tasarlandı: bekleyen her birleştirme ve sonuç alma için zaman aşımı ya da kuyrukta kapanma işareti var; iptal ya da kesinti sinyali yutulmuyor. (Bl.13 · Writing Correct Shut-Down Code Is Hard) [ö]
- [ ] Önce thread'siz kod çalıştırıldı. Thread sayısı ayarlanabilir, bağımlılıklar değiştirilebilir. Arada bir düşen test "bir defalık" sayılmadı. İşlemci sayısından fazla thread ile ve bütün hedef platformlarda erken ve sık koşuldu; kod zorlamayla (jiggling) sınandı. Stres ve zorlama testleri birim takımında değil, ayrı bir koşuda. (Bl.13 · Testing Threaded Code) [ö/o]

## 14-16 · Artımlı İyileştirme ve vaka incelemeleri
- [ ] Yeni bir tür eklemek yalnız yeni sınıf ve fabrikada bir dal gerektiriyor. Her yeni tür N ayrı yere dokunmayı gerektirmeye başlayınca özellik eklemek durduruldu, önce yeniden düzenlendi. (Bl.14 · So I Stopped) [ö/o]
- [ ] Eski ve yeni yapı bir süre yan yana yaşatıldı, eskiler tek tek silindi. (Bl.14) [o]
- [ ] Yeniden düzenleme sırasında gerekirse bir önceki adım geri alındı; yeniden düzenleme deneme-yanılmayla yakınsar. (Bl.15) [o]
- [ ] +1/-1 hesabı tek bir adlı değişkende (G33). Olumsuz koşul yok (G29). Karmaşık koşul adlı bir fonksiyona çıktı (G28). [ö]
- [ ] Taban sınıf türevlerini tanımıyor (G7); türev yaratma işi fabrikada. Tek istisna, türev sayısının kesin sabit olduğu durumdur (sonlu durum makinesi); o zaman taban ve türevler aynı dağıtım biriminde durur. Sabit grupları davranış taşıyan bir enum'a dönüştü (J3). [ö]
- [ ] Yalnız testlerin çağırdığı üretim kodu, testiyle birlikte silindi. (Bl.16) [ö]
- [ ] Kod küçüldüğü için düşen kapsam yüzdesi gerileme sanılmadı. (Bl.16) [o]

## 17 · Kalan koku kodları (başka bölümde geçmeyenler)
- [ ] G1: İdeal olan, kaynak dosyada tek dil. Kaçınılmaz ikinci dil (HTML, CSS, SQL) hem sayıca hem kapladığı yerce en az. Her kaynak dosya için geçerli; kitabın örnekleri Java dosyasına gömülü XML, HTML, YAML ve JavaScript'tir. Belge yorumundaki HTML de ikinci dildir (Bl.16). [ö]
- [ ] G2: Başka bir programcının makul olarak bekleyeceği davranış uygulanmış (en az sürpriz ilkesi): gün adını çeviren fonksiyon kısaltmayı da tanır, büyük-küçük harfe bakmaz. Bariz olduğu belli olmayan beklenti (`tues`, `thurs`) uygulanmadı, soru olarak bırakıldı. (Bl.16) [o]
- [ ] G4: Emniyet kapatılmamış: derleyici, tür denetleyici ya da linter uyarısı susturulmamış; başarısız test kapatılmamış ya da silinmemiş. Emniyeti elle yönetmek her zaman risklidir: otomatik denetim varsa o seçildi, elle yönetilen ayar (Java `serialVersionUID`) gerekçeli. (Bl.16) [ö]
- [ ] G6: Üst ve alt düzey kavramların ayrımı tam. Yalnız bir gerçekleştirmeye ait sabit, değişken ve yardımcı fonksiyon türevde; gerçekleştirmeye bağlı olmayan kod tabanda. Aynısı dosya, modül ve bileşen için de geçerli. Yanlış düzeydeki soyutlama sahte değerle kapatılmadı: sınırsız bir yığında `percentFull()` 0 döndürmez, metot ayrı bir arayüze (`BoundedStack`) gider. (Bl.16) [o]
- [ ] G8: Arayüz dar: public üye, alan ve sabit sayısı az; sınıfın metodu ve örnek değişkeni az. Veri, yardımcı fonksiyon, sabit ve ara değer gizli. Aynı veriyi sunan bir fonksiyon varken tablo dışarı açılmamış (Bl.16 · `LAST_DAY_OF_MONTH`). Alt sınıflar için çok sayıda protected alan ve fonksiyon açılmamış. Fonksiyonun bildiği değişken sayısı az. [ö]
- [ ] G9 ve G12: Ölü kod yok: hiç fırlatmayan `try`'ın yakalama bloğu, gerçekleşmeyen koşulun ya da `switch` durumunun dalı, çağrılmayan fonksiyon, erişimcileriyle birlikte kullanılmayan alan. Tasarım değişince anlamsızlaşan kod da ölüdür: enum gelince geçerlilik denetimi (`isValidMonthCode`) silinir. Ölü olduğundan şüphelenilen koşul kaldırılıp testler koşularak sınandı (Bl.15 · `compactString`). Kullanılmayan import ya da değişken, boş varsayılan yapıcı, değer katmayan niteleyici (Java'da argüman ve yerel değişkendeki `final`) yok. (Bl.15, Bl.16) [ö]
- [ ] G11: Benzer işler aynı biçimde yapılıyor. Aynı türdeki nesne her fonksiyonda aynı adı taşıyor (`response`); benzer metotların adları benzer (`processVerificationRequest`, `processDeletionRequest`). Kardeş fonksiyonlar aynı geleneği izliyor: biri değer döndürürken öbürü alana yazmıyor (Bl.15). Yeni ya da düzeltilen kod, dosyada yerleşmiş kalıba uyuyor (Bl.16). [o]
- [ ] G13: Genel bir sabit, enum ya da genel amaçlı statik fonksiyon, kolaylık olsun diye özel bir sınıfa gömülmemiş. Fonksiyonun, sabitin ve değişkenin nerede bildirileceği düşünüldü, el altındaki yere atılmadı. Özel sınıfa bağlı olmayan kavram kendi dosyasında (Bl.16 · `Day` enum'u `DayDate`'ten çıktı). [o]
- [ ] G16, G19: Niyet gizlenmemiş: uzun tek ifade, Macar gösterimi (`m_otCalc`, `iThsWkd`) ve sihirli sayı yok. Küçük ve yoğun olan değil, okunan kod seçildi. Karmaşık hesap açıklayıcı ara değişkenlere bölünmüş (`match.group(1)` → `key`); bunun fazlası zor olur, çoğu azından iyidir. (Bl.16) [o]
- [ ] G17: Kod, okuyucunun arayacağı yerde (en az sürpriz): `PI` trigonometri fonksiyonlarının yanında, `OVERTIME_RATE` ücret hesaplayıcısında, `LAST_DAY_OF_MONTH` `Month` enum'unda (Bl.16). Yer, yazana kolay geldiği için değil, fonksiyon adlarının söylediğine göre seçildi: toplam saati `saveTimeCard` değil `getTotalHours` hesaplar. Performans yüzünden başka yerde hesaplanıyorsa ad bunu söyler (`computeRunningTotalOfHours`). [o]
- [ ] G18: Statik metot yalnız polimorfik olma ihtimali olmayan, bütün verisini argümandan alan fonksiyonda kullanılmış (`Math.max`); şüphede örnek metodu seçilmiş. Bütün verisini argümandan alsa bile farklı algoritmalarla çalışma ihtimali olan fonksiyon (`HourlyPayCalculator.calculatePay(employee, overtimeRate)`) örnek metodudur. Sınıfın kendi verisiyle çalışan fonksiyon static değil (Bl.16 · `addDays`). Bilinçli prosedürel sınıf dışı fonksiyon bu kokuya girmez. [ö]
- [ ] G21: Algoritma anlaşıldı; `if` ve bayrak yamasıyla "çalışır" hâle getirilmedi. Deneyerek çalıştırmak serbest, ama iş bitmeden nasıl çalıştığı bilindi: testlerin geçmesi yetmez. Algoritmanın uygun olup olmadığından emin olamamak olağandır; kodun ne yaptığını bilmemek tembelliktir. Anlamanın yolu, fonksiyonu nasıl çalıştığı apaçık olana dek yeniden düzenlemektir. (Bl.16 · `getPreviousDayOfWeek`) [o]
- [ ] G22: Mantıksal bağımlılık fiziksel: gereken bilgi açıkça isteniyor, hakkında varsayım yapılmıyor. `HourlyReporter` sayfa boyunu (`PAGE_SIZE = 55`) kendi bilmez, biçimleyiciye sorar (`formatter.getMaxPageSize()`); bu aynı zamanda yanlış yerdeki sorumluluktur (G17). Gerçekleştirmenin bir ayrıntısına örtük dayanan genel algoritma, o ayrıntıyı soyut bir metotla ister (Bl.16 · `getDayOfWeekForOrdinalZero`). [o]
- [ ] G26: Kesin: para için kayan noktalı sayı yok, "ilk eşleşme tektir" varsayımı yok. Boş dönebilecek çağrı denetlenmiş. Eşzamanlı güncelleme olasıysa kilit var. Değişken gereğinden somut türle bildirilmemiş (`List` yeterken `ArrayList`); erişim de gereğinden geniş değil. [ö/o]
- [ ] G27: Karar gelenekle değil yapıyla zorlanıyor: adlandırılmış enum üzerinde switch yerine soyut metotlu taban sınıf. [o]
- [ ] G32: Yapı keyfi değil; dışarıdan kullanılan sınıf başka bir sınıfın içine gömülmemiş. [ö/o]
- [ ] J1: İçe aktarma listesi, birlikte çalışılan paketlerin kısa bir beyanı. Aynı paketten iki ya da daha fazla sınıf kullanılıyorsa sınıflar tek tek değil, paket olarak içe aktarılıyor; dile göre biçimi Dil eşlemesinde. J2: Sabitler kalıtımla alınmıyor. J3: Anlamlı sabit grupları davranış taşıyan enum. [ö]
- [ ] E1: Depo tek komutla alınıyor, proje tek komutla kuruluyor. Elle aranacak ek kütüphane ya da dosya, sırayla çalıştırılacak gizemli komut dizisi yok. Komut Dil eşlemesinde. [ö]

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
| Normal akışı bölen null ya da istisna | SPECIAL CASE (NULL OBJECT, boş koleksiyon) | Bl.7 · Define the Normal Flow | Durum gerçekten bir hataysa istisna fırlatılır |
| Yabancı ya da henüz yazılmamış API; değiştirilemeyen sunucuya kilit eklemek | ADAPTER (+ seam ve Fake) | Bl.8; Bl.13 · Adapted Server | Sınır nesnesi tek yerde kalıyorsa gereksiz katman olur |
| Geniş dış arayüz sisteme yayılıyor | Sarmalayıcı sınıf (FACADE niteliğinde) | Bl.8 · Using Third-Party Code | "Her Map sarmalanmaz" |
| Kesişen kaygıyı düz nesneye (POJO) dokunmadan eklemek | PROXY, iç içe DECORATOR | Bl.11 | Vekil karmaşası kodu kirletiyorsa; tek katmanda |
| Kurulum kullanıma karışmış | Separation of Main + DI | Bl.11 | DI kapsayıcısı gereksiz; service locator yarım bir çözüm |
| Pahalı kurulum | LAZY INITIALIZATION | Bl.11 | Ölçülmüş ihtiyaç yoksa; gömülü hâli SRP'yi ve test edilebilirliği bozar |
| Static API'yi koruyup uygulamayı değiştirilebilir tutmak | SINGLETON + DECORATOR + ABSTRACT FACTORY | Bl.16 | DI mümkünse; küresel durum testleri bağımlı kılar |
| Ağır ya da yavaş bağımlılık testi kırıyor | TEST DOUBLE / Fake / stub (DIP) | Bl.10, Bl.11, Bl.13 | Hızlı, saf ve değişmeyen bağımlılık için |
| Birlikte gezen argümanlar | Argüman nesnesi (VALUE OBJECT) | Bl.3 · Argument Objects | Doğal ikili (`Point(x, y)`) zaten tek kavramsa |
| Opak hesap | EXPLAINING TEMPORARY VARIABLE | Bl.16; G19 | — |
| Alan ile kod arasında iletişim boşluğu | DSL, test için alan dili | Bl.9, Bl.11 | Tek kullanım varsa |
| Paylaşılan kaynak | Producer-Consumer ve diğer modeller; client- veya server-based locking | Bl.13 | Bekleme payı yoksa eşzamanlılık hiç gerekmez |
| Davranış taşıyan sabit grubu | enum + davranış | Bl.16; J3 | — |

---

## Dil eşlemesi

Maddelerdeki ortak kavramın her dildeki karşılığı. Yeni bir dil bu tabloya sütun olarak girer. Java sütunu kitaptan gelir; sayfa numarası kitaptaki örneği gösterir, dilin temel sözdizimi (yapıcı, `catch`, `//`) için sayfa verilmez. Kitapta geçmeyen kural ya da araç "(kitapta yok)" diye işaretlidir. Karşılığı olmayan hücre "uygulanmaz" der ve nedenini verir.

**Adlar ve fonksiyonlar**

| Kavram | Python | Java |
|---|---|---|
| Ad yazımı | fonksiyon ve değişken `snake_case`, sınıf `PascalCase`: `elapsed_time_in_days` | fonksiyon ve değişken `camelCase`, sınıf `PascalCase`: `elapsedTimeInDays` (s.18). Maddelerdeki örnekler bu yazımla verilir. |
| Yüklem adı önekleri | `is_`, `has_`, `can_` | `is`, `has`, `can`; erişimci adları `get`/`set`/`is` (s.25) |
| Adlı kurucu | `@classmethod` fabrikası: `from_real_number(...)` | statik fabrika metodu: `Complex.FromRealNumber(23.0)` (s.25) |
| Fabrikayı zorunlu kılmak | uygulanmaz: `__init__` gizlenemez, yalnız adla gelenek kurulur | `private` yapıcı (s.25) |
| Alıcı nesne (argüman sayılmaz) | `self`, `cls` | `this`; imzada görünmez |
| Değişken sayılı argüman | `*args` bir, `**kwargs` bir argüman | `Object... args` bir argüman (s.43) |
| Anahtar sözcüklü argüman | Dilin aracıdır, argüman sayısına girer. Sıra belirsizliği önce adla çözülür. | uygulanmaz: dilde adlı argüman yok, belirsizliği yalnız ad çözer (s.43) |
| Değer döndürmeyen fonksiyon | `None` döner | `void` (s.41) |
| Tür sınaması | `isinstance`, `match` | `instanceof`, `switch` (s.38) |
| Tabloyla dağıtım | değerleri fonksiyon olan `dict` | değerleri fonksiyon ya da nesne olan `Map` (kitapta yok) |
| Tek satıra sıkıştırılmış kapsam | aynı satırda `if x: y`, `def f(): return x`; `lambda` ataması (PEP 8, kitapta yok) | `{return "";}` tek satırda (s.89). `lambda` ataması: uygulanmaz, Java'da olağan kullanımdır. |
| Boş gövde | ayrı satırda `pass` | ayrı satırda, girintili `;` (s.90) |
| Döngü denetim değişkeni | uygulanmaz: `for` değişkeni zaten döngü deyiminde doğar | `for (int i = 0; …)` (s.80) |
| Değer katmayan niteleyici (G12) | uygulanmaz: `final` anahtar sözcüğü yok | argüman ve yerel değişkendeki `final` (s.276) |
| Yorum işareti | `#` | `//`, `/* */` |
| Kapanış yorumu | `# end while` | `} // while` (s.67) |
| Belge yorumu | docstring, `Args:`/`Returns:` | Javadoc, `@param`/`@return` (s.63, 71) |
| Biçimlendirici | black ya da ruff (kitapta yok) | IDE biçimlendiricisi (s.90) |

**Sınıflar ve nesneler**

| Kavram | Python | Java |
|---|---|---|
| Yapıcı | `__init__` | yapıcı |
| Alanların bilinen yeri | yalnız `__init__`'te atanır | sınıfın tepesinde bildirilir (s.81) |
| Erişim düzeyi | Gelenektir: `_ad` özeldir ve Java'daki `protected`/paket düzeyinin yerini tutar, `__ad` ad bozmalıdır. | `private`, paket, `protected`, `public` |
| Açık alan (melezde A) | `_` ile başlamayan alan | `public` örnek alanı (s.99) |
| Erişimci (melezde A) | yalnız `return self._x` yapan property ya da getter; yalnız `self._x = v` yapan setter | yalnız `return x;` yapan getter; yalnız `this.x = v;` yapan setter (s.94, 99) |
| Dilin protokol metotları (melezde B sayılmaz) | `__eq__`, `__hash__`, `__repr__` gibi dunder metotlar | `equals`, `hashCode`, `toString` (kitapta yok) |
| DTO | `@dataclass`, `NamedTuple` | açık alanlı fonksiyonsuz sınıf ya da bean (s.100); `record` (kitapta yok) |
| Sınıf dışı fonksiyon | modül fonksiyonu | uygulanmaz: dilde yok, tümü static sınıf modülün karşılığıdır (`PrimeGenerator`, s.145) |
| Statik metot | `@staticmethod` | `static` (s.296) |
| Sabit | `BÜYÜK_AD`, modül ya da sınıf düzeyinde | `public static final` (s.136) |
| Sabit kalıtımı (J2) | sabit tutan taban sınıftan türemek yerine modülden içe aktarmak | sabitli `interface`'i `implements` etmek yerine `import static` (s.307-308) |
| Test için gevşetilmiş erişim | uygulanmaz: paket düzeyi yok; test `_` önekli üyelere dokunmaz | `protected` ya da paket düzeyi, yalnız aynı paketteki test için (s.136) |
| Protected alan | alt sınıfın başka dosyada eriştiği `_` önekli alan | `protected` (s.80, 292) |
| Arayüz | `Protocol` ya da `ABC` | `interface` (s.149) |
| Yapıyla zorlama (G27) | `ABC` + `@abstractmethod` örnekleme anında zorlar; yalnız `Protocol` tür denetleyicide zorlar, çalışma anında değil | `abstract` metot derleme anında zorlar (s.301) |
| Davranış taşıyan enum | `enum.Enum` + metot; üyeler kendi gövdesini taşıyamaz, davranış değerden okunur | `enum` + sabit başına gövdeli soyut metot (s.308-309) |
| Ham eşleme (Bl.8) | `dict` | `Map` (s.114) |
| Yerel ada bağlama (Demeter ölçümü) | `x = …`, `x: T = …`, `(x := …)`, `with … as x`; `for` hedefi ve demet açma koleksiyon öğesidir | yerel değişken bildirimi, `try (… x = …)`; ölçüm aracı yok (kitapta yok) |
| Kurup veren bağlam yöneticisi (Demeter) | `@contextmanager` üreteci, her `yield`i kurulan bir nesneyse fabrikadır: `with açılmış(yol) as sayfa` | kaynak döndüren fabrika ile `try (Sayfa sayfa = Sayfa.aç(yol))` (kitapta yok) |
| Tablodan seçilen sınıfla kurma (Demeter) | `SINIFLAR[tür](veri)`, `SINIFLAR.get(tür, Varsayılan)(veri)`; tablo sözlük yazımı ya da `{s.KIND: s for s in (A, B)}` | `Map<String, Supplier<T>>` ya da `EnumMap` ile seçip kurmak (kitapta yok) |
| Yeni nesne kuran standart kütüphane çağrısı (Demeter) | `re.compile`; argparse `add_subparsers`, `add_parser`, `add_argument_group`, `add_mutually_exclusive_group`, `parse_args`; `redirect_stdout`, `redirect_stderr` | `new` her kuruluşu açıkça gösterir; statik fabrikalar (`Pattern.compile`) (kitapta yok) |
| Gereğinden somut tür (G26) | tür ipucunda `Sequence` ya da `Iterable` yeterken `list` (kitapta yok) | `List` yeterken `ArrayList` (s.301) |
| Dağıtım birimi (G7) | paket ya da dağıtım (kitapta yok) | jar dosyası (s.291) |
| Paketi içe aktarma (J1) | `import paket.modul` ve nitelikli ad (`modul.Sinif`). `from x import *` karşılık değildir: adları ad alanına kopyalar, modülü yükleyip sert bağımlılık kurar ve adın kaynağını gizler (kitapta yok). | `import package.*;` Joker yalnız paketi arama yoluna ekler, gerçek bağımlılık kurmaz (s.307). |

**Hatalar**

| Kavram | Python | Java |
|---|---|---|
| Null | `None` | `null` (s.110) |
| Yakalama bloğu | `except` | `catch` |
| Yutulan istisna | `except: pass`, gövdesi yalnız yorum olan `except` | boş ya da yalnız yorumlu `catch` (s.60) |
| İstisna zinciri | `raise AlanHatasi(...) from e` | `new StorageException("retrieval error", e)` (s.106) |
| G/Ç istisnası | `OSError` | `IOException`, `FileNotFoundException` (s.106) |
| Denetimsiz istisna | uygulanmaz: dilde denetimli istisna yok, bütün istisnalar denetimsiz | kendi istisnaları `RuntimeException`'dan türer, imzada `throws` yayılmaz (s.106-107) |

**Testler**

| Kavram | Python | Java |
|---|---|---|
| Test çatısı | `unittest` | JUnit (s.128-130) |
| Ortak kurulum | `setUp` | `@Before` (s.150) |
| Beklenen istisna testi | `assertRaises` | `@Test(expected = ...)` (s.105) |
| Gerekçeli atlama | `@unittest.skip("…")` | `@Ignore("…")` (s.58, 313) |
| Bütün testler tek komutla (E2) | `python3 -m unittest discover -s tests -t .` | `mvn test` ya da `gradle test` (kitapta yok) |
| Konsola yazma (Self-Validating) | `print` | `System.out.println` |
| Ölçüm aracı | `measure_code.py` | Yok. [ö] maddeler okunarak denetlenir. |

**Sistem ve eşzamanlılık**

| Kavram | Python | Java |
|---|---|---|
| Tek komutla kurma (E1) | `pip install -e .` (kitapta yok) | `ant all` (s.287); bugün `mvn package` ya da `gradle build` (kitapta yok) |
| Giriş noktası | `main()` ve `if __name__ == "__main__":` | `public static void main` (s.155) |
| Gömülü tembel kurulum | `if self._x is None: self._x = Somut()` | `if (service == null) service = new MyServiceImpl(...);` (s.154) |
| Service locator | global kayıt sözlüğü, adla arama | JNDI `lookup` (s.157) |
| Bağımlılığı verme (DI) | yapıcı argümanı ya da setter: `set_data_source(self, source)`; alan `__init__`'te çalışır bir varsayılanla doğar | yapıcı argümanı ya da setter: `setDataSource(...)` (s.157) |
| Bağlama yeri | `main` ya da onun çağırdığı kurulum modülünde elle bağlama (kitapta yok) | `main` ya da DI kapsayıcısı; Spring XML `p:dataSource-ref` setter ile bağlar (s.157, 163-164) |
| Kesişen kaygı | dekoratör, aynı arayüzü uygulayan sarmalayıcı sınıf | JDK Proxy, Spring AOP, AspectJ (s.161-166) |
| Görünmez büyü | monkeypatch, `sys.meta_path`, metaclass | çalışma anında bytecode yeniden yazma, özel ClassLoader, yansımayla özel üyeye erişim (kitapta yok) |
| Uyarı susturma (G4) | `# noqa`, `# type: ignore`, `# pylint: disable`, `warnings.filterwarnings("ignore")` | `@SuppressWarnings`, derleyici uyarısını kapatmak (s.289) |
| Emniyeti elle yöneten ayar (G4) | uygulanmaz: `pickle`'da sürüm alanı yok | `serialVersionUID` (s.289) |
| Çerçeve eşleme bilgisi (POJO) | ORM'in bildirimsel eşlemesi (kitapta yok) | `@Entity`, `@Table` gibi anotasyonlar ya da XML dağıtım tanımlayıcısı (s.166) |
| Kritik bölüm | paylaşılan tek kilitle `with self._lock:` (`threading.Lock`) | `synchronized` (s.181) |
| Hazır yapılar | `queue.Queue`, `concurrent.futures` | `java.util.concurrent`: `ConcurrentHashMap`, Executor, `Future` (s.182-183, 326) |
| Atomik sayaç (kilitsiz çözüm) | uygulanmaz: standart kütüphanede atomik tür yok, kilit kullanılır | `AtomicInteger`, CAS (s.327-328) |
| Oku-değiştir-yaz | `self.n += 1` | `++lastIdUsed` (s.180) |
| Bileşik işlem | kilit (kitapta yok) | `ConcurrentHashMap.putIfAbsent` (s.329) |
| Kapanma | `join(timeout)`, `future.result(timeout)`, `CancelledError` yeniden fırlatılır | `Thread.join(ms)`, `Future.get(t, unit)`, `InterruptedException` sonrası `interrupt()` (kitapta yok) |
| Para (G26) | `int` kuruş ya da `Decimal` | tamsayı tabanlı Money sınıfı (s.301) |
