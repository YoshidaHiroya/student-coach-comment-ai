with base as (
  select * from {{ ref('stg_study_log') }}
)

select
  student_id,
  event_date,

  count(*) as event_cnt,
  sum(coalesce(duration_sec, 0)) as total_duration_sec,

  sum(case when activity_type = 'watch' then 1 else 0 end) as watch_cnt,
  sum(case when activity_type = 'solve' then 1 else 0 end) as solve_cnt,
  sum(case when activity_type = 'review' then 1 else 0 end) as review_cnt,

  avg(score) as avg_score

from base
group by 1,2
