def patched_forward(
    pixel_values=None,
    input_points=None,
    input_labels=None,
    image_embeddings=None,
    image_positional_embeddings=None,
    return_dict=True,
    **kwargs,
):
    # Unpack the input tensors
    batch_size = pixel_values.size(0)
    num_points = input_points.size(1)

    # Compute the image features
    image_features = image_embeddings + image_positional_embeddings

    # Compute the point-wise features
    point_features = torch.gather(image_features, 1, input_points.unsqueeze(-1).expand(-1, -1, image_features.size(-1)))

    # Compute the logits
    logits = self.classifier(point_features)

    # Compute the loss
    loss = self.loss_fn(logits, input_labels)

    # Prepare the output
    output = {
        "loss": loss,
        "logits": logits,
    }

    if return_dict:
        return output
    else:
        return loss, logits