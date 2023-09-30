select e.employee_id, d.department_id
from employees e, departments d
where d.department_id(+) = e.department_id
union
select e.employee_id, d.department_id
from employees e, departments d
where d.department_id = e.department_id(+);

select d.department_id
from departments d, employees e
where lower(department_name)  like '%re%'
union
select d.department_id
from departments d, employees e
where upper(e.job_id) = 'SA_REP';

select department_id 
from departments
minus
select distinct department_id
from employees;

SELECT department_id "Cod departament"
FROM employees
WHERE upper(job_id)='HR_REP'
INTERSECT
SELECT department_id
FROM departments
WHERE lower(department_name) LIKE '%re%';

select last_name, hire_date, department_id
from employees 
where department_id in (select department_id
          from employees
            where last_name = 'Gates');
            
select employee_id
from employees
where salary > all(
  select salary 
  from employees
  where upper(job_id) like '%CLERK'
);

SELECT e.last_name, d.department_name, e.salary, j.job_title
FROM employees e, departments d, jobs j
WHERE e.department_id = d.department_id
AND e.job_id = j.job_id
AND (e.salary, e.commission_pct) IN
(SELECT salary, commission_pct
FROM employees
WHERE department_id IN
(SELECT department_id
FROM departments
WHERE location_id IN
(SELECT location_id
FROM locations
WHERE LOWER(city)= 'oxford')));
            
#15 - 18 - 19
# Tema 
#Dumitru Florentin Giuliano 

select  e.employee_id, j.job_id, e.last_name, e.salary
from employees e, jobs j
where e.job_id = j.job_id and
(e.salary > 3000 or e.salary in (
    select b.max_salary*0.5 + 0.5*j.min_salary 
    from employees aa, jobs b
    where b.job_id = aa.job_id
));

select last_name, salary
from employees
where manager_id =
    (select employee_id
    from employees
    where nvl(manager_id, 1) = 1);
    
select e.last_name, d.department_id, e.salary
from employees e, departments d
where d.department_id = e.department_id and 
(d.department_id, e.salary) in
(
  select department_id, salary
  from employees
  where nvl2(commission_pct, 1,2) = 1
);