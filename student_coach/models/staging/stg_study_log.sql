with src as (
  select * from {{ ref('study_log') }}
)

select
  event_id,
  student_id,
  cast(event_ts as timestamp) as event_ts,
  cast(event_ts as date) as event_date,
  lower(activity_type) as activity_type,
  content_id,
  lower(content_type) as content_type,
  duration_sec,
  score,
  is_correct,
  source,
  nullif(memo, '') as memo
from src
