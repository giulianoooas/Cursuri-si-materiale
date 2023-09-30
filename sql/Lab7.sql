--2

select e.department_id, e.last_name,
e.salary, aux.salariu_mediu
from  employees e,
(
  select department_id,  round(avg(salary)) as salariu_mediu
  from employees
  group by department_id
)aux
where e.department_id = aux.department_id;

--3
select e.department_id, e.last_name,
e.salary, aux.salariu_mediu, aux.nr
from  employees e,
(
  select department_id,  round(avg(salary)) as salariu_mediu, count(employee_id) as nr
  from employees
  group by department_id
)aux
where e.department_id = aux.department_id
order by e.department_id;

--5
select e.employee_id as cod_angajat, e.salary as salariu
from employees e,
(
  select department_id, avg(salary) as medie
  from employees
  group by department_id
) aux
where aux.department_id = e.department_id
and e.salary > aux.medie;

--7
select e.employee_id as cod_angajat, e.salary as salariu
from employees e,
(
  select department_id, min(salary) as minim
  from employees
  group by department_id
) aux
where aux.department_id = e.department_id
and e.salary = aux.minim;


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

-- 11
select department_id
from departments
where department_id not in (
  select distinct department_id
  from employees
  where department_id is not NULL
);

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

--13
select l.city as locatie
from locations l,
  (
    select location_id
    from departments
    group by location_id
    having count(department_id) > 0
  ) aux
  where aux.location_id = l.location_id;
  -- 7 rezultate

--14
select job_title as Titlul_jobului
from jobs j
where not exists(select 'x'
  from employees jj, job_history jjj
  where jj.job_id = jjj.job_id
  and j.job_id = jj.job_id
);
-- 12 rezultate

select distinct job_title as Titlul_jobului
  from employees jj, job_history jjj, jobs j
  where jj.job_id = jjj.job_id
  and j.job_id = jj.job_id;
-- 8

select job_title
from jobs;
-- 20 afisari 