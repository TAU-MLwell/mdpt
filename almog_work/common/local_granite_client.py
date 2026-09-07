"""Direct local loading of an IBM Granite model using transformers.

No server, no Ollama, no vLLM, no API keys. This loads the model weights
into the current Python process, following IBM's official usage pattern:
https://github.com/ibm-granite/granite-4.1-language-models

Model choice: ibm-granite/granite-4.1-8b (current Granite generation,
dense instruct model). Override with MDPT_LOCAL_MODEL, e.g. set it to
ibm-granite/granite-4.1-3b for faster iteration/testing.

GPU usage: this machine has GPUs available, but GPU inference here uses a
Triton kernel that needs to JIT-compile a small C extension at runtime,
which requires Python.h (the python3-dev header). That header isn't
installed system-wide and can't be added without sudo. As a workaround, we
set CPATH to a conda-forge Python 3.12 environment's include dir
(~/py312-headers-env), created once via micromamba, purely to supply that
header for Triton's compiler. Set MDPT_DEVICE=cpu to force CPU instead.
"""
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = os.getenv("MDPT_LOCAL_MODEL", "ibm-granite/granite-4.1-8b")

_HEADERS_INCLUDE_DIR = os.path.expanduser("~/py312-headers-env/include/python3.12")
if os.path.isdir(_HEADERS_INCLUDE_DIR) and _HEADERS_INCLUDE_DIR not in os.environ.get("CPATH", ""):
    os.environ["CPATH"] = _HEADERS_INCLUDE_DIR + os.pathsep + os.environ.get("CPATH", "")

_tokenizer = None
_model = None


def load_granite():
    """Load the Granite tokenizer and model once, and reuse them across calls."""
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        default_device = "cuda" if torch.cuda.is_available() else "cpu"
        device = os.getenv("MDPT_DEVICE", default_device)
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
