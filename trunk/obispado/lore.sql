BEGIN;CREATE TABLE "aportantes_aportante" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(40) NOT NULL,
    "ruc" varchar(11) NOT NULL
)
;
CREATE TABLE "ingresos_venta" (
    "id" serial NOT NULL PRIMARY KEY,
    "fecha" timestamp with time zone NOT NULL,
    "aportante_id" integer NOT NULL REFERENCES "aportantes_aportante" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "ingresos_ventadetalle" (
    "id" serial NOT NULL PRIMARY KEY,
    "venta_id" integer NOT NULL REFERENCES "ingresos_venta" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cuenta_id" integer NOT NULL REFERENCES "plan_de_cuentas_cuentanivel3" ("id") DEFERRABLE INITIALLY DEFERRED,
    "gravadas5" double precision,
    "gravadas10" double precision,
    "iva5" double precision,
    "iva10" double precision,
    "exenta" double precision
)
;
CREATE TABLE "egresos_compra" (
    "id" serial NOT NULL PRIMARY KEY,
    "fecha" timestamp with time zone NOT NULL,
    "Proveedor_id" integer NOT NULL REFERENCES "proveedores_proveedor" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "egresos_compradetalle" (
    "id" serial NOT NULL PRIMARY KEY,
    "compra_id" integer NOT NULL REFERENCES "egresos_compra" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cuenta_id" integer NOT NULL REFERENCES "plan_de_cuentas_cuentanivel3" ("id") DEFERRABLE INITIALLY DEFERRED,
    "gravadas5" double precision,
    "gravadas10" double precision,
    "iva5" double precision,
    "iva10" double precision,
    "exenta" double precision
)
;
CREATE TABLE "plan_de_cuentas_tipocuenta" (
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
;
CREATE TABLE "proveedores_proveedor" (
    "id" serial NOT NULL PRIMARY KEY,
    "nombre" varchar(40) NOT NULL,
    "ruc" varchar(11) NOT NULL
)
;COMMIT;
