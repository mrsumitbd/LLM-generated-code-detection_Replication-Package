import anthropic


class BaseTask:
    """Base class for evaluation tasks."""

    @property
    def name(self) -> str:
        """Return the name of the task."""
        return self.__class__.__name__

    def get_task_instruction(self) -> str:
        """Return the instruction for the task."""
        return ""


class SummarizationTask(BaseTask):
    """Task for summarizing text."""

    @property
    def name(self) -> str:
        return "Summarization"

    def get_task_instruction(self) -> str:
        return "Summarize the following text in 2-3 sentences."


class TranslationTask(BaseTask):
    """Task for translating text."""

    @property
    def name(self) -> str:
        return "Translation"

    def get_task_instruction(self) -> str:
        return "Translate the following text to French."


class QuestionAnsweringTask(BaseTask):
    """Task for answering questions."""

    @property
    def name(self) -> str:
        return "Question Answering"

    def get_task_instruction(self) -> str:
        return "Answer the following question based on the provided context."


def evaluate_task(task: BaseTask, content: str) -> str:
    """Evaluate a task using Claude API."""
    client = anthropic.Anthropic()

    instruction = task.get_task_instruction()
    prompt = f"{instruction}\n\nContent: {content}"

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


if __name__ == "__main__":
    # Example usage
    summarization_task = SummarizationTask()
    print(f"Task: {summarization_task.name}")
    print(f"Instruction: {summarization_task.get_task_instruction()}")

    # Example text to summarize
    sample_text = """
    Artificial intelligence has revolutionized many industries over the past decade.
    Machine learning algorithms can now recognize patterns in data that would be impossible
    for humans to detect manually. From healthcare to finance, AI applications are improving
    efficiency and accuracy. However, there are also concerns about job displacement and
    the need for ethical guidelines in AI development.
    """

    result = evaluate_task(summarization_task, sample_text)
    print(f"\nSummarization Result:\n{result}")

    # Example with translation task
    translation_task = TranslationTask()
    print(f"\n\nTask: {translation_task.name}")
    print(f"Instruction: {translation_task.get_task_instruction()}")

    english_text = "Hello, how are you today?"
    result = evaluate_task(translation_task, english_text)
    print(f"\nTranslation Result:\n{result}")