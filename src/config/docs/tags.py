from src.config.interfaces import IOpenApiTagsMetadata


class OpenApiTagsMetadata(IOpenApiTagsMetadata):
    """
    Holds route group metadata for OpenAPI docs.
    """

    @staticmethod
    def get_tags_metadata() -> list[dict[str, str]]:
        return [
            {"name": "User", "description": "Profile info"},
            # ...extend here as needed
        ]
