select count(*)
from employees;--107

select count(department_id)
from employees;--106, deoarece un angajat nu are setat departamentul

select count(employee_id)
from employees;

select count(department_id)
from departments;

select department_id,count(*)
from employees
-- where
-- and
group by department_id
-- having
order by 2 asc;

select d.department_name,d.department_id, count(e.employee_id), e.salary, count(e.salary)
from departments d, employees e
where d.department_id = e.department_id
group by d.department_name, d.department_id,e.salary;

select d.department_name,d.department_id, count(e.employee_id) as Angajati
from departments d, employees e
where d.department_id = e.department_id(+)
group by d.department_name, d.department_id;

select d.department_name,d.department_id, count(e.employee_id) as Angajati
from departments d, employees e
where d.department_id = e.department_id(+)
having count(e.employee_id) >= 5 -- asa merge
group by d.department_name, d.department_id;

select distinct j.job_id, max(salary),min(salary), sum(salary), round(avg(salary))
from employees e,jobs j
where j.job_id = e.job_id
group by j.job_id;

select count( distinct manager_id) Managerii
from employees; -- 18 

select manager_id
from employees
where manager_id is not null
group by manager_id;

select max(salary) - min(salary) as diferenta
from employees
group by job_id;

select d.department_id, d.department_name, max(salary)
from employees e, departments d
where e.department_id = d.department_id 
having max(salary) > 7000
group by d.department_id, d.department_name;

select min(avg(salary))
from employees
group by job_id;

select job_id, avg(salary)
from employees
group by job_id
having avg(salary) = (
select min(avg(salary))
from employees
group by job_id);
-- PK_CLERK 2780


select d.department_id, d.department_name, round(avg(salary))
from employees e, departments d
where e.department_id = d.department_id 
group by d.department_id, d.department_name
order by 3 asc;


select dd.department_id, dd.department_name
from employees ee, departments dd
where ee.department_id = dd.department_id 
having round(avg(salary)) = (select max(round(avg(salary)))
from employees e, departments d
where e.department_id = d.department_id 
group by d.department_id, d.department_name)
group by dd.department_id, dd.department_name;

-- 14 - 25