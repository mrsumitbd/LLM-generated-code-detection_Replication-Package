import anthropic


def print_metrics(metrics, logger, roundto=4):
    """
    Print metrics using Claude to format them nicely.
    
    Args:
        metrics: Dictionary of metrics to print
        logger: Logger object to use for output
        roundto: Number of decimal places to round to (default 4)
    """
    client = anthropic.Anthropic()
    
    # Format metrics for Claude
    metrics_str = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
    
    # Use Claude to format the metrics nicely
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Format these metrics nicely for logging output. Round all numeric values to {roundto} decimal places. 
Keep the output concise and readable.

Metrics:
{metrics_str}

Return only the formatted metrics, no explanation."""
            }
        ]
    )
    
    # Extract the formatted output
    formatted_metrics = message.content[0].text
    
    # Log the formatted metrics
    logger.info(formatted_metrics)
    
    return formatted_metrics


if __name__ == "__main__":
    import logging
    
    # Set up a simple logger for testing
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Test with sample metrics
    test_metrics = {
        "accuracy": 0.95432,
        "precision": 0.92187,
        "recall": 0.88765,
        "f1_score": 0.90432,
        "loss": 0.12345678
    }
    
    print_metrics(test_metrics, logger, roundto=4)