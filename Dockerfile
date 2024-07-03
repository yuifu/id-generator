# ベースイメージとしてPythonを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルを作業ディレクトリにコピー
COPY app.py .
COPY templates ./templates
COPY requirements.txt .

# 必要なPythonパッケージをインストール
RUN pip install -r requirements.txt

# Flaskアプリケーションを起動
CMD ["python", "app.py"]
