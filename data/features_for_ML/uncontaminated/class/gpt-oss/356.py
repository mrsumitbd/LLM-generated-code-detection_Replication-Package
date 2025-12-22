import re
from typing import Any, Callable, Iterable, Optional, Union

try:
    from transformers import AutoTokenizer
except ImportError as exc:
    raise ImportError(
        "The `transformers` library is required for HuggingfaceTokenizer. "
        "Install it via `pip install transformers`."
    ) from exc


class HuggingfaceTokenizer:
    """
    A lightweight wrapper around Hugging Face tokenizers that supports optional
    sequence length truncation/padding and custom cleaning functions.
    """

    def __init__(
        self,
        name: str,
        seq_len: Optional[int] = None,
        clean: Optional[Callable[[str], str]] = None,
        **kwargs: Any,
    ):
        """
        Parameters
        ----------
        name : str
            The name or path of the pretrained tokenizer.
        seq_len : int, optional
            If provided, the tokenizer will truncate/pad sequences to this length.
        clean : callable, optional
            A function that takes a string and returns a cleaned string.
        **kwargs
            Additional keyword arguments passed to `AutoTokenizer.from_pretrained`.
        """
        self.name = name
        self.seq_len = seq_len
        self.clean = clean

        # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(name, **kwargs)

        # If the tokenizer does not have a pad token, set one
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token or self.tokenizer.cls_token

    def __call__(
        self,
        sequence: Union[str, Iterable[str]],
        **kwargs: Any,
    ) -> Any:
        """
        Tokenize the input sequence(s).

        Parameters
        ----------
        sequence : str or iterable of str
            The text(s) to tokenize.
        **kwargs
            Additional keyword arguments passed to the tokenizer call.

        Returns
        -------
        dict
            The tokenizer output, typically containing `input_ids`, `attention_mask`, etc.
        """
        # Ensure we have an iterable of strings
        if isinstance(sequence, str):
            texts = [sequence]
        else:
            texts = list(sequence)

        # Apply cleaning if a clean function is provided
        cleaned_texts = [self._clean(text) for text in texts]

        # Tokenize
        tokenized = self.tokenizer(
            cleaned_texts,
            padding="max_length" if self.seq_len else False,
            truncation=True if self.seq_len else False,
            max_length=self.seq_len,
            return_tensors="pt",
            **kwargs,
        )
        return tokenized

    def _clean(self, text: str) -> str:
        """
        Apply the cleaning function to a single string.

        Parameters
        ----------
        text : str
            The input text.

        Returns
        -------
        str
            The cleaned text.
        """
        if self.clean is None:
            return text
        if callable(self.clean):
            return self.clean(text)
        # If clean is a regex pattern string, perform a simple substitution
        if isinstance(self.clean, str):
            return re.sub(self.clean, "", text)
        # Fallback: return text unchanged
        return text