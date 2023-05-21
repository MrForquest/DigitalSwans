import os

import numpy as np
from PIL import Image
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor


class Solver:
    def __init__(self, path_to_weights):
        # Load config from a config file
        cfg = get_cfg()
        cfg.merge_from_file(
            model_zoo.get_config_file(
                "COCO-Detection/retinanet_R_50_FPN_1x.yaml")
        )
        cfg.MODEL.WEIGHTS = path_to_weights
        cfg.MODEL.DEVICE = "cpu"
        self.predictor = DefaultPredictor(cfg)
        self.result = {"klikun": 0, "shipun": 0, "malyj": 0}
        self.threshold = 0.6

    def predict_by_path(self, img_path):
        pil_img = Image.open(img_path)
        return self.predict_swans(pil_img)

    def predict_swans(self, img):
        image = img
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = np.array(image)
        # image = image[:, :, ::-1]

        outputs = self.predictor(image)

        # Display predictions
        preds = outputs["instances"].pred_classes.tolist()
        scores = outputs["instances"].scores.tolist()
        bboxes = outputs["instances"].pred_boxes

        for j, bbox in enumerate(bboxes):
            bbox = bbox.tolist()

            score = scores[j]
            pred = preds[j]

            if score > self.threshold:
                if pred == 0:
                    self.result["klikun"] += 1
                elif pred == 1:
                    self.result["shipun"] += 1
                elif pred == 2:
                    self.result["malyj"] += 1

        return self.result


class SwanAccountant:
    def __init__(self):
        self.solver = Solver("cluv_detector.pth")

    def get_num_swans_by_img(self, img: Image):
        return self.solver.predict_swans(img)

    def get_num_swans_by_path(self, image_path):
        return self.solver.predict_by_path(image_path)


if __name__ == "__main__":
    solver = SwanAccountant()

    # DIR = os.path.dirname(__file__)
    DIR = r"C:\Users\folp2\Downloads\test_ai"
    for filename in os.listdir(DIR):
        file_path = os.path.join(DIR, filename)
        res = solver.get_num_swans_by_path(file_path)
        print(res)
