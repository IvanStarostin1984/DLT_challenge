create or replace table leaderboard_daily as
select
    author_identity,
    commit_day,
    count(*) as commit_count
from commits_flat
group by author_identity, commit_day;
