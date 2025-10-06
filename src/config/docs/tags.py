from src.config.interfaces import IOpenApiTagsMetadata


class OpenApiTagsMetadata(IOpenApiTagsMetadata):
    """
    Holds route group metadata for OpenAPI docs.
    """

    @staticmethod
    def get_tags_metadata() -> list[dict[str, str]]:
        return [
            {"name": "Building", "description": "Buildings module"},
            {"name": "Organization", "description": "Organization module"},
            # ...extend here as needed
        ]
