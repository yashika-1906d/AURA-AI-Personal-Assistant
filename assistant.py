import re

from database import save_conversation

from modules.ai_engine import AIEngine
from modules.calculator import calculate
from modules.notes import add_note, get_notes, search_notes
from modules.tasks import add_task, get_tasks


class AURA:

    def __init__(self):
        self.name = "AURA"
        self.ai = AIEngine()

    def process(self, message):

        message = message.strip()

        if not message:
            return "Please enter a message.", "unknown", 0.0

        intent, confidence = self.ai.predict_intent(message)

        if confidence < 0.30:
            response = self.fallback_response()

        else:
            response = self.handle_intent(intent, message)

        save_conversation(
            message,
            response,
            intent
        )

        return response, intent, confidence

    def handle_intent(self, intent, message):

        if intent == "greeting":
            return (
                "Hello! 👋 I'm **AURA**, your AI personal assistant. "
                "How can I help you today?"
            )

        if intent == "thanks":
            return "You're welcome! 😊"

        if intent == "goodbye":
            return "Goodbye! 👋 Have a productive day!"

        if intent == "help":
            return self.help_message()

        if intent == "add_task":
            return self.handle_add_task(message)

        if intent == "show_tasks":
            return self.handle_show_tasks()

        if intent == "add_note":
            return self.handle_add_note(message)

        if intent == "show_notes":
            return self.handle_show_notes()

        if intent == "search":
            return self.handle_search(message)

        if intent == "calculator":
            return self.handle_calculator(message)

        if intent == "complete_task":
            return "Use the Tasks section to complete a task."

        if intent == "delete_task":
            return "Use the Tasks section to delete a task."

        if intent == "reminder":
            return "Use the Reminders section to create a reminder."

        return self.fallback_response()

    def handle_add_task(self, message):

        task = re.sub(
            r"^(add|create|make)\s+(a\s+)?task",
            "",
            message,
            flags=re.IGNORECASE
        ).strip()

        if not task:
            return "What task would you like me to add?"

        task_id = add_task(task)

        return (
            f"✅ Task added successfully!\n\n"
            f"**Task ID:** {task_id}\n"
            f"**Task:** {task}"
        )

    def handle_show_tasks(self):

        tasks = get_tasks()

        if not tasks:
            return "You don't have any tasks yet. 🎉"

        response = "### ✅ Your Tasks\n\n"

        for task in tasks:
            status = "✅" if task["completed"] else "⬜"

            response += (
                f"{status} **#{task['id']}** "
                f"{task['title']} — {task['priority']}\n\n"
            )

        return response

    def handle_add_note(self, message):

        content = re.sub(
            r"^(save|add|create|write)\s+(a\s+)?note",
            "",
            message,
            flags=re.IGNORECASE
        ).strip()

        if not content:
            return "What would you like me to save?"

        note_id = add_note("Quick Note", content)

        return (
            f"📝 Note saved successfully!\n\n"
            f"**Note ID:** {note_id}"
        )

    def handle_show_notes(self):

        notes = get_notes()

        if not notes:
            return "You don't have any notes yet."

        response = "### 📝 Your Notes\n\n"

        for note in notes[:10]:
            response += (
                f"**#{note['id']} — {note['title']}**\n"
                f"{note['content']}\n\n"
                "---\n\n"
            )

        return response

    def handle_search(self, message):

        keyword = re.sub(
            r"^(search|find|look for)\s*",
            "",
            message,
            flags=re.IGNORECASE
        ).strip()

        if not keyword:
            return "What would you like me to search for?"

        results = search_notes(keyword)

        if not results:
            return f"I couldn't find anything for **{keyword}**."

        response = f"### 🔎 Results for `{keyword}`\n\n"

        for note in results:
            response += (
                f"**{note['title']}**\n"
                f"{note['content']}\n\n"
            )

        return response

    def handle_calculator(self, message):

        expression = re.sub(
            r"^(calculate|solve)\s*",
            "",
            message,
            flags=re.IGNORECASE
        ).strip()

        if not expression:
            return "Please provide a mathematical expression."

        result = calculate(expression)

        if result is None:
            return "I couldn't calculate that expression."

        return f"🧮 **Answer:** {result}"

    def fallback_response(self):

        return (
            "I'm not completely sure what you mean. 🤔\n\n"
            "Try asking me to add tasks, manage notes, "
            "calculate something, search notes, or show help."
        )

    def help_message(self):

        return """
### 🤖 AURA Features

**Tasks**
- `add task complete Python project`
- `show my tasks`

**Notes**
- `add note Learn machine learning`
- `show my notes`
- `search notes machine learning`

**Calculator**
- `calculate 25 * 8`
- `calculate sqrt(144)`

**Reminders**
- Create reminders from the Reminders section.
"""