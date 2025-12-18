import os
import re
from urllib.parse import urlparse, parse_qs


def parse_azure_endpoint(full_endpoint: str) -> dict:
    """
    Parse Azure OpenAI endpoint URL into components.

    Example URL:
    https://oai-prd-laboratorio-de-soluciones.openai.azure.com/openai/deployments/ChatGPT4-1-mini-Lab-Soluciones-EsteUS/chat/completions?api-version=2025-01-01-preview

    Returns:
        dict with keys: base_url, deployment, api_version
    """
    parsed = urlparse(full_endpoint)

    base_url = f"{parsed.scheme}://{parsed.netloc}"

    deployment_match = re.search(r'/deployments/([^/]+)/', parsed.path)
    deployment = deployment_match.group(1) if deployment_match else None

    query_params = parse_qs(parsed.query)
    api_version = query_params.get('api-version', [None])[0]

    if not deployment or not api_version:
        raise ValueError(f"Could not parse deployment or api_version from endpoint: {full_endpoint}")

    return {
        "base_url": base_url,
        "deployment": deployment,
        "api_version": api_version
    }


def get_azure_chat_config() -> dict:
    """
    Get Azure ChatOpenAI configuration from environment variables.

    Reads AZURE_GPT_ENDPOINT and AZURE_GPT_API_KEY from environment.

    Returns:
        dict with keys: base_url, deployment, api_version, api_key
    """
    endpoint = os.getenv("AZURE_GPT_ENDPOINT")
    api_key = os.getenv("AZURE_GPT_API_KEY")

    if not endpoint:
        raise ValueError("AZURE_GPT_ENDPOINT environment variable not set")
    if not api_key:
        raise ValueError("AZURE_GPT_API_KEY environment variable not set")

    parsed_config = parse_azure_endpoint(endpoint)
    parsed_config["api_key"] = api_key

    return parsed_config


def get_azure_embeddings_config() -> dict:
    """
    Get Azure OpenAI Embeddings configuration from environment variables.

    Reads AZURE_EMBED_ENDPOINT and AZURE_EMBED_API_KEY from environment.

    Returns:
        dict with keys: base_url, deployment, api_version, api_key
    """
    endpoint = os.getenv("AZURE_EMBED_ENDPOINT")
    api_key = os.getenv("AZURE_EMBED_API_KEY")

    if not endpoint:
        raise ValueError("AZURE_EMBED_ENDPOINT environment variable not set")
    if not api_key:
        raise ValueError("AZURE_EMBED_API_KEY environment variable not set")

    parsed_config = parse_azure_endpoint(endpoint)
    parsed_config["api_key"] = api_key

    return parsed_config
