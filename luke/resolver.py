from .file_opener import FileOpener

class Resolver:
    """
    Resolve $ref, follow https://swagger.io/docs/specification/using-ref/
    """
    def __init__(self, spec: dict):
        self.spec = spec

    def resolve(self, ref: str) -> dict:
        if ref.startswith("#/"):
            return self.resolve_internal(ref)

        return self.resolve_external(ref)

    def resolve_internal(self, ref: str) -> dict:
        node = self.spec
        for node_name in ref[2:].split("/"):
            if node_name not in node:
                raise ValueError("Reference not found")

            node = node[node_name]

        return node

    def resolve_external(self, ref: str) -> dict:
        filename_or_url, component_path = ref.split("#")
        if not (filename_or_url and component_path):
            raise ValueError(f"ref {ref} is invalid")

        content = FileOpener.open(filename_or_url)
        if not content:
            raise ValueError("The specification is empty")

        spec = FileOpener.load_from_content(content)
        resolver = Resolver(spec)
        return resolver.resolve("#"+component_path)
