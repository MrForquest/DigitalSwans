import os

import torch
import torchvision.transforms as transforms
from PIL import Image

DIR = os.path.dirname(__file__)



class Solver:
    def __init__(self, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),  # Преобразование размера изображения
                transforms.ToTensor(),  # Преобразование в тензор
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                )
                # Нормализация значений пикселей
            ]
        )

    def solve_by_path(self, image_path):
        image = Image.open(image_path)
        return self.solve(image)

    def solve(self, image):
        if image.mode != "RGB":
            image = image.convert("RGB")
        objects = self.detector.detect(image)
        counted = {
            0: 0,
            1: 0,
            2: 0,
        }
        if objects is None:
            return counted

        for obj in objects:
            if obj[0] == "bird":
                cutted_img = image.crop(obj[-1])
                cutted_img = self.transform(cutted_img).unsqueeze(0).to("cpu")
                preds = self.predictor(cutted_img)

                if preds[0][0] == preds.max():
                    counted[0] += 1
                elif preds[0][1] == preds.max():
                    counted[1] += 1
                else:
                    counted[2] += 1
        return counted


class Detector:
    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        self.processor = torch.load(os.path.join(DIR, "processor.pth"))
        self.model = torch.load(os.path.join(DIR, "model_weights.pth")).to(self.device)

    def detect(self, image):
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        outputs = self.model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])

        results = self.processor.post_process_object_detection(
            outputs, target_sizes=target_sizes, threshold=0.9
        )[0]
        result = []
        for score, label, box in zip(
            results["scores"], results["labels"], results["boxes"]
        ):
            box = [round(i, 2) for i in box.tolist()]
            result.append(
                (self.model.config.id2label[label.item()], round(score.item(), 3), box)
            )
            return result


class SwanAccountant:
    def __init__(self):
        d = Detector()
        s = torch.load(
            os.path.join(DIR, "solver_model.pt"), map_location=torch.device("cpu")
        )
        self.solver = Solver(detector=d, predictor=s)

    def get_num_swans_by_img(self, img: Image):
        return self.solver.solve(img)

    def get_num_swans_by_path(self, image_path):
        return self.solver.solve_by_path(image_path)


if __name__ == "__main__":
    model = SwanAccountant()

    print(model.get_num_swans_by_path("img_2725.jpg"))
