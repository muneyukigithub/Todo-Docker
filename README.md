## アプリケーションの概要
Todoを管理するアプリケーションです。

<p align="center">
  <img src="./img/sampleimg1.png" width="500">
</p>
<br/>

## アプリケーションの機能一覧
* Todo作成機能
* Todo削除機能
* Todo編集機能
* Todo保存機能
* ログイン機能
* ログアウト機能
* ユーザー作成機能
* ユーザー退会機能
<br/>

## 使用技術
### フロントエンド
* React.js

### バックエンド
* Django REST framework
  
### インフラ
* AWS(CloudFront,EC2,S3,RDS)
  
### 開発環境
* Docker
<br/>

## 開発環境(Docker)の動かし方

### 事前に必要なこと
* Dockerのインストール
* Gitリポジトリのクローン
  
### Dockerコンテナのビルドと起動
```
docker-compose up --build
```
  
### Dockerコンテナの起動確認
```
docker-compose ps
```
Stateが"UP"になっていればOK
  
### アプリケーションの接続
```
http://localhost/
```
<br/>

## 公開URL

https://www.todolistapp.net/
```
ログインする場合は以下のテストユーザ/パスワードを使用してください
テストユーザー：test@test.com
パスワード：password
```
  
