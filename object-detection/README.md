# Real-time Object Detection

Detects the 80 everyday object classes from the **COCO** dataset (person, bottle, cell
phone, chair, car and more) in your webcam feed. It uses the pre-trained **SSD MobileNet v3
Large** model through OpenCV's DNN module, so no TensorFlow install is needed.

```bash
cd object-detection
python object_detection.py   # q to quit
```

Each detection gets a green box with its label and confidence. To show fewer or more
detections, change `CONFIDENCE_THRESHOLD` in the script.

## Model files (`model/`)

| File | What it is |
|------|------------|
| `frozen_inference_graph.pb` | Model weights (13 MB), from the [TensorFlow Object Detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md) (`ssd_mobilenet_v3_large_coco_2020_01_14`) |
| `ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt` | Network config for OpenCV |
| `coco.names` | Class names, one per line (the model's class IDs start at 1) |
