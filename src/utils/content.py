def normalize_content(content: object) -> str:
    """Convert message content to string."""
    if isinstance(content, list):
        return "".join(str(part) for part in content)
    if isinstance(content, str):
        return content
    return str(content)
