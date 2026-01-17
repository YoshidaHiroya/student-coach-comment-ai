# student-coach-comment-ai


## 概要

本プロジェクトは、**学習ログをもとに分析・可視化・コメント生成までを一気通貫で行う分析基盤のサンプル**です。
dbt × DuckDB を用いてデータ変換・品質管理を行い、**LLM に渡す入力データ（要約テキスト）も dbt モデルとして定義**しています。


## アーキテクチャ

```
CSV（学習ログ）
  ↓ dbt seed
stg_study_log（staging）
  ↓
fct_student_daily（日次集計）
  ↓
mart_teacher_comment_request（LLM用マート）
  ↓
CSV出力 / LLM入力
```

---

## 設計のポイント

### dbt による責務分離

* **staging**：型変換・欠損処理などの前処理
* **mart（fact）**：日次単位での集計
* **LLM用マート**：LLM に渡すための要約テキスト生成

数値集計とプロンプト生成の責務を分離することで、
Python 側では「DBから読み取って LLM に渡すだけ」の構成にしています。

---

### LLM 用マートについて

LLM に直接渡せるよう、**1行＝1生徒・1日単位の自然文テキスト**を dbt で生成しています。

例：

```
生徒ID s001 は 2026-01-11 に 1 回の学習を行い、
合計学習時間は 10.0 分でした。視聴学習は 0 回です。
```

この設計により、

* プロンプト生成ロジックを SQL 側に集約
* LLM 利用時の前処理を最小化
  しています。

---

### データ品質管理

`schema.yml` を用いて、以下のテストを定義しています。

* not null（必須カラム）
* unique（イベントID）

`dbt test` により、データ品質を継続的に検証できる構成としています。

---

### intermediate モデルを省略した理由

本プロジェクトは規模が小さいため、
**staging → mart の2層構成**とし、intermediate モデルは省略しています。
複数 mart での再利用やロジックの複雑化が進んだ場合は、
intermediate 層を追加する想定です。


## 成果物

* DuckDB 内の分析用テーブル
* LLM 入力用 CSV（`outputs/mart_teacher_comment_request.csv`）
* dbt docs によるモデル・テストの可視化



## 使用技術

* Python
* dbt
* DuckDB
* OpenAI API
* Looker Studio



