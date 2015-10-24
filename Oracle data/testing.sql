
insert into flights values ('AC014','YEG','LAX',to_date('01:13', 'hh24:mi'),180);
insert into sch_flights values ('AC014',to_date('22-Dec-2015','DD-Mon-YYYY'),to_date('01:15', 'hh24:mi'),to_date('04:15','hh24:mi'));
insert into flight_fares values ('AC004','Q',10,500,0);
insert into flight_fares values ('AC014','J',10,2000,2);
insert into flight_fares values ('AC014','Y',20,700,0);
insert into flight_fares values ('AC014','Q',5,500,0);
insert into flight_fares values ('AC014','F',20,100,0);

insert into flights values ('AC027','LAX','YEG',to_date('05:15', 'hh24:mi'),180);
insert into sch_flights values ('AC027',to_date('23-Oct-2015','DD-Mon-YYYY'),to_date('05:15', 'hh24:mi'),to_date('08:15','hh24:mi'));
insert into flight_fares values ('AC027','J',10,1500,2);
insert into flight_fares values ('AC027','F',10,200,0);
