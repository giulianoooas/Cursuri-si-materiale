create table ANGAJATI_dfg(cod_ang number(4), nume varchar2(20), prenume varchar2(20), email
char(15), data_ang date, job varchar2(10), cod_sef number(4), salariu number(8, 2), cod_dep
number(2));

drop table ANGAJATI_dfg;

create table ANGAJATI_dfg(cod_ang number(4) constraint primar primary key, nume varchar2(20) constraint null1 not null, prenume varchar2(20), email
char(15), data_ang date default sysdate, job varchar2(10), cod_sef number(4), salariu number(8, 2) constraint null2 not null, cod_dep
number(2));

SELECT constraint_name, constraint_type, table_name
FROM     user_constraints
WHERE  lower(table_name) IN ('angajati_dfg');

create table ANGAJATI_dfg(
cod_ang number(4) ,
nume varchar2(20) constraint null1 not null, 
prenume varchar2(20),
email char(15), 
data_ang date default sysdate, 
job varchar2(10), cod_sef number(4), 
salariu number(8, 2) constraint null2 not null, 
cod_dep number(2),
constraint primar primary key ( cod_ang)
);

insert into ANGAJATI_dfg (Cod_ang, Nume, Prenume, Job, Salariu, Cod_dep)
values (100, 'Nume1', 'Prenume1','Director', 20000, 10);
insert into ANGAJATI_dfg
values (101, 'Nume2', 'Prenume2', 'Nume2@email.com', to_date('02-02-2004', 'dd-mm-yyyy'), 'Inginer', 100, 10000, 10);
insert into ANGAJATI_dfg
values (102, 'Nume3', 'Prenume3', 'Nume3', to_date('05-06-2004', 'dd-mm-yyyy'), 'Analist', 101, 5000, 20);
insert into ANGAJATI_dfg (Cod_ang, Nume, Prenume, Job, Cod_sef, Salariu, Cod_dep)
values (103, 'Nume4', 'Prenume4', 'Inginer', 100, 9000, 20);
insert into ANGAJATI_dfg
values (104, 'Nume5', 'Prenume5', 'Nume5', Null, 'Analist', 101, 3000, 30);

desc ANGAJATI_dfg;

create table ANGAJATI10_dfg as
select *
from ANGAJATI_dfg
where cod_dep = 10;

select *
from ANGAJATI_dfg
where cod_dep = 10;

alter table angajati10_dfg
add constraint pk_anj_dfg  primary key(cod_ang);

alter table angajati_dfg
add(comision number(4,2));

alter table angajati_dfg
modify (comision number(2,2));

alter table angajati_dfg
modify (salariu number(10,2));

alter table angajati_dfg
modify (salariu default 1000);

insert into ANGAJATI_dfg (Cod_ang, Nume, Prenume, Job, Cod_dep)
values (105, 'Nume1', 'Prenume1','Director', 10);

update angajati_dfg
set comision = 0.1
where upper(job) like 'A%';

alter table angajati_dfg
modify (email varchar2(20));

alter table angajati_dfg
add (nr_telefon varchar2(20) default '021.1222');

alter table angajati_dfg
drop column nr_telefon;

rename angajati_dfg to angajati3_dfg;

rename angajati3_dfg to angajati_dfg;

drop table angajati10_dfg;
select * from angajati10_dfg;

rollback;

create table DEPARTAMENTE_dfg (cod_dep number(2), nume varchar2(15), cod_director number(4));

alter table departamente_dfg 
add constraint pk_dp_dfg primary key (cod_dep);

alter table departamente_dfg 
modify( nume not null);

insert into departamente_dfg
values(10    ,'Administrativ',    100);
insert into departamente_dfg
values(20, 'Proiectare',    101);
insert into departamente_dfg
values(30, 'Programare',    Null);

alter table angajati_dfg
add constraint A foreign key (cod_dep) references departamente_dfg (cod_dep);