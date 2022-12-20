import datetime
import random
import re

from django.core.management.base import BaseCommand, CommandError
from movie.models import Movie, Position, Genre, Language, MovieImage, MovieTrailer
from celebrity.models import Celebrity, CelebrityImage
from comment.models import Review, Rating, Reply
from account.models import UserInfo
from group.models import Group, Discussion, Comment

import json


class Command(BaseCommand):
    help = "create test data"

    def delete_all_data(self):
        Reply.objects.all().delete()
        Review.objects.all().delete()
        Rating.objects.all().delete()

        MovieImage.objects.all().delete()
        MovieTrailer.objects.all().delete()
        CelebrityImage.objects.all().delete()

        Genre.objects.all().delete()
        Language.objects.all().delete()
        Position.objects.all().delete()
        l = Movie.objects.all()
        for i in l:
            i.genres.all().delete()
        Genre.objects.all().delete()
        Movie.objects.all().delete()
        Celebrity.objects.all().delete()

        UserInfo.objects.all().delete()

    def create_rating_and_review(self):
        movies = Movie.objects.all()

        content = "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！" \
                  "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！" \
                  "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！" \
                  "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！" \
                  "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！" \
                  "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！" \
                  "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！" \
                  "我觉得这部电影非常的好看！我觉得这部电影非常的好看！我觉得这部电影非常的好看！"

        user_pool = []
        for i in range(1, 101):
            name = "test" + str(i)
            user: UserInfo = UserInfo.objects.create_user(username=name, nickname=name, password="123")
            user.introduction = "test_introduction" + str(i)
            user.save()
            user_pool.append(user)

        for movie in movies:
            users = random.sample(user_pool, 5)
            for user in users:
                value = random.randint(1, 10)
                Rating.objects.create(movie=movie, author=user, value=value, content=content)
                movie.vote_count += 1
                movie.vote_sum += value
                movie.save()

        for movie in movies:
            users = random.sample(user_pool, 5)
            for user in users:
                title = user.username
                review = Review.objects.create(title=title, content=content, author=user, movie=movie)

                reply_users = random.sample(user_pool, 5)
                for reply_user in reply_users:
                    Reply.objects.create(content=reply_user.username, author=reply_user, review=review)

    def create_discussion_and_comment(self):
        groups = list(Group.objects.all())
        users = list(UserInfo.objects.all())

        for i in groups:
            authors = random.sample(users, 4)
            for j in authors:
                d = Discussion.objects.create(group=i, author=j, title='title', content='discussion')
                comment_author = random.sample(users, 2)
                for k in comment_author:
                    Comment.objects.create(discussion=d, author=k, content="comment")

    def create_star_movie_celebrity(self):
        movies = Movie.objects.all()
        celebrities = Celebrity.objects.all()[:1000]
        users = UserInfo.objects.all()

        for t in users:
            to_insert_movie = random.sample(list(movies), 3)
            for movie in to_insert_movie:
                t.like_movies.add(movie)

            to_insert_celebrity = random.sample(list(celebrities), 3)
            for celebrity in to_insert_celebrity:
                t.like_celebrities.add(celebrity)

    def create_group(self):
        users = UserInfo.objects.all()
        for i in range(10):
            g = Group.objects.create(name="group" + str(i), introduction=str(i))
            for j in random.sample(list(users), 5):
                g.members.add(j)

    def handle(self, *args, **options):
        # 首先删除之前表中的所有数据
        # self.delete_all_data()

        movies_file = open("movies.json", "r", encoding='utf-8')
        movie_list = json.load(movies_file)
        movies_file.close()

        celebrity_file = open("actors.json", "r", encoding='utf-8')
        celebrity_dic = json.load(celebrity_file)
        celebrity_file.close()

        created_cele_url = {}

        created_genres = {}
        created_languages = {}

        for movie_info in movie_list:
            date = movie_info['datePublished']
            y_m_d = re.search(r"(\d+)-(\d+)-(\d+)", date)
            if not y_m_d:
                print(movie_info['name'])

            movie = Movie.objects.create(
                movie_name=movie_info['name'],
                overview=movie_info['description'],
                duration=movie_info['duration'],
                release_date=datetime.date(int(y_m_d.group(1)), int(y_m_d.group(2)), int(y_m_d.group(3))),
                image=movie_info['image'],
                region=movie_info['region'],
                vote_count=0,
                vote_sum=0
            )

            genres = movie_info['genre']
            for i in genres:
                if i in created_genres:
                    genre = created_genres[i]
                else:
                    genre = Genre.objects.create(name=i)
                    created_genres[i] = genre

                movie.genres.add(genre)

            languages = movie_info['language']
            for i in languages:
                if i in created_languages:
                    language = created_languages[i]
                else:
                    language = Language.objects.create(name=i)
                    created_languages[i] = language

                movie.languages.add(language)

            all_photos = movie_info["all_photos"]
            for i in all_photos:
                MovieImage.objects.create(movie=movie, path=i)
            trailer = movie_info['trailer']
            if trailer:
                MovieTrailer.objects.create(movie=movie, path=trailer)

            celebrity_list = movie_info['director'] + movie_info['author'] + \
                             movie_info['actor'][0: min(6, len(movie_info['actor']))]  # 演员栏最多保存了6个

            position_type = [0] * len(movie_info['director']) + [1] * len(movie_info['author']) + \
                            [2] * min(6, len(movie_info['actor']))  # 演员栏最多保存了6个

            for i in range(len(celebrity_list)):
                cele_url = celebrity_list[i]['url']
                if cele_url not in celebrity_dic:
                    # 应该不会发生
                    continue

                if cele_url not in created_cele_url:
                    cele_info: dict = celebrity_dic[cele_url]

                    cele = Celebrity.objects.create(
                        celebrity_name=cele_info['name'],
                        biography=cele_info['description'],
                        image=cele_info['image'],
                        career=cele_info.get('职业') if cele_info.get('职业') else "",
                        birthday=cele_info.get('出生日期') if cele_info.get('出生日期') else "",
                        place_of_birth=cele_info.get('出生地') if cele_info.get('出生地') else "",
                        gender=0 if cele_info.get('性别') is None else 1 if cele_info.get('性别') == '男' else 2
                    )

                    created_cele_url[cele_url] = cele

                    all_photos = cele_info['all_photos']
                    for j in all_photos:
                        CelebrityImage.objects.create(celebrity=cele, path=j)

                else:
                    cele = created_cele_url[cele_url]

                Position.objects.create(
                    movie=movie,
                    celebrity=cele,
                    position=position_type[i]
                )

        self.create_rating_and_review()
        self.create_star_movie_celebrity()
        self.create_group()
        self.create_discussion_and_comment()

        self.stdout.write("创建数据成功")
