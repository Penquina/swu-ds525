
-- Use the `ref` function to select from other models
/*
ref = reference ไปที่  my_first_dbt_model.sql
*/
select *
from {{ ref('my_first_dbt_model') }}
where id = 1
