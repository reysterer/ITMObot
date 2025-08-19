def answer_faq(query: str, programs: dict) -> str | None:
    q = query.lower()

    if "разница" in q or "сравн" in q:
        return (
            "AI → акцент на исследования и алгоритмы (машинное/глубокое обучение).\n"
            "AI Product → акцент на управление ИИ-продуктами, менеджмент и бизнес-навыки."
        )

    if "срок" in q or "длительность" in q:
        return "Обе программы длятся 2 года, форма обучения — очная."

    if "форма" in q or "очно" in q or "заочно" in q:
        return "Форма обучения: очная."

    if "описание ai product" in q or "что такое ai product" in q:
        return "AI Product — про продакт-менеджмент и управление ИИ-продуктами."

    if "описание" in q or "что такое ai" in q:
        return "AI — про ML/DL, NLP, CV и анализ данных."

    return None