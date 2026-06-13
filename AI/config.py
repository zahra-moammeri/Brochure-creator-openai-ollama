import openai

MODEL = "llama3.2"

openai = openai.OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}