import os
import roboflow

def build_roboflow(image_set, args, resolution):
    # Initialize the Roboflow API client
    rf = roboflow.Roboflow(api_key=args.roboflow_api_key)

    # Load the Roboflow project
    project = rf.workspace(args.roboflow_workspace).project(args.roboflow_project)

    # Load the Roboflow model
    model = project.version(args.roboflow_version).model

    # Set the image resolution
    model.setResolution(resolution)

    # Predict on the image set
    predictions = model.predict(image_set, confidence=args.confidence_threshold, overlap=args.nms_threshold)

    # Save the predictions to a file
    predictions.save(os.path.join(args.output_dir, "predictions.json"))

    return predictions