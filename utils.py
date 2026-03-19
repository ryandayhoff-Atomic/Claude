"""Utility functions for the Claude project."""


def slugify(text):
    """Convert a string to a URL-friendly slug.

    Args:
        text: The input string to slugify.

    Returns:
        A lowercase, hyphen-separated string with non-alphanumeric
        characters removed.
    """
    import re
    import unicodedata

    # Transliterate unicode characters to their closest ASCII equivalents
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    text = text.strip("-")
    return text
