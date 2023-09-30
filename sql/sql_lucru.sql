select  concat(last_name, ' ')||first_name as name
from employees
where salary > 500 and initcap(first_name) like first_name and last_name like 'A%'
order by salary*1.4
asc;