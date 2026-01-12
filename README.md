# Description
CLI for making images via Gemini.

# How to use

## In Docker
- create `google-sa.json` with Google Service Account Credentials
- execute:
```shell
cat > google-sa.json

docker run \
  -v $(pwd)/google-sa.json:/app/src/google-sa.json \
  -v $(pwd)/examples:/app/src/examples \
  -v $(pwd)/results:/app/src/results \
  deusalex/gemini-cli:latest \
  './cli.py run --input ./examples/input.png --prompt "Dress the woman from the original photo in clothes from additional photos" --extra-image ./examples/style1.png --extra-image ./examples/style2.png'
```
- see at result a `results/` folder

## At local
- install libs:
```shell
pip install poetry
poetry install --no-root
```
- create `google-sa.json` with Google Service Account Credentials
- execute:
```shell
export GOOGLE_APPLICATION_CREDENTIALS=google-sa.json

./cli.py run \
  --input ./examples/input.png \ 
  --prompt "Dress the woman from the original photo in clothes from additional photos" \
  --extra-image ./examples/style1.png \
  --extra-image ./examples/style2.png
```
