import llm
from llm.default_plugins.openai_models import Chat, Completion
from pathlib import Path
import json
import time
import httpx
from typing import Optional
from pydantic import Field

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

    class Options(llm.Options):
        prefill: Optional[str] = Field(
            description="Initial text for the model's response (beta feature). Uses DeepSeek's Chat Prefix Completion.",
            default=None
        )
        response_format: Optional[str] = Field(
            description="Format of the response (e.g., 'json_object').",
            default=None
        )

    def execute(self, prompt, stream, response, conversation):
        messages = []
        if conversation is not None:
            for prev_response in conversation.responses:
                messages.append({"role": "user", "content": prev_response.prompt.prompt})
                messages.append({"role": "assistant", "content": prev_response.text()})

        messages.append({"role": "user", "content": prompt.prompt})

        # Handle prefill option
        if prompt.options.prefill:
            messages.append({
                "role": "assistant",
                "content": prompt.options.prefill,
                "prefix": True  # Ensure the prefix parameter is set to True
            })

        response._prompt_json = {"messages": messages}
        kwargs = self.build_kwargs(prompt)

        # Set max_tokens to 8192 (within the valid range for Beta API)
        kwargs["max_tokens"] = 8192

        # Handle response_format option
        if prompt.options.response_format:
            kwargs["response_format"] = {"type": prompt.options.response_format}

        # Remove 'prefill' and 'response_format' from kwargs if they are there
        kwargs.pop('prefill', None)
        kwargs.pop('response_format', None)

        client = self.get_client()

        try:
            completion = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=stream,
                **kwargs,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content is not None:
                    yield content

            response.response_json = {"content": "".join(response._chunks)}
        except httpx.HTTPError as e:
            raise llm.ModelError(f"DeepSeek API error: {str(e)}")

class DeepSeekCompletion(Completion):
    needs_key = "deepseek"
    key_env_var = "LLM_DEEPSEEK_KEY"

    def __init__(self, model_id, **kwargs):
        super().__init__(model_id, **kwargs)
        self.api_base = "https://api.deepseek.com/beta"  # Use beta API

    def __str__(self):
        return f"DeepSeek Completion: {self.model_id}"

    class Options(llm.Options):
        prefill: Optional[str] = Field(
            description="Initial text for the model's response (beta feature). Uses DeepSeek's Completion Prefix.",
            default=None
        )
        response_format: Optional[str] = Field(
            description="Format of the response (e.g., 'json_object').",
            default=None
        )

    def execute(self, prompt, stream, response, conversation):
        messages = []
        if conversation is not None:
            for prev_response in conversation.responses:
                messages.append(prev_response.prompt.prompt)
                messages.append(prev_response.text())
        messages.append(prompt.prompt)

        full_prompt = "\n".join(messages)

        # Handle prefill option
        if prompt.options.prefill:
            full_prompt += f"\n{prompt.options.prefill}"

        response._prompt_json = {"prompt": full_prompt}
        kwargs = self.build_kwargs(prompt)

        # Set max_tokens to 8192 (within the valid range for Beta API)
        kwargs["max_tokens"] = 8192

        # Handle response_format option
        if prompt.options.response_format:
            kwargs["response_format"] = {"type": prompt.options.response_format}

        # Remove 'prefill' and 'response_format' from kwargs if they are there
        kwargs.pop('prefill', None)
        kwargs.pop('response_format', None)

        client = self.get_client()

        try:
            completion = client.completions.create(
                model=self.model_name,
                prompt=full_prompt,
                stream=stream,
                **kwargs,
            )

            for chunk in completion:
                text = chunk.choices[0].text
                if text:
                    yield text

            response.response_json = {"content": "".join(response._chunks)}
        except httpx.HTTPError as e:
            raise llm.ModelError(f"DeepSeek API error: {str(e)}")

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
