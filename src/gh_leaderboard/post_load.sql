create or replace table leaderboard_daily as
select
    author_identity,
    commit_day,
    count(*) as commit_count
from commits_flat
group by author_identity, commit_day;

create or replace view leaderboard_latest as
with latest_days as (
    select distinct commit_day
    from leaderboard_daily
    order by commit_day desc
    limit 2
)
select ld.*
from leaderboard_daily ld
join latest_days l on l.commit_day = ld.commit_day;
