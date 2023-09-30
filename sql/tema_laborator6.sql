select max(salary) as Salariul_maxim
from employees
having max(salary) > 15000;

select e.last_name, e.first_name, e.employee_id, d.department_id, l.city
from employees e, departments d, locations l
where d.department_id = e.department_id
and l.location_id = d.location_id
and e.salary = (
select max(salary)
from employees
having max(salary) > 15000);

select sum(salary) as "suma salarii",city as "Oras",d.department_id,department_name as "Nume departament",job_id as "job"
from employees e join departments d
on e.department_id=d.department_id
join locations l
on d.location_id=l.location_id
where e.department_id>80
group by city,department_name,job_id, d.department_id;

select employee_id
from employees e, departments d,
(
  select dd.department_id
  from departments dd, employees ee
  where dd.department_id = ee.department_id
  and hire_date > (
    select max(eee.hire_date)
    from employees eee, departments ddd
    where eee.department_id = ddd.department_id
    and eee.department_id = 30
  )
  having count(ee.employee_id) > 8
  group by dd.department_id
) aux
where d.department_id = e.department_id
and aux.department_id = d.department_id;

