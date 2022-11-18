首先在`mysql`中新建数据库`MeetMovies`， 并更改`settings.py`中`DATABASES`对应的用户名和密码。

清空原先的数据库中的数据
```shell
python manage.py flush
```

执行
```shell
python manage.py makemigrations
python manage.py migrate
```

创建测试数据(需要在执行了`migrate`的两步操作后)
```shell
python manage.py create_testdata
```

启动服务器
```shell
python manage.py runserver
```


