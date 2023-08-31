CREATE TABLE public."user" (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar(200) NOT NULL,
	email varchar(200) NOT NULL,
	"password" varchar(500) NOT NULL,
	created_date timestamp NOT NULL,
	is_super_admin bool NULL DEFAULT false,
	expiry_date timestamp NULL,
	modified_date timestamp NULL,
	status int4 NULL
);

ALTER TABLE public."user" ADD created_by integer NULL;
ALTER TABLE public."user" ADD modified_by integer NULL;