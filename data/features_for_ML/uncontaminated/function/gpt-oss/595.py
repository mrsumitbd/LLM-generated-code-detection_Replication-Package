from typing import Any
import inspect
import sys

def inspect_embeddings(app: Any):
    """
    Inspect the embeddings object and print detailed information.

    Args:
        app: txtai Application instance
    """
    # Guard against missing application or embeddings
    if app is None:
        print("No application instance provided.")
        return

    embeddings = getattr(app, "embeddings", None)
    if embeddings is None:
        print("Application does not have an 'embeddings' attribute.")
        return

    print("\n=== Embeddings Object Inspection ===")
    print(f"Type: {type(embeddings)}")
    print(f"Class: {embeddings.__class__.__name__}")
    print(f"Module: {embeddings.__class__.__module__}")
    print(f"Docstring: {embeddings.__class__.__doc__ or 'None'}")
    print(f"Base classes: {[base.__name__ for base in embeddings.__class__.__bases__]}")
    print(f"Class annotations: {embeddings.__class__.__dict__.get('__annotations__', {})}")

    # Print class-level attributes (excluding methods and private)
    print("\n--- Class-level attributes ---")
    for name, value in sorted(embeddings.__class__.__dict__.items()):
        if name.startswith("_"):
            continue
        if inspect.isroutine(value):
            continue
        try:
            val_repr = repr(value)
        except Exception:
            val_repr = "<unrepresentable>"
        print(f"{name:30s} : {val_repr}")

    # Print instance-level attributes
    print("\n--- Instance-level attributes ---")
    # Use getmembers to include attributes from __slots__ if present
    members = inspect.getmembers(embeddings, lambda a: not(inspect.isroutine(a)))
    for name, value in sorted(members):
        if name.startswith("_"):
            continue
        try:
            val_repr = repr(value)
        except Exception:
            val_repr = "<unrepresentable>"
        print(f"{name:30s} : {val_repr}")

    # If the embeddings object has a loaded model, inspect it
    model = getattr(embeddings, "model", None)
    if model is not None:
        print("\n=== Loaded Model Inspection ===")
        print(f"Model type: {type(model)}")
        print(f"Model class: {model.__class__.__name__}")
        print(f"Model module: {model.__class__.__module__}")
        print(f"Model docstring: {model.__class__.__doc__ or 'None'}")
        # Show some common attributes that might exist on the model
        common_attrs = [
            "name",
            "config",
            "device",
            "dtype",
            "num_parameters",
            "num_layers",
            "hidden_size",
            "num_attention_heads",
            "max_position_embeddings",
            "vocab_size",
            "model_type",
            "model_name_or_path",
            "model_revision",
            "model_hash",
        ]
        for attr in common_attrs:
            if hasattr(model, attr):
                try:
                    val_repr = repr(getattr(model, attr))
                except Exception:
                    val_repr = "<unrepresentable>"
                print(f"{attr:30s} : {val_repr}")

    # Print any additional metadata that might be stored on the embeddings
    metadata_attrs = [
        "device",
        "size",
        "dim",
        "batch",
        "pooling",
        "tokenizer",
        "model_config",
        "model_kwargs",
        "model_loaded",
        "model_loaded_time",
        "model_loaded_size",
        "model_loaded_device",
        "model_loaded_path",
        "model_loaded_name",
        "model_loaded_type",
        "model_loaded_version",
        "model_loaded_hash",
    ]
    print("\n--- Additional Embeddings Metadata ---")
    for attr in metadata_attrs:
        if hasattr(embeddings, attr):
            try:
                val_repr = repr(getattr(embeddings, attr))
            except Exception:
                val_repr = "<unrepresentable>"
            print(f"{attr:30s} : {val_repr}")

    print("\n=== End of Inspection ===\n")