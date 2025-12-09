def send_problem_message(problem, formater):
    title = formater(problem["title"])
    difficulty = formater(problem["difficulty"].capitalize())
    url = problem["url"]
    tags = ", ".join(problem["tag"] or [])

    message_text = (
        f"<b>{title}</b>\n"
        f"<i>Сложность:</i> <b>{difficulty}</b>\n"
        f"<i>Теги:</i> {formater(tags)}\n\n"
        f'<a href="{url}">Открыть задачу на LeetCode</a>'
    )
    return message_text
