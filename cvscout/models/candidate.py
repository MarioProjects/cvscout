import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, computed_field, field_validator

from cvscout.utils import clean_string


class ExperienciaLaboral(BaseModel):
    """Work experience data model."""

    empresa: str = Field(
        ...,
        description="Company name where the candidate worked.",
    )
    puesto: str = Field(
        ...,
        description="Job title of the candidate.",
    )
    fecha_inicio: datetime = Field(
        ...,
        description="Start date of the job experience.",
    )
    fecha_fin: datetime = Field(
        ...,
        description="End date of the job experience.",
    )
    relacionado: bool = Field(
        ...,
        description="""
        Whether the job experience is related to the job title.
        A job experience is considered related if the tasks to be performed
        are similar or related to the job title.
        """,
    )

    @computed_field
    @property
    def duracion(self) -> str:
        """Calculate the duration of the job experience."""
        delta = relativedelta(self.fecha_fin, self.fecha_inicio)
        # Format the difference
        parts = []
        if delta.years:
            parts.append(f"{delta.years} año{'s' if delta.years > 1 else ''}")
        if delta.months:
            parts.append(f"{delta.months} mes{'es' if delta.months > 1 else ''}")
        if delta.days:
            parts.append(f"{delta.days} día{'s' if delta.days > 1 else ''}")

        # Join the parts into a single string
        difference_str = " y ".join(parts)
        return difference_str

    @property
    def duracion_meses(self) -> int:
        """Calculate the duration of the job experience in months."""
        delta = relativedelta(self.fecha_fin, self.fecha_inicio)
        return delta.years * 12 + delta.months


class Candidato(BaseModel):
    """Candidate detail data model."""

    nombre: str = Field(
        ...,
        description="Candidate's name.",
    )
    edad: int = Field(
        ...,
        description="Candidate's age.",
    )
    experiencia: list[ExperienciaLaboral] = Field(
        ...,
        description="List of job experiences of the candidate.",
    )
    resumen: str = Field(
        ...,
        description="""
            Description of experience, an explanatory text about the candidate's experience.
            Please just take into account the job experiences related to the job title.
        """,
    )

    @field_validator("experiencia", mode="after")
    @classmethod
    def just_experiencia_related(
        cls, experiences: list[ExperienciaLaboral]
    ) -> list[ExperienciaLaboral]:
        """Remove job experiences that are not related to the job title."""
        return [exp for exp in experiences if exp.relacionado]

    @field_validator("resumen", mode="after")
    @classmethod
    def explainability_score(cls, resumen: str) -> str:
        """Generate an explanatory text about the candidate's experience."""
        explicacion_score = """
        El score asignado al candidato se calcula teniendo en cuenta la experiencia laboral relacionada
        con el puesto ofertado, premiando la fidelidad del candidato en las empresas en las que ha trabajado.
        """
        return clean_string(resumen + explicacion_score)

    @computed_field
    @property
    def score(self) -> int:
        """Calculate the score of the candidate."""
        # Take into account only the job experiences related to the job title
        related_experiences = [exp for exp in self.experiencia if exp.relacionado]

        total_relevant_months = 0

        # We will reward the loyalty of the candidate to the company
        # by applying a multiplier to the duration of the job experience
        for exp in related_experiences:
            months = exp.duracion_meses
            if months < 3:
                multiplier = 0.5
            elif months < 6:
                multiplier = 0.75
            elif months < 24:
                multiplier = 1.0
            else:
                multiplier = 1.25

            total_relevant_months += months * multiplier

        years_experinece = total_relevant_months / 12.0

        if years_experinece <= 0:
            score = 0
        elif years_experinece > 5:
            score = 100
        else:
            # score = 100 * math.sin(math.pi * (years_experinece - 0) / (10 - 0))
            score = 100 * (1 - math.exp(-1.25 * years_experinece))
        return int(score)


CANDIDATE_PARSER = PydanticOutputParser(pydantic_object=Candidato)
CANDIDATE_FORMAT_INSTRUCTIONS = CANDIDATE_PARSER.get_format_instructions()
