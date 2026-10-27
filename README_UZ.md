# ScriptTime-UZ — o‘zbekcha ma’lumot

**Maqsad:** o‘zbek tilida turli yozuv shakllari (eski lotin, yangi lotin, kirill) va normativ hujjatlar amal qilish sanalarining axborot qidiruvi sifatiga ta’sirini o‘rganish.

Bu hozircha **ilmiy prototip**, huquqiy maslahat beruvchi xizmat yoki o‘qitilgan LLM emas. Boshlang‘ich ma’lumotlar to‘plami 3 ta tadqiqotchi parafrazi va 3 ta mustaqil savoldan iborat. Ularning 9 ta yozuv varianti ilmiy xulosa chiqarish uchun yetarli emas.

## Ishga tushirish
```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m scripttime evaluate
```

## Keyingi vazifalar
Rasmiy hujjatlarning bandma-band versiyalarini mustaqil tekshirish, 60+ asosiy savol tuzish, xatolarning sababini tahlil qilish, keyin kichik embedding modelini o‘qitib ko‘rish. GitHub kodi Toolbase.uz ishlab chiqarish tizimidan alohida.

## Muallif
Yakhyokhon Kodirov — https://orcid.org/0009-0003-5930-8827

Professorlarning maqolalari [docs/RELATED_WORK_PROFESSORS.md](docs/RELATED_WORK_PROFESSORS.md) faylida tahlil qilingan. Bu hamkorlik yoki ularning ilmiy rahbarligi mavjud degani emas.
