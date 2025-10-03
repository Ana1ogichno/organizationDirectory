from .postgres import PostgresSettings
from .project import ProjectSettings


class Settings:
    project: ProjectSettings = ProjectSettings()
    postgres: PostgresSettings = PostgresSettings()
