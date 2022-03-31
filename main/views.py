from exceptions import DataLayerError

import os
import sys
sys.path.append(os.path.abspath('..'))

from flask import Blueprint, render_template, request
from functions import PostsHandler
import logging

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')
logging.basicConfig(filename="basic.log", level=logging.INFO)


@main_blueprint.route('/')
def main_page():
    return render_template("index.html")


@main_blueprint.route('/search')
def search_page():
    s = request.args.get('s', '')
    posts_handler = PostsHandler("posts.json")
    logging.info('Поиск выполнен')
    try:
        posts = posts_handler.search_posts(s)
        return render_template("post_list.html", posts=posts, s=s)
    except DataLayerError:
        return "Файл поврежден"
