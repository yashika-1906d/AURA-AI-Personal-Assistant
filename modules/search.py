from modules.notes import search_notes
from modules.tasks import get_tasks


def search_everything(keyword):
    keyword = keyword.lower()

    notes = search_notes(keyword)

    tasks = [
        task
        for task in get_tasks()
        if keyword in task["title"].lower()
    ]

    return {
        "notes": notes,
        "tasks": tasks
    }


def format_search_results(results):

    output = []

    if results["notes"]:
        output.append("### 📝 Notes")

        for note in results["notes"]:
            output.append(
                f"- **{note['title']}**: {note['content']}"
            )

    if results["tasks"]:
        output.append("### ✅ Tasks")

        for task in results["tasks"]:
            status = "Completed" if task["completed"] else "Pending"

            output.append(
                f"- **{task['title']}** — {status}"
            )

    if not output:
        return "No matching information was found."

    return "\n\n".join(output)