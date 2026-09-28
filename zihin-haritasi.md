---
title: Clean Code
markmap:
  initialExpandLevel: 2
  maxWidth: 320
---

# Clean Code

## Omurga: Kent Beck'in basit tasarımı (Bl.12)
- Önem sırasıyla dört kural
  - 1. Tüm testleri çalıştırır
  - 2. Tekrar içermez
  - 3. Programcının niyetini ifade eder
  - 4. Sınıf ve metot sayısını en aza indirir
- Kural 1'in altında tasarım yatar
  - Test edilebilirlik sınıfları küçük ve tek amaçlı olmaya iter → **SRP**
  - Sıkı bağ test yazmayı zorlaştırır → **DIP**, **bağımlılık enjeksiyonu**, soyutlama
  - Sonuç: düşük bağımlılık + yüksek uyum
- Kural 2-4 yeniden düzenleme adımıdır
  - Testler, temizlik sırasında kırma korkusunu kaldırır
  - Birkaç satır ekle → dur → tasarımı bozdum mu? → temizle → testleri çalıştır
- Kural 4 en düşük önceliklidir
  - Aşırı küçük sınıf/metot da bir hatadır
  - Dogmaya direnç: "her sınıfa arayüz", "veri ile davranış ayrı sınıflarda"

## Bağlantılar (haritanın ana okları)
- Eşikler alarmdır, ölçüt değildir
  - Fonksiyon: 20 satır tavan, hedef 2-4 satır (Bl.3 · Small!)
  - Dosya: çoğu 200 satırın altında, üst sınır 500; katı kural değil, çok arzu edilir (Bl.5 · Vertical Formatting)
  - Sınıf: satır değil **sorumluluk** sayılır (Bl.10); 200 satırı aşmak "büyük ihtimalle birden fazla iş" alarmı
  - Eşiğin altında kalmak doğruluğun kanıtı değildir: tek değişme nedeni var mı?
- Argüman: 0 ideal, 1-2 iyi, 3'ten kaçın, 3'ten fazlası olmaz → argüman nesnesi (Bl.3 · Function Arguments)
- Tasarım kalıpları ihtiyaç doğunca gelir
  - ◇ işaretli yapraklar Clean Code'da geçmez; ilgili kitap başlığının altında durur
  - Tekrar → TEMPLATE METHOD ya da STRATEGY (Bl.12 · No Duplication, G5)
  - Tür üzerine switch → ABSTRACT FACTORY + polimorfizm, tek switch (Bl.3 · Switch Statements, G23)
  - Nesne kurmayı uygulamaya bırakmak → ABSTRACT FACTORY (Bl.11 · Factories)
  - Yabancı API → ADAPTER (Bl.8 · Using Code That Does Not Yet Exist)
  - null yerine davranış taşıyan nesne → SPECIAL CASE (Bl.7 · Define the Normal Flow)
  - Kesişen kaygıyı POJO'ya dokunmadan eklemek → PROXY, iç içe DECORATOR (Bl.11 · Java Proxies, Pure Java AOP)
  - Veri yapısına yeni işlem, türe dokunmadan → VISITOR (Bl.6 · Data/Object Anti-Symmetry)
  - Tek fabrika örneği → SINGLETON + DECORATOR + ABSTRACT FACTORY (Bl.16 · DayDateFactory)
  - Kalıp adı sınıf adında → ifade gücü: COMMAND, VISITOR, DECORATOR (Bl.12 · Expressive, N3)
  - Ön tasarım yok (BDUF yok): basit ama ayrışmış başla, gerektikçe büyüt (Bl.11)
  - ◇ Çok sayıda benzer nesnede değişmez ortak kısmı paylaş → FLYWEIGHT
- Nesne mi, veri yapısı mı? (Bl.6)
  - Yeni türler eklenecekse → nesne + polimorfizm
  - Yeni işlemler eklenecekse → veri yapısı + fonksiyon
  - Melez (yarı nesne yarı veri) → hiçbiri kolay olmaz

## 1 · Temiz Kod
- There Will Be Code: kod, gereksinimin kesin ifadesidir; yok olmayacak
- Bad Code / Total Cost of Owning a Mess: karmaşa, ekibin hızını sıfıra doğru düşürür
  - Bad Code: LeBlanc yasası, sonra hiç demektir
- Grand Redesign in the Sky: baştan yazmak çözüm değildir, sürekli temizlik çözümdür
- Attitude / Primal Conundrum: hızlı gitmenin tek yolu kodu temiz tutmaktır
- What Is Clean Code?: zarif, verimli, tek işe odaklı, niyeti açık, özenle yazılmış
  - Dave Thomas: testi olmayan kod temiz değildir; bir işi yapmanın tek yolu, en küçük API
  - Ron Jeffries: tekrar yok, tek iş, ifade gücü; erken kurulan küçük ve basit soyutlamalar
- We Are Authors: kod okunmak için yazılır; okuma yazmadan çok daha sık yapılır
- **Boy Scout Rule**: dokunduğun kodu bulduğundan temiz bırak

## 2 · Anlamlı İsimler
- Use Intention-Revealing Names: ad neden var olduğunu, ne yaptığını söyler
  - Ölçü birimi adda: elapsedTimeInDays
- Avoid Disinformation: yanlış ipucu verme (Set olan şeye "List" deme)
- Make Meaningful Distinctions: a1/a2, Info/Data gibi gürültü ayrım değildir
- Pronounceable / Searchable: telaffuz edilebilir, aranabilir; magic number yok
- Avoid Encodings: tür ve önek kodlama yok (Hungarian, m_, I-arayüz)
- Avoid Mental Mapping: okuyucu adı kafasında çevirmesin
- Class Names: isim; Method Names: fiil
- Don't Be Cute / Don't Pun: espri yok, aynı sözcük iki anlamda kullanılmaz
  - Don't Pun: değer birleştiren add başka, koleksiyona öğe koyan insert/append başka
- Pick One Word per Concept: bir kavram → tek sözcük
- Solution / Problem Domain Names: önce çözüm alanının, yoksa problem alanının adı
- Add Meaningful Context / Don't Add Gratuitous Context: bağlamı sınıf ve ad alanı verir
- Bl.17'deki ad kokuları: N2 ad soyutlama düzeyini söyler (dial değil connect) · N4 belirsiz olmayan ad · N7 ad yan etkiyi söyler (createOrReturnOos) · G11 tutarlılık

## 3 · Fonksiyonlar
- **Small!**: küçük olmalı, daha da küçük; idealde 2-4 satır; 20 satıra neredeyse hiç ulaşmamalı
- Blocks and Indenting: if/else/while bloğu tek satır olur (bir çağrı); girinti 1-2 düzey
- **Do One Thing**: tek bir iş yapar, onu iyi yapar, yalnız onu yapar
  - Sections within Functions: içinde bölümler görünüyorsa birden fazla iş yapıyordur
  - Tek iş testi: içinden, uygulamasını yeniden söylemekten öte adı olan bir fonksiyon çıkarılabiliyorsa birden fazla iş yapıyordur
- One Level of Abstraction per Function
  - Stepdown Rule: kod yukarıdan aşağı bir hikâye gibi okunur, her fonksiyon bir alt düzeye iner
- Switch Statements: tek switch, fabrikanın dibine gömülür, polimorfik nesne üretir
  - ◇ Tür değil durum değişiyorsa, davranış durum nesnesinde → STATE
  - ◇ Parça ile bütün aynı arayüzle, "tek mi grup mu?" if'i kalkar → COMPOSITE
- Use Descriptive Names: uzun ve açık ad, kısa ve belirsiz addan iyidir
- **Function Arguments**
  - 0 > 1 > 2; 3'ten kaçın; 3'ten fazlası gerekçe istemez, kullanılmaz
  - Common Monadic Forms: sorgu ya da dönüşüm; olay ise adı belli olsun
  - **Flag Arguments**: bayrak argümanı fonksiyonun iki iş yaptığını ilan eder → ikiye böl
  - Dyadic / Triads: sıra karışır, okuyucu durur
    - Dyadic Functions: ikiliyi tekliye indirmenin üç yolu: argümanın metodu yap, argümanı alana çevir, argümanı yapıcıda alan bir sınıf çıkar (FieldWriter)
  - Argument Objects: birlikte gezen değişkenler kendi adını hak eden bir kavramdır
    - ◇ Değeriyle tanınan, değişmez argüman nesnesi → VALUE OBJECT
    - ◇ Çok parçalı nesneyi adım adım, yarım bırakmadan kur → BUILDER
  - Argument Lists / Verbs and Keywords: ad argümanları anlatsın
- Have No Side Effects: gizli yan etki yok; zamansal bağ varsa adda görünsün
- Output Arguments: çıktı argümanı yok; durum değişecekse sahibinin metodu olsun
- **Command Query Separation**: ya bir şey yap ya bir şey döndür
- Prefer Exceptions to Returning Error Codes
  - Extract Try/Catch Blocks; Error Handling Is One Thing
  - Error.java Dependency Magnet: hata kodu sayımı her şeyi ona bağlar
- **Don't Repeat Yourself**: tekrar, yazılımdaki kötülüğün kökü olabilir
- Structured Programming: küçük fonksiyonda erken return zararsızdır
- How Do You Write Functions Like This?: önce kaba yaz, testlerle arıt; baştan kusursuz yazılmaz

## 4 · Yorumlar
- Comments Do Not Make Up for Bad Code: yorum, ifade başarısızlığıdır
  - Bölüm girişi: yanlış yorum, hiç yorum olmamasından çok daha kötüdür
- Explain Yourself in Code: yorum yerine iyi adlı bir fonksiyon
- Good Comments
  - Legal; Informative; **Explanation of Intent (NEDEN)**; Clarification
  - **Warning of Consequences**; TODO; Amplification; public API belgeleri
- Bad Comments
  - Mumbling; Redundant; Misleading; Mandated; Journal; Noise; Scary Noise
  - Don't Use a Comment When You Can Use a Function or a Variable
  - Position Markers; Closing Brace; Attributions and Bylines
  - **Commented-Out Code**: sil, sürüm kontrolü hatırlar
  - HTML; Nonlocal Information; Too Much Information; Inobvious Connection
  - Function Headers; iç koddaki API belgeleri

## 5 · Biçimlendirme
- The Purpose of Formatting: biçim iletişimdir, "çalışsın" kadar önemlidir
- Vertical Formatting: küçük dosya (çoğu ~200 satır, üst sınır ~500) anlaşılması kolaydır
  - Newspaper Metaphor: yukarıda başlık/özet, aşağı indikçe ayrıntı
  - Vertical Openness / Density: kavramlar boş satırla ayrılır, ilişkili satırlar sık durur
  - Vertical Distance: ilişkili kavramlar yakın; çağıran çağrılanın üstünde
    - Variable Declarations: yerel değişken kullanımına yakın, döngü denetim değişkeni döngü deyiminde; alanlar tek ve bilinen bir yerde
    - protected alanlardan kaçın: sıkı ilişkili kavramları dosyalara dağıtır
  - Vertical Ordering: bağımlılık aşağı doğru akar
- Horizontal Formatting: kısa satır; boşluk ilişkiyi gösterir; hizalama yok
  - Horizontal Formatting: 100-120 karakter kabul edilir, ötesi özensizliktir
- Indentation: kapsamı görünür kılar, bozulmaz
- **Team Rules**: ekip tek bir stilde anlaşır
  - Team Rules: kurallar biçimlendirme aracına kodlanır
- Bl.17 bağlantısı · G35 Keep Configurable Data at High Levels: bilinen sabit alt düzeye gömülmez, argümanla aşağı iner

## 6 · Nesneler ve Veri Yapıları
- Data Abstraction: veriyi değil, soyut arayüzü göster
  - ◇ Koleksiyonu içini göstermeden dolaş → ITERATOR
- **Data/Object Anti-Symmetry**
  - Nesne: veriyi gizler, davranışı açar → yeni tür kolay, yeni işlem zor
  - Veri yapısı: veriyi açar, davranışı yok → yeni işlem kolay, yeni tür zor
  - "Her şey nesnedir" bir efsanedir; seçim beklenen değişikliğe göre yapılır
  - VISITOR ya da çift dağıtımın bedeli: yapıyı prosedürel programa geri çevirir (dipnot 1)
- **Law of Demeter**: yalnız yakın arkadaşlarla konuş
  - Dört arkadaş: f metodu yalnız kendi sınıfının, f'nin kurduğu nesnenin, argümanın ve alanın metotlarını çağırır
  - Train Wrecks: a.b().c().d() zinciri
    - Zinciri ara değişkenlere bölmek, zincirdekiler nesneyse ihlali gidermez; iş nesneye taşınır (createScratchFileStream)
  - Hybrids: yarı nesne yarı veri → her iki yönde de zor
    - Melez tanımı: public alan ya da alanı fiilen açan erişimciler ile anlamlı davranış aynı sınıfta
  - Hiding Structure: nesneye veri sorma, ona işi yaptır
    - ◇ Durumu içini açmadan dışarıda sakla, geri yükle → MEMENTO
  - ◇ Nesneler birbirine değil bir aracıya konuşsun → MEDIATOR
  - ◇ Birlikte tutarlı kalan küme, dışarıya tek kapı (root) → AGGREGATE
- Data Transfer Objects: davranışsız veri taşıyıcı
- Active Record: veri yapısıdır; iş kuralı ayrı nesnede durur
  - ◇ Nesne ile satır arasında çevirmen, domain tabloyu bilmez → DATA MAPPER
  - ◇ Domain'e koleksiyon gibi görünen kalıcılık kapısı → REPOSITORY
  - ◇ Tablo diliyle konuşan erişim sınıfı (bkz. Bl.11 · Pure Java AOP) → DAO

## 7 · Hata Yönetimi
- Use Exceptions Rather Than Return Codes
- Write Your Try-Catch-Finally Statement First: işlemin sınırını önce çiz
  - try bloğu bir işlem gibidir: catch programı tutarlı bir durumda bırakır
  - Test geçince yakalanan tür, fırlatılan gerçek türe daraltılır (FileNotFoundException)
- Use Unchecked Exceptions: imzalardan sızan bağımlılığı önler
  - Denetimli istisna OCP'yi bozar; yalnız kritik bir kütüphanede değer taşır
- Provide Context with Exceptions: işlem ve neden mesajda olsun
- Define Exception Classes in Terms of a Caller's Needs: sarmala, çağıranın diline çevir
  - Çoğu zaman tek istisna sınıfı yeter; ayrı sınıf yalnız biri yakalanırken öbürü geçsin diye açılır
- Define the Normal Flow: Special Case nesnesiyle istisnasız akış
  - ◇ Hiçbir şey yapmayan varsayılan, Special Case'in özel hâli → NULL OBJECT
- **Don't Return Null** / **Don't Pass Null**

## 8 · Sınırlar
- Using Third-Party Code: sınır arayüzünü (Map vb.) sistemde dolaştırma, sarmala
  - Sınır türü public API'den döndürülmez, argüman olarak alınmaz
  - ◇ Karmaşık alt sisteme tek, sade kapı → FACADE
- Exploring and Learning Boundaries: Learning Tests; bedava ve öğretici
  - Learning Tests Are Better Than Free: yeni sürümde yeniden koşulur, davranış farkını hemen gösterir
  - Giden sınır testleri: öğrenme gerekmese de arayüzü üretim kodu gibi kullanan testler geçişi kolaylaştırır
- Using Code That Does Not Yet Exist: istediğin arayüzü tanımla → ADAPTER
- Clean Boundaries: yabancı koda az yerde dokun; sınırı testlerle tanımla

## 9 · Birim Testleri
- The Three Laws of TDD
- Keeping Tests Clean: kirli test, hiç test olmamasından beterdir
- Tests Enable the -ilities: esneklik, bakım ve yeniden kullanım testlerle gelir
- Clean Tests: okunabilirlik; build-operate-check
  - Domain-Specific Testing Language
    - Baştan tasarlanmaz, yeniden düzenlemeden doğar
  - A Dual Standard: test kodu da temizdir ama üretim verimliliği gerekmez
    - Sınırı: yalnız bellek ve işlemci verimliliği gevşer, temizlik gevşemez
- One Assert per Test → **Single Concept per Test**
- **F.I.R.S.T.**: Fast, Independent, Repeatable, Self-Validating, Timely

## 10 · Sınıflar
- Class Organization: sabitler → alanlar → public metotlar → onları izleyen private'lar
  - Encapsulation: gizlilik tercih edilir, test için gevşetmek son çaredir
- **Classes Should Be Small!**: boyut sorumluluk sayısıyla ölçülür
  - Kısa ad verilemiyorsa büyüktür; Processor/Manager/Super uyarı işaretidir
  - ~25 sözcükle "eğer, ve, veya, ama" olmadan anlatılabilmeli
- **The Single Responsibility Principle**: tek değişme nedeni
  - Çok sayıda küçük sınıf, birkaç büyük sınıftan iyidir
  - "Çalışıyor" ile "temiz" ayrı işlerdir; çalışınca durma
- **Cohesion**: az alan; her metot alanların çoğunu kullanır
  - Maintaining Cohesion Results in Many Small Classes: yalnız birkaç metodun paylaştığı alanlar yeni bir sınıf ister
    - Argüman taşımamak için alana yükseltilen değişkenler uyumu düşürür → onları paylaşan metotlar yeni sınıfa çıkar
- Organizing for Change: açık/kapalı ilke (OCP); yeni iş alt sınıfla eklenir
  - Yalnız bir public metoda hizmet eden özel yardımcı kümesi bölme adayıdır
  - Sınıf mantıksal olarak tamamsa dokunulmaz; tasarımı değiştirmenin tetiği gerçek değişikliktir
- **Isolating from Change**: somut ayrıntıya değil soyutlamaya bağlan → **DIP**
  - Bağımlılık yapıcıya verilir → test kendi sahte nesnesini verir
  - ◇ Değişikliği abonelere bildir, yayıncı onları tanımaz → OBSERVER
  - ◇ Soyutlama ile uygulama ayrı ayrı çoğalsın → BRIDGE

## 11 · Sistemler
- How Would You Build a City?: soyutlama düzeyleri ve modülerlik ile
- **Separate Constructing a System from Using It**
  - LAZY INITIALIZATION eleştirisi: gömülü tembel kurulum somut sınıfa bağlar, testi zorlar, SRP'yi bozar; ölçülmüş ihtiyaç yoksa erken optimizasyondur
  - Separation of Main: kurulum main'de, uygulama hazır nesneleri kullanır; oklar main'den dışa
  - Factories: ne zaman kurulacağına uygulama karar verir, nasıl kurulacağına fabrika
    - ◇ Hangi nesnenin yaratılacağı alt sınıfa kalsın → FACTORY METHOD
    - ◇ Hazır bir nesneyi kopyalayıp yenisini üret → PROTOTYPE
  - **Dependency Injection**: nesne bağımlılığını kendisi kurmaz, edilgen kalır → SRP desteklenir
    - Bağımlılık yapıcı argümanıyla, setter ile ya da ikisiyle verilir
    - JNDI araması DI'ın yarım hâlidir: nesne bağımlılığını hâlâ kendisi çözer
    - ◇ Bağımlılığı kendin ara (JNDI gibi), DI'ın yarım hâli → SERVICE LOCATOR
- Scaling Up: sistem, kaygılar ayrıldıkça büyüyebilir
  - POJO: çerçeve türünden türemez, çerçevenin yaşam döngüsü metotlarını uygulamaz, iş metodunda bağımlılık aramaz (EJB2 karşı örneği)
  - Cross-Cutting Concerns: proxy / AOP ile kesişen kaygılar
    - ◇ İstek bir zincirde sırayla dolaşsın (filtre zinciri) → CHAIN OF RESPONSIBILITY
  - Pure Java AOP Frameworks: eşleme anotasyonları, eşleme sık değişmiyorsa sınıfta kalabilir; tam POJO için dış yapılandırmaya taşınır
- Test Drive the System Architecture: ön tasarım (BDUF) yok; basit ama ayrışmış başla
- Optimize Decision Making: kararı en son sorumlu ana kadar ertele
- Use Standards Wisely: standart, ancak kanıtlanabilir değer katıyorsa
- Systems Need Domain-Specific Languages
  - ◇ Küçük bir dilin gramerini yorumla → INTERPRETER
- Conclusion: çalışabilecek en basit şeyi kullan; niyet her soyutlama düzeyinde açık kalsın

## 12 · Ortaya Çıkış (Emergence)
- Getting Clean via Emergent Design: dört kural iyi tasarımın ortaya çıkmasını sağlar
- Rule 1 · Runs All the Tests → SRP, DIP, DI (bkz. Omurga)
- Rules 2-4 · Refactoring
  - No Duplication: satır tekrarı + uygulama tekrarı; küçükteki yeniden kullanım büyüğü getirir
    - Ortak kısım çıkarılınca SRP ihlalleri görünür
    - TEMPLATE METHOD üst düzey tekrarı kaldırır
  - Expressive: iyi ad, küçük fonksiyon/sınıf, standart kalıp adları, iyi test
  - Minimal Classes and Methods: sayıyı düşük tut ama en düşük öncelik bu
    - Dogma: her sınıfa arayüz açmak, alan ile davranışı ayrı sınıflara bölmek (bkz. Omurga)
- Conclusion: deneyimin yerini tutmaz, ama onu hızla kazandırır

## 13 · Eşzamanlılık
- Why Concurrency? / Myths and Misconceptions: ne'yi ne zaman'dan ayırır; bedava değildir
- Concurrency Defense Principles
  - SRP: eşzamanlılık kodunu diğer koddan ayır
  - Limit the Scope of Data; Use Copies of Data; bağımsız thread'ler
- Know Your Library / Execution Models: Producer-Consumer, Readers-Writers, Dining Philosophers
- Synchronized bölümleri küçük tut; aralarında bağımlılık kurma
- Doğru kapanma kodu zordur
- Testing Threaded Code: seyrek hatalar da hatadır; önce thread'siz kodu çalıştır; takılabilir, ayarlanabilir kod
  - Run with More Threads Than Processors: görev değişimi sıklaşsın, hata ortaya çıksın
  - Run on Different Platforms: bütün hedef platformlarda erken ve sık koş
  - Instrument Your Code to Try and Force Failures: jiggling (wait, sleep, yield, öncelik), elle ya da otomatik
- Ek A · Dependencies Between Methods Can Break Concurrent Code: tek tek güvenli çağrılardan kurulan bileşik işlem güvenli değildir → putIfAbsent ya da kilit

## 14 · Ardışık İyileştirme
- Args Implementation: temiz son hâl
- Args: The Rough Draft: önce çalışan kirli taslak
- So I Stopped: büyüme karmaşayı artırınca dur
- **On Incrementalism**: büyük adım yok; her küçük değişiklikten sonra testler yeşil
- Ders: çalışan kod yetmez; önce yaz, sonra temizle

## 15-16 · Vaka İncelemeleri
- JUnit Internals: iyi koda bile Boy Scout uygulanır
- Refactoring SerialDate: önce testleri güçlendir, sonra adım adım temizle
  - First, Make It Work: kapsam aracı çalışmayan kodu gösterir (Clover, T2)
  - Kod küçülünce düşen kapsam yüzdesi gerileme değildir
  - DayDateFactory: taban sınıf türevini yaratmaz, fabrika yaratır (G7)

## 17 · Kokular ve Sezgisel Kurallar
- Comments: C1 uygunsuz bilgi · C2 eski · C3 gereksiz · C4 kötü yazılmış · C5 yorumdaki kod
- Environment: E1 derleme tek adım · E2 testler tek adım
- Functions: F1 çok argüman · F2 çıktı argümanı · F3 bayrak argümanı · F4 ölü fonksiyon
- General
  - G1 bir kaynak dosyada birden çok dil · G2 bariz davranış eksik · **G3 sınırlarda yanlış davranış** · G4 aşılmış güvenlik önlemleri
  - **G5 tekrar** · G6 yanlış soyutlama düzeyi · G7 taban sınıfın türeve bağımlı olması
    - G5'in üç biçimi: birebir aynı kod → metot; aynı switch/if zinciri → polimorfizm; benzer algoritma → TEMPLATE METHOD ya da STRATEGY
    - G6 ayrımı tamdır: yanlış düzeydeki soyutlama sahte değerle kapatılmaz (sınırsız yığında percentFull → 0 yalandır)
    - G7 istisnası: türev sayısı kesin sabitse (sonlu durum makinesi) taban türevleri bilebilir, o zaman ikisi aynı dağıtım biriminde durur
  - G8 fazla bilgi · G9 ölü kod · G10 dikey ayrılık · G11 tutarsızlık · G12 karmaşa
  - G13 yapay bağ · **G14 feature envy** · **G15 seçici argüman** · G16 gizli niyet
    - G14 istisnası: taşımak tasarımı bozuyorsa kıskançlık gerekli kötülüktür (rapor biçimi çalışan sınıfına girmez: SRP, OCP, CCP)
  - **G17 yanlış yerdeki sorumluluk** · G18 uygunsuz static · G19 açıklayıcı değişken
  - G20 ad ne yaptığını söylesin · G21 algoritmayı anla · G22 mantıksal bağımlılığı fiziksel yap
    - G21: testlerin geçmesi yetmez, kodun nasıl çalıştığı bilinir; yolu, apaçık olana dek yeniden düzenlemektir
  - **G23 switch/if yerine polimorfizm (tek switch kuralı)** · G24 standart gelenekler
    - G23: her switch şüphelidir; Bl.6'daki istisna (işlemler türlerden sık değişir) nadirdir
  - G25 magic number yerine adlı sabit · G26 kesin ol · G27 gelenek yerine yapı
    - G25: sihirli değer kendini anlatmayan her simgedir ("John Doe"); iyi bilinen sabit açık formülde ham kalabilir (5280), hataya açık uzun sabit (π) adlıdır
  - G28 koşulları kapsülle · G29 olumsuz koşuldan kaçın · **G30 fonksiyon tek iş yapar**
  - G31 gizli zamansal bağ · G32 keyfi olma · **G33 sınır koşullarını kapsülle**
    - G31: sıra gizlenmez; kova zinciri (her adım sonrakinin girdisini üretir) ya da öncekini kendisi çağıran adım. Sırayı zorlayıp nedenini anlatmayan argüman keyfidir (G32)
  - **G34 tek soyutlama düzeyi** · G35 ayarlar üst düzeyde durur · G36 geçişli gezinmeden kaçın
    - G34: deyimler adın bir düzey altında; düzeyleri ayırmak yeni düzey çizgileri ortaya çıkarır, ayırma sürer
- Java: J1 joker import · J2 sabit kalıtılmaz · J3 sabit yerine enum
- Names: N1 açıklayıcı · N2 doğru soyutlama düzeyi · N3 standart terim · N4 belirsiz olmayan
  - N5 uzun kapsam → uzun ad · N6 kodlama yok · N7 yan etkiyi adda söyle
    - N1: anlam kayar; adlar her geçişte yeniden değerlendirilir, iyi ad yapıya anlam yükler (score → isStrike tahmin edilir)
    - N5'in tersi: dar kapsamda uzun ad gürültüdür (beş satırlık döngüde i, rollCount değil)
- Tests: T1 yetersiz test · T2 kapsam aracı · T3 önemsiz testi atlama · T4 yok sayılan test bir sorudur
  - **T5 sınır koşullarını test et** · **T6 hatanın çevresini sıkı test et** · T7-T8 başarısızlık örüntüleri · T9 hızlı
    - T4: derlenemeyen soru yoruma alınmış test olarak kalır; bu yoruma alınmış kod (C5) değil, gereksinime sorulan sorudur
- Conclusion: bu liste tam değildir; bir değer sistemi sunar, kural kataloğu değildir

