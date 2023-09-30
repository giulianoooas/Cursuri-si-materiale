INSERT INTO DEPT_dfg (department_id, department_name)
VALUES (300, 'Programare') ;

INSERT INTO emp_dfg
VALUES (250, 'Giuliano', 'Dumitru', 'giulia@yahoo.com', null, sysdate, 'programaer', null,null,null , 300);
COMMIT;

INSERT INTO emp_dfg (employee_id, last_name, first_name, email, hire_date, job_id, department_id)
VALUES (251, 'Traian', 'Custura', 'traian@yahoo.com', sysdate, 'chitar', 300);
COMMIT;

select *
from emp1_dfg;

create table emp1_dfg as select * from employees;
delete from emp1_dfg;

insert into emp1_dfg
select *
from employees
where commission_pct > 0.25;

insert into emp1_dfg 
select *
from employees
where salary = (
  select max(salary)
  from employees
);

insert into emp1_dfg 
select *
from employees
where salary = (
  select min(salary)
  from employees
);

accept nume prompt 'numele'
accept prenume prompt 'prenume'
INSERT INTO emp_dfg (employee_id, last_name, first_name, email, hire_date, job_id, department_id)
VALUES (2322, '&nume', '&prenume', substr('&prenume',0,0)||substr('&nume',0,7)||'@yahoo.com', sysdate, 'chitar', 300);
COMMIT;

select * from emp_dfg;

ccreate table emp2_dfg as select * from employees;
delete from emp2_dfg;

create table emp0_dfg as select * from employees;
delete from emp0_dfg;

insert first
when department_id = 80 then into emp0_dfg
when salary < 5000 then into emp1_dfg
when salary >= 5000 and salary <= 10000 then into emp2_dfg
when salary > 10000 then into emp3_dfg
select * from employees;
