import llm
from llm.default_plugins.openai_models import Chat, Completion
from pathlib import Path
import json
import time
import httpx

def get_deepseek_models():
    return fetch_cached_json(
        url="https://api.deepseek.com/v1/models",
        path=llm.user_dir() / "deepseek_models.json",
        cache_timeout=3600,
    )["data"]

def get_model_ids_with_aliases(models):
    return [(model['id'], []) for model in models]

class DeepSeekChat(Chat):
    needs_key = "deepseek"
    key_env_var = "LLM_DEEPSEEK_KEY"

    def __init__(self, model_id, **kwargs):
        super().__init__(model_id, **kwargs)
        self.api_base = "https://api.deepseek.com/beta"  # Use beta API

    def __str__(self):
        return f"DeepSeek Chat: {self.model_id}"

class DeepSeekCompletion(Completion):
    needs_key = "deepseek"
    key_env_var = "LLM_DEEPSEEK_KEY"

    def __init__(self, model_id, **kwargs):
        super().__init__(model_id, **kwargs)
        self.api_base = "https://api.deepseek.com/beta"  # Use beta API

    def __str__(self):
        return f"DeepSeek Completion: {self.model_id}"

@llm.hookimpl
def register_models(register):
    key = llm.get_key("", "deepseek", "LLM_DEEPSEEK_KEY")
    if not key:
        return
    try:
        models = get_deepseek_models()
        models_with_aliases = get_model_ids_with_aliases(models)
        for model_id, aliases in models_with_aliases:
            register(
                DeepSeekChat(
                    model_id=f"deepseekchat/{model_id}",
                    model_name=model_id,
                ),
                aliases=[model_id]
            )
            register(
                DeepSeekCompletion(
                    model_id=f"deepseekcompletion/{model_id}",
                    model_name=model_id,
                ),
                aliases=[f"{model_id}-completion"]
            )
    except DownloadError as e:
        print(f"Error fetching DeepSeek models: {e}")

class DownloadError(Exception):
    pass

def fetch_cached_json(url, path, cache_timeout, headers=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file() and time.time() - path.stat().st_mtime < cache_timeout:
        with open(path, "r") as file:
            return json.load(file)

    try:
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        with open(path, "w") as file:
            json.dump(response.json(), file)
        return response.json()
    except httpx.HTTPError:
        if path.is_file():
            with open(path, "r") as file:
                return json.load(file)
        else:
            raise DownloadError(f"Failed to download data and no cache is available at {path}")

@llm.hookimpl
def register_commands(cli):
    @cli.command()
    def deepseek_models():
        "List available DeepSeek models"
        key = llm.get_key("", "deepseek", "LLM_DEEPSEEK_KEY")
        if not key:
            print("DeepSeek API key not set. Use 'llm keys set deepseek' to set it.")
            return
        try:
            models = get_deepseek_models()
            models_with_aliases = get_model_ids_with_aliases(models)
            for model_id, aliases in models_with_aliases:
                print(f"DeepSeek Chat: deepseekchat/{model_id}")
                print(f"  Aliases: {model_id}")
                print(f"DeepSeek Completion: deepseekcompletion/{model_id}")
                print(f"  Aliases: {model_id}-completion")
                print()
        except DownloadError as e:
            print(f"Error fetching DeepSeek models: {e}")
