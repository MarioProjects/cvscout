import os
from openai import OpenAI
from datetime import datetime

from cvscout.models import Candidato, CANDIDATE_PARSER, CANDIDATE_FORMAT_INSTRUCTIONS


class LLM:
    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize the LLM.

        Args:
            model (str): The model to use. Defaults to "gpt-4o".
        """
        assert (
            "OPENAI_API_KEY" in os.environ
        ), "Please set the OPENAI_API_KEY environment variable"

        self.llm = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.model = model
        self.system_template = """
        You are a human resources specialist.
        You must use spanish language.
        You have to perform the task of extracting information from CVs.
        You will be presented with a job title and the candidate's CV.

        Take into account that current date is {current_date}.

        Extract the data following the format:
        {format_instructions}
        """
        self.prompt_template = """
        Job title: {job_title}

        CV:
        {cv}
        """

    def __call__(self, job_title: str, cv: str) -> Candidato:
        """
        Analyze a CV and return a structured representation of the work experience.

        Args:
            job_title (str): The job title to analyze.
            cv (str): The CV to analyze.

        Returns:
            Candidato: The structured representation of the work experience.
        """
        # Get the current date
        current_date = datetime.now()
        # Format the date
        formatted_date = current_date.strftime("%d %B %Y")

        system_instructions = self.system_template.format(
            current_date=formatted_date,
            format_instructions=CANDIDATE_FORMAT_INSTRUCTIONS,
        )

        prompt = self.prompt_template.format(job_title=job_title, cv=cv)

        chat_completion = self.llm.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_instructions,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=self.model,
        )

        try:  # extract the response
            response = chat_completion.choices[0].message.content
            info_candidato: Candidato = CANDIDATE_PARSER.parse(response)
            return info_candidato
        except Exception as e:
            raise Exception(f"Error parsing response: {e}")
