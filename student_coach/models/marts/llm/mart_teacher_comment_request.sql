with base as (

    select
        student_id,
        event_date,
        event_cnt,
        total_duration_sec,
        watch_cnt
    from {{ ref('fct_student_daily') }}

)

select
    student_id,
    event_date,

    -- LLM に渡すための要約テキスト
    '生徒ID ' || student_id || ' は ' ||
    event_date || ' に ' ||
    event_cnt || ' 回の学習を行い、' ||
    '合計学習時間は ' ||
    round(total_duration_sec / 60.0, 1) || ' 分でした。' ||
    '視聴学習は ' || watch_cnt || ' 回です。'
    as summary_text

from base
