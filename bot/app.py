import os
import asyncio
import json
from pathlib import Path

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command

from core.loader import load_programs
from core.faq import answer_faq
from core.recommender import recommend_courses
from core.relevancy import is_relevant

#данные и базовые штуки
programs = load_programs("data")          # читает ai.json и ai_product.json
router = Router()
FAV_PATH = Path("data/favorites.json")    # user_id -> [courses]


#утилиты
def _get_all_courses(programs_dict: dict):
    """Собирает все курсы во всех программах с метаданными."""
    items = []  # (course, program, semester, type)
    for prog_name, prog in programs_dict.items():
        for sem in prog.get("semesters", []):
            for c in sem.get("mandatory", []):
                items.append((c, prog_name, sem["num"], "обязательный"))
            for c in sem.get("electives", []):
                items.append((c, prog_name, sem["num"], "электив"))
    return items


def _load_favs() -> dict:
    if FAV_PATH.exists():
        try:
            return json.loads(FAV_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_favs(data: dict):
    FAV_PATH.parent.mkdir(exist_ok=True)
    FAV_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


#команды
@router.message(Command("start", "help"))
async def welcome(msg: types.Message):
    await msg.answer(
        "Привет! Я помогу с магистратурами ИТМО: AI и AI Product.\n\n"
        "Примеры:\n"
        "• обязательные AI семестр 1\n"
        "• элективы AI Product семестр 2\n"
        "• разница программ\n"
        "• /programs — список программ\n"
        "• /search nlp — поиск курса\n"
        "• /interests nlp, cv — рекомендации\n"
        "• /favorites — избранное"
    )


@router.message(Command("programs"))
async def cmd_programs(msg: types.Message):
    names = ", ".join(programs.keys())
    await msg.answer(f"Доступные программы: {names}\n\n"
                     "Пример: /semester 2 AI   или   /semester 1 \"AI Product\"")


@router.message(Command("semester"))
async def cmd_semester(msg: types.Message):
    # /semester <номер> <AI|AI Product>
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 3 or not parts[1].isdigit():
        await msg.answer('Использование: /semester <номер> <AI|AI Product>\n'
                         'Напр.: /semester 1 AI   или   /semester 2 "AI Product"')
        return

    sem_num = int(parts[1])
    prog_name = parts[2].strip().strip('"')

    prog = programs.get(prog_name)
    if not prog:
        await msg.answer("Не нашёл такую программу. Используй: /programs")
        return

    sem = next((s for s in prog["semesters"] if s["num"] == sem_num), None)
    if not sem:
        await msg.answer(f"Для {prog_name} нет данных по семестру {sem_num}.")
        return

    mand = sem.get("mandatory", [])
    elect = sem.get("electives", [])

    text = [f"📚 {prog_name}: семестр {sem_num}"]
    text.append("📘 Обязательные:\n- " + "\n- ".join(mand) if mand else "📘 Обязательных нет.")
    text.append("📗 Элективы:\n- " + "\n- ".join(elect) if elect else "📗 Элективов нет.")
    await msg.answer("\n\n".join(text))


@router.message(Command("search"))
async def cmd_search(msg: types.Message):
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        await msg.answer("Использование: /search <фрагмент названия курса>")
        return
    query = parts[1].lower()

    items = _get_all_courses(programs)
    hits = [(c, p, s, t) for (c, p, s, t) in items if query in c.lower()]
    if not hits:
        await msg.answer("Ничего не нашёл. Попробуй другой запрос или /programs.")
        return

    lines = [f"• {c} ({p}, семестр {s}, {t})" for (c, p, s, t) in hits[:15]]
    more = f"\n… и ещё {len(hits)-15}" if len(hits) > 15 else ""
    await msg.answer("Найдено:\n" + "\n".join(lines) + more)


@router.message(Command("interests"))
async def cmd_interests(msg: types.Message):
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        await msg.answer('Использование: /interests <ключевые слова>\n'
                         'Напр.: /interests nlp, cv')
        return
    ans = recommend_courses(parts[1], programs)
    await msg.answer(ans or "Пока не нашёл подходящих курсов.")


@router.message(Command("favorites"))
async def cmd_favorites(msg: types.Message):
    favs = _load_favs()
    my = favs.get(str(msg.from_user.id), [])
    if not my:
        await msg.answer("В избранном пусто. Добавляй так: /fav_add <полное название курса>")
        return
    await msg.answer("⭐ Твоё избранное:\n- " + "\n- ".join(my))


@router.message(Command("fav_add"))
async def cmd_fav_add(msg: types.Message):
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        await msg.answer("Укажи полное название курса после команды.\nНапр.: /fav_add Введение в NLP")
        return
    course = parts[1].strip()

    items = _get_all_courses(programs)
    all_names = {c for (c, _, _, _) in items}
    if course not in all_names:
        await msg.answer("Такого курса не найдено. Проверь написание.")
        return

    favs = _load_favs()
    uid = str(msg.from_user.id)
    favs.setdefault(uid, [])
    if course not in favs[uid]:
        favs[uid].append(course)
        _save_favs(favs)
        await msg.answer(f"Добавил в избранное: «{course}».")
    else:
        await msg.answer("Этот курс уже есть в избранном.")


@router.message(Command("fav_clear"))
async def cmd_fav_clear(msg: types.Message):
    favs = _load_favs()
    uid = str(msg.from_user.id)
    if uid in favs and favs[uid]:
        favs[uid] = []
        _save_favs(favs)
        await msg.answer("Избранное очищено.")
    else:
        await msg.answer("У тебя пока нет избранного.")


#общий обработчик свободного текста
@router.message()
async def handle_free_text(msg: types.Message):
    text = (msg.text or "").lower().strip()

    if not is_relevant(text):
        await msg.answer("Я отвечаю только про программы AI и AI Product 🙂")
        return

    faq_answer = answer_faq(text, programs)
    if faq_answer:
        await msg.answer(faq_answer)
        return

    rec_answer = recommend_courses(text, programs)
    if rec_answer:
        await msg.answer(rec_answer)
        return

    # разбор запроса вида: "обязательные/элективы AI семестр 2"
    if "ai product" in text:
        prog_name = "AI Product"
    elif "ai" in text:
        prog_name = "AI"
    else:
        await msg.answer("Уточни, речь идёт про AI или AI Product?")
        return

    sem_num = None
    for token in text.split():
        if token.isdigit():
            sem_num = int(token)
            break
    if not sem_num:
        await msg.answer("Укажи номер семестра (например: «обязательные AI семестр 2»).")
        return

    prog = programs.get(prog_name)
    if not prog:
        await msg.answer("Не удалось найти данные по программе.")
        return

    sem = next((s for s in prog["semesters"] if s["num"] == sem_num), None)
    if not sem:
        await msg.answer(f"В {prog_name} нет данных по {sem_num} семестру.")
        return

    if "обязательн" in text:
        courses = sem.get("mandatory", [])
        if not courses:
            await msg.answer(f"В {prog_name}, семестр {sem_num} обязательных дисциплин нет.")
        else:
            await msg.answer(
                f"📘 Обязательные дисциплины {prog_name}, семестр {sem_num}:\n- " +
                "\n- ".join(courses)
            )
    elif "электив" in text or "выбор" in text:
        courses = sem.get("electives", [])
        if not courses:
            await msg.answer(f"В {prog_name}, семестр {sem_num} элективных дисциплин нет.")
        else:
            await msg.answer(
                f"📗 Элективные дисциплины {prog_name}, семестр {sem_num}:\n- " +
                "\n- ".join(courses)
            )
    else:
        await msg.answer("Уточни: «обязательные» или «элективы».")


#запуск
async def main():
    token = os.getenv("TG_TOKEN")
    if not token:
        raise RuntimeError("Не задан TG_TOKEN в переменных окружения.")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
