#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class MazeConfig:

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    display: bool = True


def parse_config_file(filename: str) -> MazeConfig:
    raw_config: dict[str, str] = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            clean_line = line.strip()

            if not clean_line:
                continue

            if clean_line.startswith("#"):
                continue

            if "=" not in clean_line:
                raise ValueError(
                    f"Invalid syntax on line {line_number}: "
                    "expected KEY=VALUE"
                )

            key, value = clean_line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            if not key:
                raise ValueError(f"Missing key on line {line_number}")

            if not value:
                raise ValueError(f"Missing value for key {key}")

            raw_config[key] = value

    return build_config(raw_config)


def build_config(raw_config: dict[str, str]) -> MazeConfig:

    required_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]

    for key in required_keys:
        if key not in raw_config:
            raise ValueError(f"Missing mandatory key: {key}")

    width = parse_positive_int(raw_config["WIDTH"], "WIDTH")
    height = parse_positive_int(raw_config["HEIGHT"], "HEIGHT")
    entry = parse_coordinates(raw_config["ENTRY"], "ENTRY")
    exit = parse_coordinates(raw_config["EXIT"], "EXIT")
    output_file = raw_config["OUTPUT_FILE"]
    perfect = parse_bool(raw_config["PERFECT"], "PERFECT")

    seed: int | None = None
    if "SEED" in raw_config:
        seed = parse_optional_seed(raw_config["SEED"])

    display = True
    if "DISPLAY" in raw_config:
        display = parse_bool(raw_config["DISPLAY"], "DISPLAY")

    validate_config_values(width, height, entry, exit, output_file)

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        display=display,
    )


def parse_positive_int(value: str, key: str) -> int:

    try:
        number = int(value)
    except ValueError as error:
        raise ValueError(f"{key} must be an integer") from error

    if number <= 0:
        raise ValueError(f"{key} must be positive")

    return number


def parse_optional_seed(value: str) -> int | None:

    if value.lower() in ("none", "null", ""):
        return None

    try:
        return int(value)
    except ValueError as error:
        raise ValueError("SEED must be an integer or None") from error


def parse_bool(value: str, key: str) -> bool:

    normalized = value.strip().lower()

    if normalized == "true":
        return True

    if normalized == "false":
        return False

    raise ValueError(f"{key} must be True or False")


def parse_coordinates(value: str, key: str) -> tuple[int, int]:

    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError(f"{key} must use format x,y")

    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError as error:
        raise ValueError(f"{key} coordinates must be integers") from error

    return x, y


def validate_config_values(
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        output_file: str
) -> None:

    if not output_file:
        raise ValueError("OUTPUT_FILE cannot be empty")

    entry_x, entry_y = entry
    exit_x, exit_y = exit

    if not 0 <= entry_x < width or not 0 <= entry_y < height:
        raise ValueError("ENTRY is outside maze bounds")

    if not 0 <= exit_x < width or not 0 <= exit_y < height:
        raise ValueError("EXIT is outside maze bounds")

    if entry == exit:
        raise ValueError("ENTRY and EXIT must be different")