# Gemini AI Tool
AI-assistant based on Gemini that lets you fill in forms as if you were talking to a human in natural language.

## How to launch
This guide assumes you have **Docker** installed.
If you don't have it, please follow the instructions on the [Docker website](https://docs.docker.com/get-docker/).

1. Clone the repository
```bash
git clone https://github.com/chmieladr/gemini-ai-tool.git
```
2. Go to the directory
```bash
cd gemini-ai-tool
```
3. Open the `.env` file and set the `GEMINI_API_KEY` variable to your actual Gemini API key.
   If you don't have it, please follow the instructions on the [Gemini website](https://aistudio.google.com/apikey).
4. Build the docker image (might require `sudo` or elevated privileges on Windows)
```bash
docker compose up --build
```
5. Open the browser and go to `http://localhost:80`

> **Note!** To see the submitted forms, you can go to `http://localhost:80/submissions` endpoint.