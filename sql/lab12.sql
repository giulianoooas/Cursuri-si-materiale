update emp_dfg
set job_id = 'SA_REP' 
where department_id = 80 and commission_pct is not NULL;

select *
from emp_dfg;
rollback;

define jobul 
define commision
update emp_dfg
set job_id = upper('&jobul')
where department_id = 80 and commission_pct = &commision;

create table jobs_dfg as select * from jobs;

select *
from jobs_dfg;

alter table jobs_dfg
add constraint pk_jobs_dfg primary key(job_id);

desc jobs_dfg;

alter table emp_dfg
add constraint fk_emp_jobs_dfg
foreign key(job_id) references jobs_dfg(job_id);

delete from emp_dfg
where employee_id > 206;

commit;

select employee_id
from emp_dfg
where first_name = 'Douglas'
and last_name = 'Grant';

update dept_dfg
set manager_id = (
  select employee_id
from emp_dfg
where first_name = 'Douglas'
and last_name = 'Grant'
)
where department_id = 20;

update emp_dfg
set salary = salary + 1000
where employee_id = (
   select employee_id
from emp_dfg
where first_name = 'Douglas'
and last_name = 'Grant'
);

rollback;

update emp_dfg
set (salary,commission_pct) = (
  select salary, commission_pct
  from emp_dfg e1
  where exists (
    select 1
    from emp_dfg e2
    where e2.manager_id = e1.employee_id
    and e2.salary = (
    select min(salary) 
    from emp_dfg
    ) 
  )
) where salary = (
    select min(salary) 
    from emp_dfg
  );
  
update emp_dfg e1
set e1.email = (
  select nvl(e2.last_name, '.')||e2.first_name
  from emp_dfg e2
  where e1.employee_id = e2.employee_id
) where salary = (
  select max(e2.salary)
  from emp_dfg e2
  where e2.department_id = e1.department_id
  group by e2.department_id
);

select *
from emp_dfg;

delete from dept_dfg
where not exists (
  select 1
  from emp_dfg
  where dept_dfg.department_id = emp_dfg.department_id
);

select *
from dept_dfg;

Insert into emp_mng(employee_id, last_name,first_name,salary,email, hire_date, job_id)
values(&cod,'&&nume','&&prenume',&salariu, substr('&prenume',1,1)|| substr('&nume', 1,7), sysdate, 'SA_REP');
