def patched_forward(
            pixel_values=None,
            input_points=None,
            input_labels=None,
            image_embeddings=None,
            image_positional_embeddings=None,
            return_dict=True,
            **kwargs,
        ):
    if image_embeddings is None:
        if pixel_values is None:
            raise ValueError("Either pixel_values or image_embeddings must be provided")
        
        image_embeddings = self.image_encoder(pixel_values)
        
        if image_positional_embeddings is None:
            image_positional_embeddings = self.image_encoder.get_positional_embeddings(
                image_embeddings.shape
            )
    
    batch_size = image_embeddings.shape[0]
    
    if input_points is not None:
        points_embeddings = self.prompt_encoder(
            points=input_points,
            labels=input_labels,
        )
    else:
        points_embeddings = None
    
    sparse_embeddings, dense_embeddings = self.prompt_encoder(
        points=input_points,
        labels=input_labels,
        boxes=kwargs.get("input_boxes", None),
        masks=kwargs.get("input_masks", None),
    )
    
    low_res_masks, iou_predictions = self.mask_decoder(
        image_embeddings=image_embeddings,
        image_positional_embeddings=image_positional_embeddings,
        sparse_prompt_embeddings=sparse_embeddings,
        dense_prompt_embeddings=dense_embeddings,
        multimask_output=kwargs.get("multimask_output", True),
    )
    
    masks = self.postprocess_masks(
        low_res_masks,
        input_size=kwargs.get("input_size", None),
        original_size=kwargs.get("original_size", None),
    )
    
    if not return_dict:
        return (masks, iou_predictions)
    
    return {
        "masks": masks,
        "iou_predictions": iou_predictions,
        "image_embeddings": image_embeddings,
    }