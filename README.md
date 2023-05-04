## アプリケーションの概要

Todoを管理できるアプリケーションです。

<ここに画像入れる>

## アプリケーションの機能一覧

・Todo作成機能
・Todo削除機能
・Todo編集機能
・Todo保存機能
・ログイン機能
・ログアウト機能
・ユーザー作成機能
・ユーザー退会機能

## 使用技術
フロントエンド
・React.js

バックエンド
・Django REST framework

インフラ
・AWS(CloudFront,EC2,S3,RDS)

開発環境
・Docker

## 開発環境(Docker)の動かし方



## 公開URL



# django-react-nginx-mysql-docker

## Modify the time for wait.sh

Modify the timeout seconds in `frontend/nginx/wait.sh` if the frontend nginx server starts earlier than react. (e.g. 15 -> 120)

```
WAITFORIT_TIMEOUT=${WAITFORIT_TIMEOUT:-15}
```

## `backend/web-back/.env` just for development

```
SECRET_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
DEBUG=False
HOST=db
USER=user
```

## migration for database
```
$ docker-compose run --rm web-back sh -c "python manage.py makemigrations"
$ docker-compose run --rm web-back sh -c "python manage.py migrate"
```

## create superuser

```
docker-compose run --rm web-back sh -c "python manage.py createsuperuser"
```

## add packages

```
docker-compose run --rm web-front sh -c "yarn add next react"
```

## run server

```
docker-compose up --build
```
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
django-react-nginx-mysql-docker/README.md at main · greenteabiscuit/django-react-nginx-mysql-docker 