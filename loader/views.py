from exceptions import DataLayerError, PictureWrongTypeError

import os
import sys

sys.path.append(os.path.abspath('..'))

from flask import Blueprint, render_template, request
from functions import PostsHandler, save_uploaded_picture
import logging

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')
logging.basicConfig(filename="basic.log", level=logging.INFO)

@loader_blueprint.route('/post')
def create_post_page():
    return render_template("post_form.html")


@loader_blueprint.route('/post', methods=['POST'])
def create_post_from_data():
    picture = request.files.get("picture", None)
    content = request.form.get("content", None)
    posts_handler = PostsHandler("posts.json")

    if not picture or not content:
        logging.exception('Ошибка при загрузке файла')
        return "Данные не были загружены"

    try:
        picture_path = save_uploaded_picture(picture)
    except PictureWrongTypeError:
        logging.info('Неверный формат файла')
        return "Неверный формат файла"
    except FileNotFoundError:
        return "Файл не найден, проверьте путь к файлу"

    picture_url = "/" + picture_path

    post_object = {"pic": picture_url, "content": content}

    try:
        posts_handler.add_post(post_object)
    except DataLayerError:
        return "Не удалось добавить пост"

    return render_template("post_upload.html", picture_url=picture_url, content=content)
