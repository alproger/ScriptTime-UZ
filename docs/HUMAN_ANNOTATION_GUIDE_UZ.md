# ScriptTime-UZ: inson tomonidan manbalarni tekshirish qo‘llanmasi

**Holat:** 27-oktabr 2026. Ilmiy tajribaga tayyorgarlik. Jadvallarning sarlavhalari tayyor, natijalar hali to‘planmagan.

## Nega bu kerak?
GitHub'dagi 3 ta demo yozuvi va 3 ta asosiy savol haqiqiy benchmark emas. Kamida bir nechta hujjat oilasi bo‘yicha hujjatning **asl tahriri**, **nashr sanasi**, **bandining amal qilish sanasi** va **savolga to‘g‘ri dalil**ni tekshirishimiz kerak.

## Bugungi tekshiruv
1. `data/annotation/source_registry.csv` dagi LexUZ havolasini oching.
2. Hujjatning qabul sanasi va amaldagi matnini *tarixiy holat* bilan adashtirmang. LexUZ'dagi `ONDATE` versiya ko‘rinishini har safar tekshiring.
3. Kamida 5 ta aniq band/qoida toping. `evidence_template.csv`dagi sarlavhalarni nusxalab, faqat **manbada haqiqatan bor** ma’lumot bilan to‘ldiring. Bitta hujjatda turli moddalarning kuchga kirish sanasi farq qilishi mumkin.
4. Band o‘zgargan sanalarni tekshirmasangiz, `review_status=pending` yozing; taxmin qilmang.
5. 10 ta **mustaqil** savol yozing. Eski lotin/yangi lotin/kirill variantlari bitta `question_group_id` bo‘lib qoladi. `gold_evidence_id` avval tekshirilgan bandga mos kelishi shart.
6. Savolning `as_of` (qaysi tarixni so‘rayapti?) va `known_at` (shu vaqtgacha qaysi ma’lumot e’lon qilingan?) sanalarini ajrating.

## Annotatsiya mezoni
- Evidence matni original ma’lumotni buzib ko‘rsatmasin.
- Qonunning *qabul qilingan kuni* bilan *kuchga kirgan kuni*ni bitta sana deb hisoblamang.
- Aniq dalil topilmasa, `needs_abstention=true`, javobni uydirmang.
- Bir savolning yozuv variantlarini train va testga alohida tarqatmang.
- Faqat hujjatning nomi bo‘yicha javobi topiladigan yengil savollarga bog‘lanib qolmang: bir mavzudagi eski/yangi qarama-qarshi bandlarni tanlang.
- Ikkinchi tekshiruvchi iloji boricha boshqa inson bo‘lsin; bahsli bandlar `pending` qoladi.

## Datasetni oshkora e’lon qilish
Dastlabki fayllarda shaxsiy ma’lumot, maktab o‘quvchilari haqidagi ma’lumot yoki yopiq Toolbase fayllari bo‘lmasin. LexUZ'dagi to‘liq katta matnlarni ularning qayta foydalanish shartlarini tekshirmasdan GitHubga ko‘chirmang; havola, band raqami va qisqa zarur parchalar bilan boshlang.

## Ilmiy maqsad
O‘lchovlar: `Hit@1`, `Recall@3`, `MRR@3`, noto‘g‘ri amal davridagi hujjatni tanlash tezligi. **Natijani faqat mustaqil tekshirilgan korpus va savollar orqali chiqaring.**
