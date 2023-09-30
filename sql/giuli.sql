select min_salary as normal_salary 
from jobs 
where min_salary > 5000
order by min_salary asc;

describe employees;

select  employee_id, last_name, job_id, hire_date
from employees;

select last_name||', '||job_id as "Angajat si titlu"
from employees;

select employee_id||', '||first_name||', '||last_name||', '|| email || ', '|| phone_number|| ', ' || hire_date||' , '|| job_id||' , '|| salary||', '|| commission_pct||', '|| manager_id||', '|| department_id as "Informatii personale"
from EMPLOYEES;

select  job_id, salary, salary + 0.4 * salary as marire_lunara
from employees
where salary > 7000
order by salary desc;

select  job_id, salary, salary + 0.4 * salary as marire_lunara
from employees
where 1.4*salary > 7000
order by marire_lunara desc;

select sysdate
from dual;
select  to_char(sysdate, 'DD/MM/YYYY HH24:MI') as data
from dual;

SELECT SYSDATE
FROM
EMPLOYEES;

select job_id, first_name|| ' '||last_name as name, to_char(hire_date, 'DAY') as zi
from employees;

select  first_name|| ' '||last_name as name, to_char(hire_date, 'yyyy ddd') as data
from employees
order by 2 asc;

select  first_name|| ' '||last_name as name, salary
from employees
where salary > 2850;

select first_name|| ' '||last_name as name, job_id, hire_date
from employees
where  hire_date  between '20- FEB-1987' and '1- MAY- 1989';

select first_name|| ' '||last_name as name, department_id
from employees
where department_id in (10,30,50)
order by    first_name asc;

select job_id
from EMPLOYEES;

select first_name|| ' '||last_name as name, job_id, salary
from EMPLOYEES
where( job_id like '%CLERK' or job_id like '%REP') and not salary in (1000,2000,3000) ;

select first_name|| ' '||last_name as name, job_id
from EMPLOYEES
where manager_id IS NULL;

select first_name|| ' '||last_name as name, salary, commission_pct
from EMPLOYEES
where salary > (salary*commission_pct)*5;


