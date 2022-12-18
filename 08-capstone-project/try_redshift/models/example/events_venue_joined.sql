select
    eventname
    , venuename
    , venuecity
from {{ ref('stg_events')}} as e
join {{ ref('stg_venues')}} as v
on e.venueid = v.venueid
