from .models import Candidato
from .llm import LLM


class CVScout:
    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize the CV Scout.

        Args:
            model (str): The model to use. Defaults to "gpt-4o".
        """
        self.llm = LLM(model)

    def __call__(self, job_title: str, cv: str) -> Candidato:
        """
        Analyze a CV and return a structured representation of the work experience.

        Args:
            job_title (str): The job title to analyze.
            cv (str): The CV to analyze.

        Returns:
            Candidato: The structured representation of the work experience.
        """
        return self.llm(job_title, cv)
