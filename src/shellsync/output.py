import sys


# USE_COLOR = sys.stdout.isatty()
USE_COLOR = True

def _color(code: str, text: str) -> str:
    if not USE_COLOR:
        return text

    return f"\033[{code}m{text}\033[0m"


def green(text: str) -> str:
    return _color("32", text)


def yellow(text: str) -> str:
    return _color("33", text)


def red(text: str) -> str:
    return _color("31", text)


def cyan(text: str) -> str:
    return _color("36", text)


def bold(text: str) -> str:
    return _color("1", text)


def print_status(label: str, target: str) -> None:
    colors = {
        "CURRENT": green,
        "PUSHED": green,
        "OK": green,
        "UPDATE": yellow,
        "BACKUP": cyan,
        "WOULD PUSH": yellow,
        "MISSING": red,
        "FAIL": red,
        "ERROR": red,
    }

    color = colors.get(label, lambda value: value)

    padded_label = f"{label:<18}"
    print(f"  {color(padded_label)} {target}")

def heading(text: str) -> None:
    print(f"\n{bold(text)}")


def success(text: str) -> None:
    print(green(f"✓ {text}"))


def error(text: str) -> None:
    print(red(f"✗ {text}"), file=sys.stderr)


