# Docker Hubにあるpythonイメージをベースにする
FROM python:3.7-alpine

# 環境変数を設定する
ENV PYTHONUNBUFFERED 1

# コンテナ内にcodeディレクトリを作り、そこをワークディレクトリとする
RUN mkdir /code
WORKDIR /code

# ホストPCにあるrequirements.txtをコンテナ内のcodeディレクトリにコピーする
# コピーしたrequirements.txtを使ってパッケージをインストールする
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# ホストPCの各種ファイルをcodeディレクトリにコピーする
COPY . /code/