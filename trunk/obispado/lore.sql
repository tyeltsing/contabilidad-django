BEGIN;CREATE TABLE "plan_de_cuentas_tipocuenta" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(40) NOT NULL,
    "tipo_de_saldo" varchar(1) NOT NULL
)
;
CREATE TABLE "plan_de_cuentas_cuentanivel1" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(40) NOT NULL,
    "tipo_id" integer NOT NULL REFERENCES "plan_de_cuentas_tipocuenta" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "plan_de_cuentas_cuentanivel2" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(40) NOT NULL,
    "tipo_id" integer NOT NULL REFERENCES "plan_de_cuentas_cuentanivel1" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "plan_de_cuentas_cuentanivel3" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(40) NOT NULL,
    "tipo_id" integer NOT NULL REFERENCES "plan_de_cuentas_cuentanivel2" ("id") DEFERRABLE INITIALLY DEFERRED
)
;COMMIT;
