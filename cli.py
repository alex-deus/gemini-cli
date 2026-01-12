#!/usr/bin/env python3
import json
import mimetypes
from datetime import datetime
from os import getenv
from pathlib import Path

import click
from google import genai


@click.group
def cli() -> None:
    ...


@cli.command("run")
@click.option(
    "--input",
    "image_input",
    default="examples/input.png",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--prompt", required=True, type=str)
@click.option(
    "--extra-image", "extra_images", multiple=True, type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option("--output", "image_output", default=None, show_default=True)
def run(image_input: Path, prompt: str, extra_images: tuple[Path, ...], image_output: str | None) -> None:
    # Make default image_output
    if not image_output:
        image_output = f"results/{datetime.utcnow().isoformat()}.png"

    # Load Google's Creds
    json_file_path = getenv("GOOGLE_APPLICATION_CREDENTIALS")
    with open(json_file_path) as f:
        google_creds_data = json.load(f)

    client = genai.Client(vertexai=True, project=google_creds_data["project_id"])

    parts = []

    # Load input image
    image = _load_image(image_input)
    parts.append(image)

    # Load extra images
    for img in extra_images:
        parts.append(_load_image(img))

    # Load prompt
    part = genai.types.Part.from_text(text=prompt)
    parts.append(part)

    # Make config
    config = genai.types.GenerateContentConfig(response_modalities=["IMAGE"])

    # Run
    click.echo("Start generating")
    response = client.models.generate_content(model="gemini-2.5-flash-image", contents=parts, config=config)

    # Parse the result
    for candidate in response.candidates:
        for part in candidate.content.parts:
            if part.inline_data:
                out_path = Path(image_output)
                out_path.write_bytes(part.inline_data.data)

                return click.echo(f"Result saved to {out_path.resolve()}")

    raise RuntimeError("No image returned")


def _load_image(path: Path) -> genai.types.Part:
    if not path.exists():
        raise FileNotFoundError(path)

    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        raise ValueError(f"Unknown mime type: {path}")

    return genai.types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type)


if __name__ == "__main__":
    cli()
