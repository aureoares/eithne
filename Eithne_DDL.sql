drop database if exists eithne;

create database eithne
  default character set = 'utf8'
  default collate = 'utf8_spanish_ci';

grant all privileges on eithne.* to admin@'%' identified by 'admin' with grant option;
grant all privileges on eithne.* to admin@'localhost' identified by 'admin' with grant option;

use eithne;

drop table if exists NETWORKS;
drop table if exists COMPUTERS;
drop table if exists DEVICES;
drop table if exists PRO_TYPES;
drop table if exists PROPERTIES;
drop table if exists MEMBERS;

create table NETWORKS
(
  IDNet 		integer not null auto_increment,
  Name 			varchar(30) not null,
  Description 	varchar(60) null,
  IP 			char(15) not null,
  Netmask 		char(15) not null,
  Parent 		integer null,
  constraint pkNetworks primary key (IDNet)
);

alter table NETWORKS 
  add constraint fkNetworks_Networks
  foreign key (Parent) references NETWORKS(IDNet)
  on delete no action
  on update cascade;

create table COMPUTERS
(
  IDCom 		integer not null auto_increment,
  Name 			varchar(30) null,
  constraint pkComputers primary key (IDCom)
);

create table DEVICES
(
  IDDev 		integer not null auto_increment,
  Parent 		integer null,
  Computer 		integer not null,
  constraint pkDevices primary key (IDDev),
  constraint fkDevices_Computers foreign key (Computer) 
  				references DEVICES(IDDev)
  				on delete no action
  				on update cascade
);

alter table DEVICES 
  add constraint fkDevices_Devices
  foreign key (Parent) references DEVICES(IDDev)
  on delete no action
  on update cascade;

create table PRO_TYPES
(
  IDTyp 		integer not null auto_increment,
  Type 			varchar(120) not null,
  constraint pkPro_Types primary key (IDTyp)
);

create table PROPERTIES
(
  IDPro 		integer not null auto_increment,
  ProKey 		integer not null,
  ProValue 		text null, -- Debería ser varchar(120)
  Device 		integer not null,
  constraint pkProperties primary key (IDPro),
  constraint fkProperties_Pro_Types foreign key (ProKey) 
  				references PRO_TYPES(IDTyp)
  				on delete no action
  				on update cascade,
  constraint fkProperties_Devices foreign key (Device) 
  				references DEVICES(IDDev)
  				on delete no action
  				on update cascade
);

create table MEMBERS
(
  IDMem 		integer not null auto_increment,
  Network 		integer not null,
  Computer 		integer not null,
  constraint pkMembers primary key (IDMem),
  constraint fkMembers_Networks foreign key (Network) 
  				references NETWORKS(IDNet)
  				on delete no action
  				on update cascade,
  constraint fkMembers_Computers foreign key (Computer) 
  				references COMPUTERS(IDCom)
  				on delete no action
  				on update cascade
);
