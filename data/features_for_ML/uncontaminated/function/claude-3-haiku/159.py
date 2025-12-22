def from_pretrained(model_config):
    """
    Loads a pre-trained model from a specified configuration.

    Args:
        model_config (dict): A dictionary containing the configuration for the pre-trained model.

    Returns:
        object: The pre-trained model instance.
    """
    # Load the pre-trained model weights and architecture from the specified configuration
    model_weights = model_config.get('weights')
    model_architecture = model_config.get('architecture')

    # Create a new instance of the model based on the architecture
    model = create_model(model_architecture)

    # Load the pre-trained weights into the model
    model.load_weights(model_weights)

    return model

def create_model(architecture):
    """
    Creates a new instance of the model based on the specified architecture.

    Args:
        architecture (str): The name or identifier of the model architecture.

    Returns:
        object: The new instance of the model.
    """
    # Implement the logic to create a new instance of the model based on the architecture
    # This could involve importing the appropriate model class, initializing it, and returning the instance
    if architecture == 'resnet50':
        return ResNet50()
    elif architecture == 'vgg16':
        return VGG16()
    else:
        raise ValueError(f'Unsupported architecture: {architecture}')