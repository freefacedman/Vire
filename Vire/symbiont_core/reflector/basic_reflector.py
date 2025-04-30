class Reflector:
    """Symbiont's reflection module: generates self-questions based on learnings."""
    def __init__(self):
        pass

    def reflect_on_summary(self, summary):
        """Given a summary list, create reflection questions."""
        questions = []
        for point in summary:
            questions.append(f'Why is "{point}" important?')
            questions.append(f'What assumptions are hidden inside "{point}"?')
        return questions
