import os
import time
import duckdb
import pandas as pd
from openai import OpenAI

# =========================
# 設定
# =========================
DB_PATH = "dev.duckdb"
IN_TABLE = "mart_teacher_comment_request"
OUT_CSV = "outputs/comments.csv"

MODEL = "gpt-4o-mini"
LIMIT = 5   # まずは5件で安全に

# =========================
# OpenAI クライアント
# =========================
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY が設定されていません。\n"
        "PowerShellで $env:OPENAI_API_KEY=\"sk-...\" を実行してください。"
    )

client = OpenAI(api_key=api_key)

# =========================
# プロンプト
# =========================
SYSTEM_INSTRUCTION = (
    "あなたは塾講師です。"
    "生徒の学習ログ要約をもとに、講師コメントを日本語で作成してください。"
    "前向きで具体的に、1〜2文で書いてください。"
    "改善アドバイスは1つだけ含めてください。"
    "絵文字や箇条書きは使わないでください。"
)

def build_input(summary_text: str) -> str:
    return f"""学習ログ要約:
{summary_text}
"""

# =========================
# メイン処理
# =========================
def main():
    # DuckDB 接続
    con = duckdb.connect(DB_PATH)

    query = f"""
        select
            student_id,
            event_date,
            summary_text
        from {IN_TABLE}
        order by event_date desc, student_id
        limit {LIMIT}
    """
    rows = con.execute(query).fetchall()

    if not rows:
        raise RuntimeError(
            f"{IN_TABLE} にデータがありません。"
            "dbt run でマートが作成されているか確認してください。"
        )

    results = []

    for student_id, event_date, summary_text in rows:
        response = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": build_input(summary_text)},
            ],
        )

        comment = response.output_text.strip()

        results.append(
            {
                "student_id": student_id,
                "event_date": str(event_date),
                "summary_text": summary_text,
                "comment": comment,
            }
        )

        # レート制限対策（軽く待つ）
        time.sleep(0.2)

    df = pd.DataFrame(results)

    # CSV 出力（Excel対応）
    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Saved CSV: {OUT_CSV} (rows={len(df)})")

    # DuckDB にも保存（任意だがポートフォリオ的に◎）
    con.execute("create or replace table comments as select * from df")
    print("Saved table: comments (in DuckDB)")

# =========================
if __name__ == "__main__":
    main()
