from backend.app.models import Color


def build_color_signature(colors: list[Color]) -> str:
    normalized_names = sorted(color.normalized_name for color in colors)
    return "+".join(normalized_names)
