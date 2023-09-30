select *from project;

select *
from works_on
order by project_id;

select distinct employee_id
from works_on w, project p
where p.project_id = w.project_id and p.budget = 10000;



select employee_id
from works_on
minus
select employee_id
from (
  SELECT employee_id, project_id
  FROM (SELECT DISTINCT employee_id FROM works_on) t1,
(SELECT project_id FROM project WHERE to_char(start_date, 'mm') <= 6 and to_char(start_date,'yyyy') ='2006') t2
MINUS
SELECT employee_id, project_id FROM works_on
) t3;

SELECT employee_id
FROM works_on
WHERE project_id IN
(SELECT project_id
FROM project
WHERE to_char(start_date, 'mm') <= 6 and to_char(start_date,'yyyy') ='2006')
GROUP BY employee_id
HAVING COUNT(project_id)=
(SELECT COUNT(*)
FROM project
WHERE to_char(start_date, 'mm') <= 6 and to_char(start_date,'yyyy') ='2006');

SELECT DISTINCT employee_id
FROM works_on a
WHERE NOT EXISTS
(SELECT 1
FROM project p
WHERE to_char(start_date, 'mm') <= 6 and to_char(start_date,'yyyy') ='2006'
AND NOT EXISTS
(SELECT 'x'
FROM works_on b
WHERE p.project_id=b.project_id
AND b.employee_id=a.employee_id));

SELECT DISTINCT employee_id
FROM works_on a
WHERE NOT EXISTS (
(SELECT project_id
FROM project p
WHERE to_char(start_date, 'mm') <= 6 and to_char(start_date,'yyyy') ='2006')
MINUS
(SELECT p.project_id
FROM project p, works_on b
WHERE p.project_id=b.project_id
AND b.employee_id=a.employee_id));


select distinct p.project_name
from works_on a, project p
where exists (
  select project_id
  from works_on b
  where a.project_id = b.project_id
  and b.employee_id in (
    select employee_id
  from job_history
  group by employee_id
  having count(*) = 2
  )
  group by b.project_id 
  having count(*)= (
    select count(count(employee_id))  as d
  from job_history
  group by employee_id
  having count(*) = 2
  )
)
and a.project_id = p.project_id;

--12 
-- 13