-- Dumitru Florentin Giuliano
-- Grupa 133

-- ex 4
select d.department_name as nume_departament, 
e.last_name||' '||e.first_name as nume_angajat,
e.salary as salariul
from employees  e, departments d, 
(
  select department_id, min(salary) as salary
  from employees
  group by department_id
)  aux
where aux.department_id = e.department_id
and d.department_id = e.department_id
and e.salary = aux.salary
order by 3 asc;
-- am 12 afisari

--6
-- rezolvarea cu max

select e.last_name||' '||e.first_name as nume_angajat,
e.salary as salariul
from employees e,
(
  select max(avg(salary)) as salary
  from employees
  group by department_id
) aux
where e.salary > aux.salary;
-- 1 rezultat

select last_name||' '||first_name as nume_angajat,
salary as salariul
from employees
where salary > all(
  select avg(salary) as salary
  from employees
  group by department_id
);
-- 1 rezultat

-- 8
select d.department_name as nume_departament,
e.last_name||' '||e.first_name as nume_angajat
from departments d, employees e,
(
  select department_id as department,
  min(hire_date) as hire
  from employees
  group by department_id
) aux
where d.department_id = e.department_id
and aux.department = d.department_id
and hire_date = hire
order by 1 desc;
-- 12 rezultate