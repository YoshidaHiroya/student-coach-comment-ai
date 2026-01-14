# student-coach-comment-ai

Learning log analysis & comment generation project.

## Overview
This project builds a local analytics pipeline using:
- dbt
- DuckDB
- CSV-based learning logs

## Architecture
- Data warehouse: DuckDB
- Transformation: dbt
- Data source: CSV (seed)

## Directory Structure
```text
student_coach/
├─ models/
│  ├─ staging/
│  └─ marts/
├─ seeds/
└─ dbt_project.yml
```
## Articles
- [Zenn] Windows + dbt + DuckDB 環境構築
