def is_relevant(query: str) -> bool:
    q = query.lower()
    keywords = [
        "ai", "ai product", "artificial intelligence", "искусственный интеллект",
        "элект", "обязательн", "курс", "семестр", "програм", "разница", "срок", "форма"
    ]
    return any(word in q for word in keywords)