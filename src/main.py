import logging
import os
from collections import Counter

from flask import Flask, jsonify, request
from PIL import Image

# from model.swan_accountant import SwanAccountant

MAX_FILE_SIZE = 1024 * 1024 * 1024 + 1

logger = logging.getLogger(__name__)
application = Flask(__name__)
application.config["SECRET_KEY"] = "werty57i39fj92udifkdb56fwed232z"
application.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# swan_accountant = SwanAccountant()

creatures_descs = {
    0: {
        "en-name": "Swan Shipun",
        "ru-name": "Лебдедь Шипун",
    },
    1: {
        "en-name": "Swan Klikun",
        "ru-name": "Лебдедь Кликун",
    },
    2: {
        "en-name": "Swan Malyj",
        "ru-name": "Лебдедь Малый",
    },
}


def generate_answer(counter):
    answer = dict()
    answer["creatures"] = list()
    for i in counter:
        desc = creatures_descs[i].copy()
        desc["number"] = counter[i]
        creatures_descs[i]
        answer["creatures"].append(desc)
    return answer


fake_answer = {
    "creatures": [
        {
            "en_name": "Swan Shipun",
            "ru_name": "Лебдедь Шипун",
            "number": 10,
        },
        {
            "en_name": "Swan Klikun",
            "ru_name": "Лебдедь Кликун",
            "number": 20,
        },
        {
            "en_name": "Swan Malyj",
            "ru_name": "Лебдедь Малый",
            "number": 30,
        },
    ],
    "detail_info_src": "urlToFile",
}


@application.route("/load_imgs", methods=["POST"])
def load_imgs():
    print(request.files)
    files = request.files.getlist("fileURL")
    res_counter = Counter()
    for img in files:
        print(img)
        pil_img = Image.open(img)
        swan_nums = swan_accountant.get_num_swans_by_img(pil_img)
        res_counter.update(Counter(swan_nums))
        print(swan_nums)
    answer = generate_answer(res_counter)
    answer["success"] = True
    return jsonify(answer)


@application.route("/load_path", methods=["POST"])
def load_path():
    print(request.form)
    dir_path = request.form["dir_path"]
    print(dir_path)
    #
    """
    file_list = os.listdir(dir_path)
     res_counter = Counter()
    for filename in file_list:
        file_path = os.path.join(dir_path, filename)
        pil_img = Image.open(file_path)
        swan_nums = swan_accountant.get_num_swans_by_img(pil_img)
        res_counter.update(Counter(swan_nums))
        print(swan_nums)
    answer = generate_answer(res_counter)
    """
    answer = fake_answer
    answer["success"] = True
    return jsonify(answer)


def main():
    application.run(host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
