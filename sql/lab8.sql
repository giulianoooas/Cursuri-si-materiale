--9
select e.employee_id as cod_angajat, e.salary as salariu,
e.department_id as departament
from employees e,
(
  select department_id, max(salary) as maxim
  from employees
  group by department_id
) aux
where aux.department_id = e.department_id
and aux.maxim > 12500
order by e.department_id;

--10
select employee_id, e.department_id, e.salary
from employees e, 
(
  select distinct department_id
  from employees
  where salary = (
    select max(salary)
    from employees
    where department_id = 30
    group by department_id
  )
) aux
where e.department_id = aux.department_id;

--12
select employee_id, last_name, first_name
from employees e,
(
  select manager_id as id
  from employees
  where manager_id is not null
  group by manager_id
  having count(manager_id) >= 2
) aux
where aux.id = e.employee_id;

--exists

select employee_id, last_name, first_name
from employees e
where exists
(
  select 1
  from employees e1
  where e1.manager_id is not null
  and e1.manager_id = e.employee_id
  group by e1.manager_id
  having count(e1.manager_id) >= 2
);

--2

with tabel1 as (
  select d.department_name, sum(salary) as s, d.department_id as id, count(e.employee_id) as c
  from employees e, departments d
  where d.department_id = e.department_id
  group by d.department_id, department_name
) ,
 tabel2 as (
  select manager_id, sum(salary) as s
  from employees
  group by manager_id
)
select last_name, first_name 
from employees e, tabel1 t1, tabel2 t2
where e.department_id = t1.id
and e.employee_id = t2.manager_id
and t2.s < t1.s/t1.c;

--4
select job_title, s
from (
  select job_title, avg(salary) as s
  from employees e, jobs j
  where j.job_id = e.job_id
  group by job_title, e.job_id
  order by avg(salary) asc
)
where rownum < 4;