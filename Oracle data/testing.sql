/*
	Data Prepared by Connor Resler, resler@ualberta.ca, published on October 6, 2015
*/

insert into airports values ('YEG','Edmonton International Airport','Edmonton', 'Canada',-7);
insert into airports values ('YYZ','Pearson International Airport','Toronto', 'Canada',-5);
insert into airports values ('YUL','Trudeau International Airport','Montreal', 'Canada',-5);
insert into airports values ('YVR','Vancouver Airport','Vancouver', 'Canada',-8);
insert into airports values ('LAX','LA Airport','Los Angeles', 'US',-8);
insert into airports values ('MOS','Tatooine Airport','Mos Eisley', 'Tatooine',-8);
insert into airports values ('HND','Haneda Airport','Tokyo', 'Japan',+9);
insert into airports values ('HOB','Hobbiton Airport','Hobbiton', 'Shire',+9);

insert into flights values ('AC014','YEG','LAX',to_date('01:13', 'hh24:mi'),180);



insert into sch_flights values ('AC014',to_date('22-Dec-2015','DD-Mon-YYYY'),to_date('01:15', 'hh24:mi'),to_date('04:15','hh24:mi'));



insert into fares values ('J', 'Business class');
insert into fares values ('Y', 'Economy Lat');
insert into fares values ('Q', 'Flex');
insert into fares values ('F', 'Tango');


insert into flight_fares values ('AC014','J',10,2000,2);
insert into flight_fares values ('AC014','Y',20,700,0);
insert into flight_fares values ('AC014','Q',5,500,0);
insert into flight_fares values ('AC014','F',20,100,0);


insert into passengers values ('davood@ggg.com','Davood Rafiei','Canada');
insert into passengers values ('david@ggg.com','David Raft','Canada');
insert into passengers values ('gandalf@wizard.com','Gandalf Grey','Canada');
insert into passengers values ('ralph@ggg.com','Ralph Rafiei','Canada');
insert into passengers values ('uematsu@ff.com','Nobuo Uematsu','Japan');
insert into passengers values ('bill@ggg.com','Bill Smith','US');
insert into passengers values ('jack@ggg.com','Jack Daniel','Canada');
insert into passengers values ('greg@ggg.com','Greg Davis','Canada');
insert into passengers values ('thorin@ggg.com','Thorin Oakenshield','Canada');
insert into passengers values ('elrond@ggg.com','Elrond Smith','Canada');
insert into passengers values ('john@ggg.com','John Smith','US');
insert into passengers values ('man@ggg.com','Man Smith','Canada');
insert into passengers values ('dude@ggg.com','Dude Smith','Canada');
insert into passengers values ('person@ggg.com','Person Smith','Japan');

insert into tickets values (111,'Davood Rafiei','davood@ggg.com',700);
insert into tickets values (001,'Davood Rafiei','davood@ggg.com',200);
insert into tickets values (002,'Gandalf Grey','gandalf@wizard.com',1500);
insert into tickets values (003,'Nobuo Uematsu','uematsu@ff.com',800);
insert into tickets values (004,'Dude Smith','dude@ggg.com',700);
insert into tickets values (005,'Man Smith','man@ggg.com',200);
insert into tickets values (006,'Gandalf Grey','gandalf@wizard.com',700);
insert into tickets values (007,'Thorin Oakenshield','thorin@ggg.com',2000);

insert into bookings values (111,'AC154','Y',to_date('22-Dec-2015','DD-Mon-YYYY'),'20B');
insert into bookings values (001,'AC027','F',to_date('23-Oct-2015','DD-Mon-YYYY'),'10B');
insert into bookings values (002,'AC027','J',to_date('23-Oct-2015','DD-Mon-YYYY'),'10A');
insert into bookings values (003,'AC028','Q',to_date('23-Oct-2015','DD-Mon-YYYY'),'1A');
insert into bookings values (004,'AC028','Y',to_date('23-Oct-2015','DD-Mon-YYYY'),'2A');
insert into bookings values (005,'AC013','F',to_date('22-Dec-2015','DD-Mon-YYYY'),'20A');
insert into bookings values (006,'AC020','Y',to_date('22-Dec-2015','DD-Mon-YYYY'),'20B');
insert into bookings values (007,'AC014','J',to_date('22-Dec-2015','DD-Mon-YYYY'),'10B');

insert into users values('eorodrig@ualberta.ca','ABC1', to_date('2015/08/15 8:30:25', 'YYYY/MM/DD HH24:MI:SS'));
insert into users values('abbasi1@ualberta.ca','ABC1', to_date('2015/07/30 18:30:25', 'YYYY/MM/DD HH24:MI:SS'));
insert into users values('thorin@ggg.com','ABC1', to_date('2015/08/12 20:30:25', 'YYYY/MM/DD HH24:MI:SS'));
insert into users values('davood@ggg.com','ABC1', to_date('2015/08/12 20:30:25', 'YYYY/MM/DD HH24:MI:SS'));

insert into airline_agents values('thorin@ggg.com','Thorin Oakenshield');
insert into airline_agents values('davood@ggg.com','Davood Rafiei');
