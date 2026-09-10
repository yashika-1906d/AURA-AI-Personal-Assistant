from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


TRAINING_DATA = [
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("good evening", "greeting"),
    ("how are you", "greeting"),

    ("add a task", "add_task"),
    ("create a task", "add_task"),
    ("add something to my todo", "add_task"),
    ("I need to do something", "add_task"),

    ("show my tasks", "show_tasks"),
    ("what are my tasks", "show_tasks"),
    ("list my todo", "show_tasks"),
    ("show pending work", "show_tasks"),

    ("complete my task", "complete_task"),
    ("mark task complete", "complete_task"),
    ("finish my task", "complete_task"),

    ("delete my task", "delete_task"),
    ("remove a task", "delete_task"),

    ("save a note", "add_note"),
    ("create a note", "add_note"),
    ("write a note", "add_note"),
    ("remember this", "add_note"),

    ("show my notes", "show_notes"),
    ("list my notes", "show_notes"),
    ("display notes", "show_notes"),

    ("search my notes", "search"),
    ("find something in my notes", "search"),
    ("search my information", "search"),

    ("set a reminder", "reminder"),
    ("create reminder", "reminder"),
    ("remind me later", "reminder"),

    ("calculate something", "calculator"),
    ("solve this calculation", "calculator"),
    ("what is 25 times 5", "calculator"),
    ("calculate 100 divided by 4", "calculator"),

    ("what can you do", "help"),
    ("help me", "help"),
    ("show commands", "help"),

    ("thank you", "thanks"),
    ("thanks", "thanks"),

    ("bye", "goodbye"),
    ("goodbye", "goodbye")
]


class AIEngine:

    def __init__(self):

        texts = [item[0] for item in TRAINING_DATA]
        labels = [item[1] for item in TRAINING_DATA]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        features = self.vectorizer.fit_transform(texts)

        self.model = LogisticRegression(
            max_iter=1000
        )

        self.model.fit(features, labels)

    def predict_intent(self, message):

        features = self.vectorizer.transform([message])

        probabilities = self.model.predict_proba(features)[0]

        best_index = probabilities.argmax()

        intent = self.model.classes_[best_index]

        confidence = probabilities[best_index]

        return intent, float(confidence)

    def get_intents(self):
        return list(self.model.classes_)