from typing import List, Dict

from quiz.models import TestResult


def serialize_user_test_result(questions: List[Dict], user_result: TestResult):
    results = []
    i = 1
    for q in questions:
        results.append({
            "question": q["text"],
            "choices": q["options"],
            "user_answer": user_result.__dict__.get(f"q{1}"),
            "correct_answer": q["correct"]
        })
        i += 1
    return results
