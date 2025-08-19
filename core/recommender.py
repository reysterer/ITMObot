def recommend_courses(query: str, programs: dict) -> str | None:
    q = query.lower()

    tag_map = {
        "nlp": ["nlp", "язык", "текст", "linguistics"],
        "cv": ["cv", "computer vision", "зрение", "image", "изображен"],
        "product": ["product", "продукт", "менеджмент", "управлен"],
        "ml": ["ml", "машин", "machine learning", "обучение"],
        "dl": ["deep", "глубок"]
    }

    tags = [tag for tag, kws in tag_map.items() if any(w in q for w in kws)]
    if not tags:
        return None

    matches = []
    for prog_name, prog in programs.items():
        for sem in prog["semesters"]:
            for course in sem.get("electives", []):
                course_low = course.lower()
                if any(tag in course_low for tag in tags):
                    matches.append(f"{course} ({prog_name}, семестр {sem['num']})")

    if not matches:
        return "Не нашёл подходящих элективов по твоим интересам 😔"

    top = "\n- ".join(matches[:7])
    tags_str = ", ".join(tags)
    return f"📗 Подобрал элективы по твоим интересам ({tags_str}):\n- {top}"