--- baza mea de date merge pe ideea ca un om poate antrena doar intr- o sala
--- si un sportiv se poate antrena intr- o singura sala in mod normal
--- un antrenor poate antrena mai multi oameni
--- un sportiv poate fi antrenat de mai multi antrenori
--- o sala poate avea mai multe aparate
--- un tip de aparate poate fi in mai multe sali
--- o sala se afla intr- o singura locatie
--- In cazul bazei mele de date sportivul trebuie sa mearga la sala antrenirului pentru a fi antrenat
 
--- 4 

create table om( --- entitate independenta
id_om number primary key,
nume varchar2(40) not null,
cnp varchar(13) not null
);

create table sportiv( --- subentitate a entitatii om
id_om number,
id_sportiv number,
frecventa_antrenamente number not null,
id_sala varchar(20) not null,
constraint PK_sportiv primary key (id_om,id_sportiv)
);

create table antrenor( --- subentitate a entitatii om
id_om number,
id_antrenor number,
raiting number,
id_sala varchar(20) not null,
constraint pk_antrenor primary key (id_om, id_antrenor)
);

create table antreneaza ( --- tabela auxiliara
id_antrenor number,
id_sportiv number,
data date not null,
constraint pk_antreneaza primary key (id_antrenor, id_sportiv,data)
);

create table sala( --- entitate independenta
id_sala varchar(20) primary key,
denumire varchar(30) not null,
id_locatie varchar(20) not null
);

create table locatie( --- entitate independeta
id_locatie varchar(20) primary key,
oras varchar(20) not null,
tara varchar(20) not null,
strada varchar(20) not null,
nr number not null
);

create table are( --- tabela auxiliara
id_sala varchar(20),
id_aparatura number,
numar_aparate number not null,
constraint pk_are primary key(id_sala, id_aparatura)
);

create table aparatura( --- tabela independenta
id_aparatura number primary key,
denumire varchar(20) not null,
grupa_musculara_lucrata varchar(30) not null
);

create table job( --- tabela independenta
id_job varchar(20) primary key,
denumire varchar(40) not null,
salariu number
);

create table lucreaza ( --- tabela auxiliara
id_om number,
id_job varchar(20),
data_anagajarii date,
constraint pk_lucreaza primary key (id_om, id_job)
);

--- acum vom adauga constrangerile

--- pentru om
alter table om add constraint cnp check (length(cnp) = 13);
alter table om add constraint cnp1 unique(cnp);

--- pentru job
alter table job add constraint u3 unique(denumire); --- nu pot exista 2 joburi cu acelasi nume

--- pentru lucreaza
alter table lucreaza add constraint fk1_lucreaza foreign key (id_om) references om(id_om) on delete cascade;
alter table lucreaza add constraint fk2_lucreaza foreign key (id_job) references job(id_job) on delete cascade;

--- pentru sportiv
alter table sportiv add constraint u1 unique (id_om);
alter table sportiv add constraint fk_sportiv foreign key (id_om) references om(id_om) on delete cascade;
alter table sportiv add constraint u_sportiv unique (id_sportiv);
alter table sportiv add constraint ne_negativ3 check (frecventa_antrenamente >= 0 and frecventa_antrenamente <= 7);

--- pentru antrenor 
alter table antrenor add constraint u2 unique (id_om);
alter table antrenor add constraint fk_antrenor foreign key (id_om) references om(id_om) on delete cascade;
alter table antrenor add constraint fk1_antrenor foreign key (id_sala) references sala(id_sala) on delete cascade;
alter table antrenor add constraint u_antrenor unique (id_antrenor);
alter table antrenor add constraint ne_negativ2 check (raiting > 0 and raiting < 6);


--- pentru antreneaza
alter table antreneaza add constraint fk1_antreneaza foreign key (id_sportiv) references sportiv(id_sportiv) on delete cascade;
alter table antreneaza add constraint fk2_antreneaza foreign key (id_antrenor) references antrenor(id_antrenor) on delete cascade;

--- pentru sala 
alter table sala add constraint fk_sala foreign key (id_locatie) references locatie(id_locatie) on delete cascade;

--- pentru are
alter table are add constraint fk1_are foreign key (id_sala) references sala(id_sala) on delete cascade;
alter table are add constraint fk2_are foreign key (id_aparatura) references aparatura(id_aparatura) on delete cascade;
alter table are add constraint ne_negativ4 check (numar_aparate >= 0);

--- pentru locatie
alter table locatie add constraint ne_negativ1 check (nr > 0);

--- 5
--- inserturile pentru tabelul locatie

insert into locatie values 
(
'IUL_MAN',
'Bucuresti',
'Romania',
'Bd Iuliu Maniu',
12
);

insert into locatie values 
(
'TIM',
'Bucuresti',
'Romania',
'Bd Timisoara',
89
);

insert into locatie values 
(
'ARG',
'Bucuresti',
'Romania',
'Valea Argesului',
1
);

insert into locatie values 
(
'IAL',
'Bucuresti',
'Romania',
'Valea Ialomitei',
13
);

insert into locatie values 
(
'GIUL',
'Bucuresti',
'Romania',
'Calea Giulesti',
20
);

insert into locatie values 
(
'ARAD',
'Bucuresti',
'Romania',
'Bd Arad',
21
);

--- inserturile pentru tabelul job

insert into job values (
'IT',
'Programator',
1220
);

insert into job values (
'ING',
'Inginer',
1000
);

insert into job values (
'ASIG',
'Asigurator',
1300
);

insert into job values (
'VANZ',
'Vanzator',
900
);

insert into job values (
'ARI',
'Arhitect',
2000
);

insert into job values (
'DEL',
'Delevey',
200
);

insert into job values(
'Add', 'Agent1', 100
);

insert into job values 
('ANTRE', 'Antrenor', null);

---- inserturile pentru tabelul om

insert into om values (
8,
'A',
'5000301410701');

insert into om values (
0,
'Andrei Pasareh',
'1720101410697'
);

insert into om values (
1,
'Giuli Dumitru',
'5000301410703'
);

insert into om values (
2,
'Sebastian Popescu',
'5000301413696'
);

insert into om values (
3,
'Alina Ion',
'6000604410528'
);

insert into om values (
4,
'Maria Dobrita',
'6000604415412'
);

insert into om values (
5,
'Alexandra Sandu',
'6010604415489'
);

insert into om
values (
7, 'Giuli Dumitru', '5010830262532'
);

insert into om
values (
6, 'Giuli ', '5020830262532'
);

--- inserturile in tabelul sala

insert into sala values (
'SAS',
'SAS GYM',
'ARG'
);

insert into sala values (
'WCSS',
'WORLD CLASS',
'IUL_MAN'
);

insert into sala values (
'BL',
'BE LIFE GYM',
'TIM'
);

insert into sala values (
'DY',
'DYNAMIC GYM',
'IAL'
);

insert into sala values (
'BF',
'BEST FITNESS GYM',
'GIUL'
);

insert into sala values (
'GEDO',
'GEDO GYM',
'ARAD'
);

--- inserturile in tabelul aparatura

insert into aparatura values (
1,
'HELCOMETRU',
'Marele dorsal'
);

insert into aparatura values (
2,
'PRESA',
'PICIOARELE'
);

insert into aparatura values (
3,
'BANCA REGLABILA',
'Pectoralii'
);

insert into aparatura values (
4,
'SCRIPETI',
'Muschii superiori'
);

insert into aparatura values (
5,
'Ganetere',
'Toate  grupele'
);

--- inserturile pentru Antrenor

insert into antrenor values (
0,
0,
5,
'SAS'
);

insert into antrenor values (
1,
1,
4,
'WCSS'
);

insert into antrenor values (
2,
2,
3,
'BL'
);

--- inserturile in tabelul sportiv

insert into sportiv values (
3, 
0,
3
);

insert into sportiv values (
4, 
1,
5
);

insert into sportiv values (
5, 
2,
3
);

--- adaugam date in tabelul antreneaza

insert into antreneaza values (
0, 0, sysdate
);

insert into antreneaza values (
1, 0, sysdate
);

insert into antreneaza values (
0, 1, sysdate
);

insert into antreneaza values (
1, 1, sysdate
);

insert into antreneaza values (
1, 2, sysdate
);

insert into antreneaza values (
2, 1, sysdate
);

insert into antreneaza values (
0, 1, sysdate + 20
);

insert into antreneaza values (
1, 0, sysdate + 19
);

insert into antreneaza values (
1, 0, sysdate + 20
);

insert into antreneaza values (
2, 0, sysdate + 20
);

--- Adaugam date in tabelul are

insert into are values (
'SAS', 1, 2
);

insert into are values (
'SAS', 2, 3
);

insert into are values (
'SAS', 5, 20
);

insert into are values (
'GEDO', 5, 1
);

insert into are values (
'GEDO', 2, 3
);

insert into are values (
'GEDO', 3, 2
);

insert into are values (
'WCSS', 5, 20
);

insert into are values (
'WCSS', 1, 1
);

insert into are values (
'WCSS', 2, 3
);

insert into are values (
'WCSS', 4, 21
);

--- adaugam valori in job

insert into lucreaza values (
0, 'IT', sysdate
);

insert into lucreaza values (
0, 'ASIG', sysdate
);

insert into lucreaza values (
1, 'ING', sysdate
);

insert into lucreaza values (
2, 'VANZ', sysdate
);

insert into lucreaza values (
3, 'ARI', sysdate
);

insert into lucreaza values (
4, 'DEL', sysdate
);

insert into lucreaza values (
4, 'IT', sysdate
);

insert into lucreaza values (
2, 'ARI', sysdate
);

insert into lucreaza values (
2, 'DEL', sysdate
);

insert into lucreaza values (
2, 'IT', sysdate
);

commit;

--- 
--- Baza mea de date este in fn3, de acum incep restul cerintelor
---

--- 6
set serveroutput on;

--- functia mea va returna numarul de antrenori ai unei sali de fitness, si daca sala nu exista returneaza 0
create or replace function NumarAntrenori (nume_sala sala.denumire%type) 
return number
is
    type tablou is table of Number; --- aici voi stoca ce id - urile antrenorilor
    antrenori tablou := tablou();
    res Number := 0;
begin
    select id_antrenor bulk collect into antrenori
    from antrenor a, sala s
    where lower(s.denumire) = lower(nume_sala) and s.id_sala = a.id_sala;
    res := antrenori.count;
    return res;
end NumarAntrenori;
/

begin 
dbms_output.put_line('Sala are ' || NumarAntrenori('SAS GYM') || ' antrenori.');
end;
/

--- 7

--- procedura mea imi va arata numele antrenorilor si apoi imi va arata numele fiecarui om pe care il antreneaza
create or replace procedure RaportAntrenori 
is
    type refcursor is ref cursor;
    cursor c is 
        select o.nume, 
            cursor (
                select distinct o1.nume
                from sportiv s, antreneaza an, om o1
                where s.id_sportiv = an.id_sportiv
                and s.id_om = o1.id_om
                and  a.id_antrenor = an.id_antrenor
            ) from 
         antrenor a, om o
        where  a.id_om = o.id_om
        and a.id_antrenor in (select distinct id_antrenor from antreneaza);
    nume om.nume%type;
    crs refcursor;
begin
    open c;
    loop
        fetch c into nume,crs;
        exit when c%notfound;
        dbms_output.put_line('Antrenorul '|| nume || ' antreneaza: ');
        loop 
            fetch crs into nume;
            exit when crs%notfound;
            dbms_output.put_line(' -'|| nume || ';');
        end loop;
    end loop;
    close c;
end RaportAntrenori;
/

begin 
    RaportAntrenori();
end;
/

--- 8
--- voi mai adauga un om pe nume giuli pentru a putea evidentia eroarea too_many_rows

create or replace procedure afiseazaJoburi  --- tabele folosite sunt job, om si lucreaza
(name om.nume%type) is
    type tablou is table of job.denumire%type index by PLS_INTEGER;
    joburi tablou;
    id om.id_om%type;
    i PLS_INTEGER;
    somer exception;
begin
    --- la comanda anterioara pot obtine erorile, fie no_data_found, fie _too_many_rows
    select id_om into id
    from om
    where om.nume = name;
    select denumire bulk collect into joburi
    from lucreaza l, job j, om o
    where j.id_job = l.id_job
    and o.id_om = l.id_om and 
    o.nume = name;
    --- vom afisa
    i := joburi.first;
    if joburi.count <> 0 then dbms_output.put_line(name|| ' lucreaza: ');
    else
        raise somer;
    end if;
    while i is not null loop
        dbms_output.put_line('  - '|| joburi(i)||';');
        i := joburi.next(i);
    end loop;
exception
    when somer then
            raise_application_error(-20006, 'Nu are job!');
    when no_data_found then
        raise_application_error(-20003, 'Nu avem angajat cu acest nume!');
    when too_many_rows then
        raise_application_error(-20004, 'Avem prea multi angajati cu acest nume');
    when others then
        raise_application_Error(-20005,'Alta eroare');
end afiseazaJoburi;
/

--- vom testa prima data cand merge

begin 
    afiseazaJoburi('Andrei Pasareh');
end;
/

--- vom testa pentru cazul no_data_found

begin 
    afiseazaJoburi('Andra Pasareh');
end;
/

--- vom testa pentru too_many_rows

begin 
    afiseazaJoburi('Giuli Dumitru');
end;
/

--- cazul cand omul este somer

begin 
    afiseazaJoburi('A');
end;
/

--- 9 

--- voi face o procedura ce mi va afisa toate salile unde ce au antrenori ce lucreaza si la jobul specificat de mine
--- tabele implicate job, lucreaza, om, antrenor, sala

create or replace procedure AfisareSali (name job.denumire%type) is
    type vector is varray(100) of sala.denumire%type;
    v vector := vector();
    id job.id_job%type;
    i Number;
    nu_sunt_sali exception;
begin 
    select id_job into id 
    from job
    where denumire = name;
    --- aici pot genera exceptia no_data_found
    select distinct s.denumire bulk collect into v
    from sala s, om o, antrenor a, lucreaza l, job j
    where l.id_job = j.id_job and 
    l.id_om = o.id_om and
    o.id_om = a.id_om and
    s.id_sala = a.id_sala and 
    j.denumire = name;
    
    if v.count = 0 then
        raise nu_sunt_sali;
    else 
        dbms_output.put_line('Avem la jobul '|| name|| ' angajati care sa antreneze la salile: ' );
    end if;
    
    i := v.first;
    while i is not null loop
        dbms_output.put_line('  - '|| v(i)||';');
        i := v.next(i);
    end loop;
    
exception
    when nu_sunt_sali then
        raise_application_error(-20004, 'Nu sunt sali unde angajatii jobului sa antreneze.');
    when no_data_found then
        raise_application_error(-20003, 'Nu exista jobul acesta');
    when others then
        raise_application_Error(-20005,'Alta eroare');
end AfisareSali;
/

--- cazul no_data_found
begin
    AfisareSali('IA');
end;
/

--- cazul functional
begin
    AfisareSali('Programator');
end;
/
--- cazul in care merge, dar nu exista sali
begin
    AfisareSali('Agent1');
end;
/


--- 10
create or replace trigger reparaAntrenori
after insert on antrenor
declare
    type vec is table of om.id_om%type index by PLS_INTEGER;
    g vec;
    i Number;
begin
    select id_om bulk collect into g
    from antrenor
    where id_om not in (
        select id_om from lucreaza where lucreaza.id_job = 'ANTRE'
    );
    dbms_output.put_line(g.count);
    if g.count <> 0 then
        
        i := g.first;
        while i is not null loop
            insert into lucreaza values (g(i), 'ANTRE',sysdate);
            i := g.next(i);
        end loop;
    end if;
exception
    when others then
        raise_application_error(-20005,'EROARE');
end reparaAntrenori;
/


--- vom testa 
select * from lucreaza;
insert into antrenor values(3,4,4,'SAS');
select * from antrenor;

--- 11

create or replace trigger StergeAntrenor
after update on lucreaza
for each row 
begin
    dbms_output.put_line('A mers cu succes!');
    if :new.id_job <> :old.id_job and :old.id_job = 'ANTRE' then
        delete from Antrenor
        where id_om = :old.id_om;
    end if;
exception
    when others then
        raise_application_error(-20004,'Eroare');
end StergeAntrenor;
/

update lucreaza 
set id_job = 'A'
where id_om = 3 and id_job = 'ANTRE';
select * from antrenor;

--- 12

--- voi face un trigger ce nu mi permite sa sterg tabele

create or replace trigger LDDtrigger
before drop
on database
declare 
    exceptie exception;
begin
    raise exceptie;
exception
    when others then 
        raise_application_error(-20005,'O eroare!');
end LDDtrigger;
/

drop table sala;
select  * from sala;

--- 13
--- voi pune toate functiile si procedurile intr - un pachet

create or replace package GIULI as
    
    procedure AfisareSali (name job.denumire%type);
    procedure afiseazaJoburi (name om.nume%type);
    procedure RaportAntrenori;
    function NumarAntrenori (nume_sala sala.denumire%type) return number;
 
end GIULI;
/

create or replace package body GIULI as

    procedure AfisareSali (name job.denumire%type) is
        type vector is varray(100) of sala.denumire%type;
        v vector := vector();
        id job.id_job%type;
        i Number;
        nu_sunt_sali exception;
    begin 
        select id_job into id 
        from job
        where denumire = name;
        --- aici pot genera exceptia no_data_found
        select distinct s.denumire bulk collect into v
        from sala s, om o, antrenor a, lucreaza l, job j
        where l.id_job = j.id_job and 
        l.id_om = o.id_om and
        o.id_om = a.id_om and
        s.id_sala = a.id_sala and 
        j.denumire = name;
        
        if v.count = 0 then
            raise nu_sunt_sali;
        else 
            dbms_output.put_line('Avem la jobul '|| name|| ' angajati care sa antreneze la salile: ' );
        end if;
        
        i := v.first;
        while i is not null loop
            dbms_output.put_line('  - '|| v(i)||';');
            i := v.next(i);
        end loop;
        
    exception
        when nu_sunt_sali then
            raise_application_error(-20004, 'Nu sunt sali unde angajatii jobului sa antreneze.');
        when no_data_found then
            raise_application_error(-20003, 'Nu exista jobul acesta');
        when others then
            raise_application_Error(-20005,'Alta eroare');
    end AfisareSali;
    
     procedure afiseazaJoburi (name om.nume%type) is
        type tablou is table of job.denumire%type index by PLS_INTEGER;
        joburi tablou;
        id om.id_om%type;
        i PLS_INTEGER;
        somer exception;
    begin
        select id_om into id
        from om
        where om.nume = name;
        select denumire bulk collect into joburi
        from lucreaza l, job j, om o
        where j.id_job = l.id_job
        and o.id_om = l.id_om and 
        o.nume = name;
        --- vom afisa
        i := joburi.first;
        if joburi.count <> 0 then dbms_output.put_line(name|| ' lucreaza: ');
        else
            raise somer;
        end if;
        while i is not null loop
            dbms_output.put_line('  - '|| joburi(i)||';');
            i := joburi.next(i);
        end loop;
    exception
        when somer then
                raise_application_error(-20006, 'Nu are job!');
        when no_data_found then
            raise_application_error(-20003, 'Nu avem angajat cu acest nume!');
        when too_many_rows then
            raise_application_error(-20004, 'Avem prea multi angajati cu acest nume');
        when others then
            raise_application_Error(-20005,'Alta eroare');
    end afiseazaJoburi;

    function NumarAntrenori (nume_sala sala.denumire%type) return number
    is
        type tablou is table of Number index by PLS_INTEGER; --- aici voi stoca ce id - urile antrenorilor
        antrenori tablou;
        res Number := 0;
    begin
        select id_antrenor bulk collect into antrenori
        from antrenor a, sala s
        where lower(s.denumire) = lower(nume_sala) and s.id_sala = a.id_sala;
        res := antrenori.count;
        return res;
    end NumarAntrenori;
   
   procedure RaportAntrenori is
        type refcursor is ref cursor;
        cursor c is 
            select o.nume, 
                cursor (
                    select distinct o1.nume
                    from sportiv s, antreneaza an, om o1
                    where s.id_sportiv = an.id_sportiv
                    and s.id_om = o1.id_om
                    and  a.id_antrenor = an.id_antrenor
                ) from 
             antrenor a, om o
            where  a.id_om = o.id_om
            and a.id_antrenor in (select distinct id_antrenor from antreneaza);
        nume om.nume%type;
        crs refcursor;
    begin
        open c;
        loop
            fetch c into nume,crs;
            exit when c%notfound;
            dbms_output.put_line('Antrenorul '|| nume || ' antreneaza: ');
            loop 
                fetch crs into nume;
                exit when crs%notfound;
                dbms_output.put_line(' -'|| nume || ';');
            end loop;
        end loop;
        close c;
    end RaportAntrenori;
    
end GIULI;
/

--- vom testa toate functiile din pachet

set serveroutput on;

begin 
    dbms_output.put_line('Sala are ' || giuli.NumarAntrenori('SAS GYM') || ' antrenori.');
end;
/

begin
    giuli.AfisareSali('Agent');
end;
/

begin
    giuli.AfisareSali('IA');
end;
/

begin
    giuli.AfisareSali('Programator');
end;
/

begin 
    giuli.afiseazaJoburi('Andrei Pasareh');
end;
/

begin 
    giuli.afiseazaJoburi('Andra Pasareh');
end;
/

begin 
    giuli.afiseazaJoburi('Giuli Dumitru');
end;
/

begin 
    giuli.afiseazaJoburi('A');
end;
/

begin 
    giuli.RaportAntrenori();
end;
/

--- 14

create or replace package pachetObiecte as --- in acest pachet voi face cateva tipuri de date pentru a modela mai usor datele in comenzile pl/sql

    type nume_oameni is varray(100) of om.nume%type;
    type antrenor_calificativ is record  (
        nume_antrenor om.nume%type,
        raiting antrenor.raiting%type
    );
    type sala_locatie is record (
        nume_sala sala.denumire%type,
        nume_oras locatie.oras%type,
        nume_tara locatie.tara%type,
        nume_strada locatie.strada%type,
        nr_strada locatie.nr%type
    );
    type antrenor_sala is record (
        sala sala_locatie,
        antrenor om.nume%type
    );
    type informatii_antrenori is table of antrenor_sala index by PLS_INTEGER;
    
end pachetObiecte;
/

--- aici voi testa datele mele

declare 
    s pachetObiecte.sala_locatie;
    aux pachetObiecte.antrenor_sala;
    antr pachetObiecte.informatii_antrenori;
    poz Number := 1;
begin
    for i in (select id_antrenor id from antrenor) loop
        select denumire, oras, tara, strada, nr into s
        from locatie l, sala s, antrenor a
        where s.id_locatie = l.id_locatie
        and a.id_antrenor = i.id and
        a.id_sala = s.id_sala; 
        
        aux.sala := s;
        select nume into aux.antrenor
        from antrenor a, om o
        where a.id_antrenor = i.id and o.id_om = a.id_om;
        antr(poz) := aux;
         poz := poz + 1;
    end loop;
    
    for i in 1..antr.count loop
        dbms_output.put_line(
            antr(i).antrenor || ' se antreneaza la ' || antr(i).sala.nume_sala 
        );
    end loop;
    
end;
/

declare 
    type tablou is table of pachetObiecte.sala_locatie;
    oameni pachetObiecte.nume_oameni := pachetobiecte.nume_oameni();
    a tablou;
    i Number;
begin 
    select denumire, oras, tara, strada, nr bulk collect into a
    from locatie l, sala s
    where s.id_locatie = l.id_locatie;
    i := a.first;
    while i  is not null loop
        dbms_output.put_line(
            'Sala '|| a(i).nume_sala || ' este in tara '|| a(i).nume_tara
            || ' in orasul ' || a(i).nume_oras || ' pe strada ' || a(i).nume_strada
            || ' nr ' || a(i).nr_strada || '.'
        );
        i := a.next(i);
    end loop;
    select nume bulk collect into oameni
    from om;
    i := oameni.first;
    dbms_output.put_line('Oamenii sunt: ');
    while i is not null loop
        dbms_output.put_line(' - '|| oameni(i));
        i := oameni.next(i);
    end loop;
end;
/

--- pachetul functioneaza bine