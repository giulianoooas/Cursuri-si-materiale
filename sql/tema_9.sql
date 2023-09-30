-- Dumitru Florentin Giuliano
-- grupa 133

-- ex 12

-- a

with ajutator as (
  select employee_id
  from works_on
  where project_id in (
    select project_id
    from works_on
    where employee_id = 200
  )
  group by employee_id
  having count(*) = (
    select count(project_id)
    from works_on
    where employee_id = 200
  )
)
select distinct last_name||' '|| first_name as nume
from employees e, ajutator w
where e.employee_id = w.employee_id
and e.employee_id <> 200;
-- 3 afisari

-- b 
with ajutator1 as (
  select employee_id, count(*) as c
  from works_on
  where project_id in (
    select project_id
    from works_on
    where employee_id = 200
  )
  group by employee_id
  having count(*) >= 0
),
ajutator2 as (
  select employee_id, count(*) as c
  from works_on
  group by employee_id
  having count(*) <= (
    select count(project_id)
    from works_on
    where employee_id = 200
  )
)
select distinct last_name||' '|| first_name as nume
from employees e, ajutator1 a1, ajutator2 a2
where e.employee_id = a1.employee_id
and a2.employee_id = a1.employee_id
and a1.c = a2.c and
e.employee_id <>200;
-- 5 afisari

--ex 13
with ajutator1 as (
  select employee_id, count(*) as c
  from works_on
  where project_id in (
    select project_id
    from works_on
    where employee_id = 200
  )
  group by employee_id
  having count(*) = (
    select count(project_id)
    from works_on
    where employee_id = 200
  )
),
ajutator2 as (
  select employee_id, count(*) as c
  from works_on
  group by employee_id
  having count(*) = (
    select count(project_id)
    from works_on
    where employee_id = 200
  )
)
select distinct last_name||' '|| first_name as nume
from employees e, ajutator1 a1, ajutator2 a2
where e.employee_id = a1.employee_id
and a2.employee_id = a1.employee_id
and a1.c = a2.c
and e.employee_id <>200;

-- 2 afisari
