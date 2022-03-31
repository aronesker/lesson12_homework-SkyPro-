import json
from exceptions import DataLayerError, PictureWrongTypeError


class PostsHandler:

    def __init__(self, path):
        self.path = path

    def load_posts_json(self):
        """
        Загружает данные из JSON файла
        """
        try:
            with open(self.path, encoding="utf-8") as f:
                posts = json.load(f)
            return posts

        except (FileNotFoundError, json.JSONDecodeError):
            raise DataLayerError("Проблема с файлом")

    def search_posts(self, substring):
        """
        Выдает список по значению
        """
        substring_lower = substring.lower()
        posts_found = []
        posts = self.load_posts_json()
        for post in posts:
            if substring_lower in post['content'].lower():
                posts_found.append(post)

        return posts_found

    def add_new_post(self, post):
        """
        Добавляет пост в список постов
        """
        posts = self.load_posts_json()
        posts.append(post)
        self.save_posts_json(posts)

    def save_posts_json(self, posts):
        """
        Сохраняет посты в JSON файл
        """
        try:
            with open(self.path, 'w', encoding="utf-8") as f:
                json.dump(posts, f)
        except FileNotFoundError:
            raise DataLayerError


def save_uploaded_picture(picture):
    filename = picture.filename

    file_type = filename.split('.')[-1]

    if file_type not in ['j0pg', 'jpeg', 'png']:
        raise PictureWrongTypeError

    picture.save(f"uploads/images/{filename}")
    return filename
