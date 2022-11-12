-- CTE => Common Table Expression

with

a as (
    select * from abc
)

, b as (
    select * from a
)

select
    *
from b
