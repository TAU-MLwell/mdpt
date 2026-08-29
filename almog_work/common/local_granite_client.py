"""Direct local loading of an IBM Granite model using transformers.

No server, no Ollama, no vLLM, no API keys. This loads the model weights
into the current Python process, following IBM's official usage pattern:
https://github.com/ibm-granite/granite-4.1-language-models

Model choice: ibm-granite/granite-4.1-8b (current Granite generation,
dense instruct model). Chosen over the 3b variant for better extraction
quality on complex biomedical text, since this machine has enough RAM
(300GB+) to run it comfortably on CPU. Override with MDPT_LOCAL_MODEL,
e.g. set it to ibm-granite/granite-4.1-3b for faster iteration/testing.
"""
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = os.getenv("MDPT_LOCAL_MODEL", "ibm-granite/granite-4.1-8b")

_tokenizer = None
_model = None


def load_granite():
    """Load the Granite tokenizer and model once, and reuse them across calls."""
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        # Default to CPU: GPU inference here needs Triton to JIT-compile a kernel,
        # which requires Python.h (python3-dev) headers that aren't installed and
        # can't be added without sudo. Set MDPT_DEVICE=cuda to force GPU if headers
        # are available.
        device = os.getenv("MDPT_DEVICE", "cpu")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, device_map=device)
        _model.eval()

    return _tokenizer, _model


def run_granite_chat(messages, max_new_tokens=1500):
    """Run a chat-style completion locally and return only the newly generated text."""
    tokenizer, model = load_granite()

    chat_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    input_tokens = tokenizer(chat_text, return_tensors="pt").to(model.device)

    output_tokens = model.generate(**input_tokens, max_new_tokens=max_new_tokens)

    generated_only = output_tokens[0][input_tokens["input_ids"].shape[-1]:]
    return tokenizer.decode(generated_only, skip_special_tokens=True).strip()
