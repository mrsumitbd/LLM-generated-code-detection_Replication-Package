def patched_forward(
            pixel_values=None,
            input_points=None,
            input_labels=None,
            image_embeddings=None,
            image_positional_embeddings=None,
            return_dict=True,
            **kwargs,
        ):
            if config.variant == "monolith":
                return self.orig_forward(
                    pixel_values=pixel_values,
                    input_points=input_points,
                    input_labels=input_labels,
                    image_embeddings=image_embeddings,
                    return_dict=return_dict,
                    **kwargs,
                )
            elif config.variant == "split":
                # return_dict = get_argument(args, kwargs, signature, "return_dict")
                if config.vision_encoder:
                    # pixel_values = get_argument(args, kwargs, signature, "pixel_values")
                    image_positional_embeddings = model.get_image_wide_positional_embeddings()

                    # repeat with batch size
                    batch_size = pixel_values.shape[0]
                    image_positional_embeddings = image_positional_embeddings.repeat(batch_size, 1, 1, 1)

                    vision_outputs = model.vision_encoder(
                        pixel_values,
                        output_attentions=False,
                        output_hidden_states=False,
                        return_dict=return_dict,
                    )
                    image_embeddings = vision_outputs[0]

                    if not return_dict:
                        return (image_embeddings, image_positional_embeddings)
                    else:
                        return {
                            "image_embeddings": image_embeddings,
                            "image_positional_embeddings": image_positional_embeddings,
                        }
                else:
                    if input_points is None:
                        raise ValueError("input_points is required to export the prompt encoder / mask decoder.")

                    sparse_embeddings, dense_embeddings = model.prompt_encoder(
                        input_points=input_points,
                        input_labels=input_labels,
                        input_boxes=None,  # Not supported in the ONNX export
                        input_masks=None,  # Not supported in the ONNX export
                    )
                    outputs = model.mask_decoder(
                        image_embeddings=image_embeddings,
                        image_positional_embeddings=image_positional_embeddings,
                        sparse_prompt_embeddings=sparse_embeddings,
                        dense_prompt_embeddings=dense_embeddings,
                        multimask_output=True,  # Not supported in the ONNX export
                        attention_similarity=None,  # Not supported in the ONNX export
                        target_embedding=None,  # Not supported in the ONNX export
                    )
                    low_res_masks, iou_predictions = outputs[:2]

                    if not return_dict:
                        return (iou_predictions, low_res_masks)
                    else:
                        return {"iou_scores": iou_predictions, "pred_masks": low_res_masks}