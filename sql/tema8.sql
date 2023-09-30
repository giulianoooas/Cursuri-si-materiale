-- Dumitru Florentin Giuliano

--13 lab 7
-- metoda 1
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

--metoda 2
select city as locatie
from locations
where location_id in (
    select location_id
    from departments
    group by location_id
    having count(department_id) > 0
  );
  --7 rezultate


--14 lab 7
select job_title as Titlul_jobului
from jobs j
where not exists(select 'x'
  from employees jj, job_history jjj
  where jj.job_id = jjj.job_id
  and j.job_id = jj.job_id
);
-- 12 rezultate

--5 lab 8
with tabel as (
  select d.department_name as nume_departmentent,  
  count(e.employee_id) as nr_angajati
  from departments d, employees e
  where d.department_id = e.department_id
  group by d.department_id, d.department_name
  order by nr_angajati desc
)
select *
from tabel
where rownum < 5;
-- 4 rezultate

-- 6 lab 8
with departamente as (
  select department_id as id, count(employeE_id) as nr
  from employees
  where department_id is not null
  group by department_id
),
manageri as (
  select manager_id as man, department_id as id, department_name as nume
  from departments
),
angajat as (
  select last_name|| ' '|| first_name as nume, employee_id as eid
  from employees
)
select 'Departamanetul '||m.nume||' este codus de '||
aj.nume|| ' si are '||d.nr||' angajati.' as informatii_departament
from manageri m, angajat aj, departamente d
where d.id = m.id and m.man(+) = aj.eid;
-- 11 afisari

-- 8 lab 8
-- case
select last_name||' '||first_name as nume_angajat,
hire_date as data_angajarii,
salary as salariul,
case to_char(hire_date, 'yyyy') 
when '1989' then salary*1.2
when '1990' then salary*1.15
when '1991' then salary *1.1
else salary
end as marire
from employees
order by marire desc;
--107

--decode
select last_name||' '||first_name as nume_angajat,
hire_date as data_angajarii,
salary as salariul,
decode( to_char(hire_date, 'yyyy'), 
'1989' , salary*1.2,
'1990' , salary*1.15,
 '1991', salary *1.1,
 salary)
 as marire
from employees
order by marire desc;
--107

-- 9 lab 8
with job_si_salatiu as (
  select j.job_id as idu,
  job_title as tit,
  sum(salary) as s
  from jobs j, employees e
  where j.job_id = e.job_id
  group by j.job_id, job_title
), 
job_si_medie as (
  select j.job_id as idu,
  avg(salary) as m
  from jobs j, employees e
  where j.job_id = e.job_id
  group by j.job_id
), 
max_salariu as(
  select max(sum(salary)) as m
  from employees
  group by job_id
)
select js.tit as numele_mucnii, 
decode(js.tit,
'Sales Representative',js.s, 
'Shipping Clerk', js.s,
'Sales Manager', js.s, 
'Stock Manager', js.s,
'Stock Clerk', js.s) as Subpunct_a,
decode (js.s,ms.m, jm.m) as Subpunct_b,
decode (js.s, ms.m, NULL, j.min_salary) as Subpunct_c
from max_salariu ms,
job_si_medie jm,
job_si_salatiu js,
jobs j
where jm.idu = js.idu
and j.job_id = jm.idu;
-- 19 afisari



-- 11 lab 8
-- metoda 1
with nr_angajati as(
  select count(employee_id) as c
  from employees
)
select  na.c as nr_angajati,
(
  select count(employee_id)
  from employees
  where to_char(hire_date, 'yyyy') = '1997'
  group by to_char(hire_date,'yyyy')
) as nr_angajati_1997,
(
  select count(employee_id)
  from employees
  where to_char(hire_date, 'yyyy') = '1998'
  group by to_char(hire_date,'yyyy')
) as nr_angajati_1998,
(
  select count(employee_id)
  from employees
  where to_char(hire_date, 'yyyy') = '1999'
  group by to_char(hire_date,'yyyy')
) as nr_angajati_1999,
(
  select count(employee_id)
  from employees
  where to_char(hire_date, 'yyyy') = '2000'
  group by to_char(hire_date,'yyyy')
) as nr_angajati_2000
from nr_angajati na;
-- 1 rezultat


--metoda 2
select count(employee_id) as nr_angajati,
nvl(sum(decode(to_char(hire_date,'YYYY'), '1997', 1)),0) as nr_angajati_1997,
nvl(sum(decode(to_char(hire_date,'YYYY'), '1998', 1)),0) as nr_angajati_1998,
nvl(sum(decode(to_char(hire_date,'YYYY'), '1999', 1)),0) as nr_angajati_1999,
nvl(sum(decode(to_char(hire_date,'YYYY'), '2000', 1)),0) as nr_angajati_2000
from employees;
-- 1 rezultat