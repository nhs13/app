

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;



CREATE DATABASE app_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C.UTF-8';


\connect app_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;



CREATE SCHEMA app;


SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE app.inventory (
    product_id bigint NOT NULL,
    quantity bigint DEFAULT 0,
    cost_per_unti bigint DEFAULT 0
);




CREATE TABLE app.products (
    id bigint NOT NULL,
    name character varying NOT NULL,
    type character varying,
    classification character varying,
    details json
);



CREATE SEQUENCE app.products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




ALTER SEQUENCE app.products_id_seq OWNED BY app.products.id;


ALTER TABLE ONLY app.products ALTER COLUMN id SET DEFAULT nextval('app.products_id_seq'::regclass);




INSERT INTO app.products VALUES (5, 'test_2', 'new type', 'new class', NULL);
INSERT INTO app.products VALUES (9, 'test_2srts', 'new type', 'new class', '{"Adding": "new details"}');




SELECT pg_catalog.setval('app.products_id_seq', 13, true);


ALTER TABLE ONLY app.products
    ADD CONSTRAINT products_pk PRIMARY KEY (id);




ALTER TABLE ONLY app.products
    ADD CONSTRAINT products_un UNIQUE (name);



