--
-- PostgreSQL database dump
--

\restrict O2zRXTWCkCx1POXcNbIpEmyw8kHS24iroNyRj4t7xtoahNmIgjdJjbEGecUyllm

-- Dumped from database version 15.18
-- Dumped by pg_dump version 17.10 (Debian 17.10-0+deb13u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.payroll_records DROP CONSTRAINT payroll_records_employee_id_fkey;
ALTER TABLE ONLY public.employment_history DROP CONSTRAINT employment_history_employee_id_fkey;
DROP INDEX public.idx_payroll_records_date;
DROP INDEX public.idx_employment_history_employee;
DROP INDEX public.idx_employees_status;
DROP INDEX public.idx_employees_department;
ALTER TABLE ONLY public.payroll_records DROP CONSTRAINT unique_employee_month_year;
ALTER TABLE ONLY public.payroll_records DROP CONSTRAINT payroll_records_pkey;
ALTER TABLE ONLY public.employment_history DROP CONSTRAINT employment_history_pkey;
ALTER TABLE ONLY public.employees DROP CONSTRAINT employees_pkey;
ALTER TABLE ONLY public.departments DROP CONSTRAINT departments_pkey;
ALTER TABLE ONLY public.departments DROP CONSTRAINT departments_name_key;
ALTER TABLE public.payroll_records ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.employment_history ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.employees ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.departments ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.payroll_records_id_seq;
DROP TABLE public.payroll_records;
DROP SEQUENCE public.employment_history_id_seq;
DROP TABLE public.employment_history;
DROP SEQUENCE public.employees_id_seq;
DROP TABLE public.employees;
DROP SEQUENCE public.departments_id_seq;
DROP TABLE public.departments;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: hr_user
--

CREATE TABLE public.departments (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.departments OWNER TO hr_user;

--
-- Name: departments_id_seq; Type: SEQUENCE; Schema: public; Owner: hr_user
--

CREATE SEQUENCE public.departments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.departments_id_seq OWNER TO hr_user;

--
-- Name: departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hr_user
--

ALTER SEQUENCE public.departments_id_seq OWNED BY public.departments.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: hr_user
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    full_name character varying(255) NOT NULL,
    join_date date NOT NULL,
    status character varying(20) DEFAULT 'Active'::character varying,
    role_title character varying(100) NOT NULL,
    department character varying(100) NOT NULL,
    base_salary numeric(12,2) DEFAULT 0.00 NOT NULL,
    employee_code text,
    employee_category text,
    first_name text,
    last_name text,
    work_shift text,
    company text,
    sponsor_name text,
    wps_sponsor text,
    lob text,
    grade_band text,
    date_of_birth date,
    reporting_manager_employee_code_name text,
    family_status_yes_no text,
    leave_policy text,
    last_rejoin_date date,
    annual_leave_balance_as_on_date numeric(12,2),
    annual_leave_balance numeric(12,2),
    lop_days_loss_of_pay_days numeric(12,2),
    business_unit text,
    working_company_name text,
    cost_centre text,
    nationality text,
    rp_id_number text,
    rp_id_profession text,
    qid_expiry_date date,
    visa_type text,
    hire_type text,
    confirmation_date date,
    esb_date date,
    gender text,
    marital_status text,
    office_mobile_no text,
    personal_mobile_no text,
    e_mail_id_work text,
    no_of_dependents numeric(12,2),
    blood_group text,
    building_villa text,
    street text,
    zone text,
    apartment text,
    building text,
    floor text,
    street_2 text,
    state text,
    country text,
    zip_code text,
    name text,
    relationship text,
    mobile_no_with_country_code text,
    travel_sector text,
    travel_cost numeric(12,2),
    no_of_tickets_employee_year numeric(12,2),
    ticket_balance numeric(12,2),
    no_of_tickets_family numeric(12,2),
    salary_pay_type_cash_bank_transfer_pay_card text,
    company_accommodation text,
    company_transportation text,
    overtime text,
    company_food text,
    company_fuel_card text,
    work_permit_no text,
    work_permit_issue_date date,
    work_permit_expiry_date date,
    office_file_no text,
    access_card_no text,
    bank_code text,
    iban_no text,
    account_no text,
    highest_education_qualification text,
    year_of_passing date,
    passport_no text,
    place_of_issue date,
    issue_date date,
    expiry_date date,
    licenses_type text,
    driving_licenses_no text,
    expiry_date_2 date,
    insurance_card_no text,
    issue_date_2 date,
    expiry_date_3 date,
    hra numeric(12,2),
    food_allowance numeric(12,2),
    mobile_allowance numeric(12,2),
    special_allowance numeric(12,2),
    over_time numeric(12,2),
    total numeric(12,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT employees_status_check CHECK (((status)::text = ANY ((ARRAY['Active'::character varying, 'Terminated'::character varying])::text[])))
);


ALTER TABLE public.employees OWNER TO hr_user;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: hr_user
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO hr_user;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hr_user
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: employment_history; Type: TABLE; Schema: public; Owner: hr_user
--

CREATE TABLE public.employment_history (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    effective_date date NOT NULL,
    change_type character varying(50) NOT NULL,
    previous_value character varying(255),
    new_value character varying(255),
    notes text
);


ALTER TABLE public.employment_history OWNER TO hr_user;

--
-- Name: employment_history_id_seq; Type: SEQUENCE; Schema: public; Owner: hr_user
--

CREATE SEQUENCE public.employment_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employment_history_id_seq OWNER TO hr_user;

--
-- Name: employment_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hr_user
--

ALTER SEQUENCE public.employment_history_id_seq OWNED BY public.employment_history.id;


--
-- Name: payroll_records; Type: TABLE; Schema: public; Owner: hr_user
--

CREATE TABLE public.payroll_records (
    id integer NOT NULL,
    employee_id integer NOT NULL,
    processed_month integer NOT NULL,
    processed_year integer NOT NULL,
    base_salary numeric(12,2) NOT NULL,
    allowances numeric(12,2) DEFAULT 0.00 NOT NULL,
    deductions numeric(12,2) DEFAULT 0.00 NOT NULL,
    net_pay numeric(12,2) NOT NULL,
    processed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT payroll_records_processed_month_check CHECK (((processed_month >= 1) AND (processed_month <= 12)))
);


ALTER TABLE public.payroll_records OWNER TO hr_user;

--
-- Name: payroll_records_id_seq; Type: SEQUENCE; Schema: public; Owner: hr_user
--

CREATE SEQUENCE public.payroll_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payroll_records_id_seq OWNER TO hr_user;

--
-- Name: payroll_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hr_user
--

ALTER SEQUENCE public.payroll_records_id_seq OWNED BY public.payroll_records.id;


--
-- Name: departments id; Type: DEFAULT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.departments ALTER COLUMN id SET DEFAULT nextval('public.departments_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: employment_history id; Type: DEFAULT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.employment_history ALTER COLUMN id SET DEFAULT nextval('public.employment_history_id_seq'::regclass);


--
-- Name: payroll_records id; Type: DEFAULT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.payroll_records ALTER COLUMN id SET DEFAULT nextval('public.payroll_records_id_seq'::regclass);


--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: hr_user
--

COPY public.departments (id, name, description, created_at) FROM stdin;
1	Human Resources	\N	2026-06-17 21:54:28.660525
2	Engineering	\N	2026-06-17 21:54:28.660525
3	Finance	\N	2026-06-17 21:54:28.660525
4	Sales	\N	2026-06-17 21:54:28.660525
5	IT	\N	2026-06-17 21:54:28.660525
6	Operations	\N	2026-06-17 21:54:28.660525
7	Administration	\N	2026-06-17 21:54:28.660525
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: hr_user
--

COPY public.employees (id, full_name, join_date, status, role_title, department, base_salary, employee_code, employee_category, first_name, last_name, work_shift, company, sponsor_name, wps_sponsor, lob, grade_band, date_of_birth, reporting_manager_employee_code_name, family_status_yes_no, leave_policy, last_rejoin_date, annual_leave_balance_as_on_date, annual_leave_balance, lop_days_loss_of_pay_days, business_unit, working_company_name, cost_centre, nationality, rp_id_number, rp_id_profession, qid_expiry_date, visa_type, hire_type, confirmation_date, esb_date, gender, marital_status, office_mobile_no, personal_mobile_no, e_mail_id_work, no_of_dependents, blood_group, building_villa, street, zone, apartment, building, floor, street_2, state, country, zip_code, name, relationship, mobile_no_with_country_code, travel_sector, travel_cost, no_of_tickets_employee_year, ticket_balance, no_of_tickets_family, salary_pay_type_cash_bank_transfer_pay_card, company_accommodation, company_transportation, overtime, company_food, company_fuel_card, work_permit_no, work_permit_issue_date, work_permit_expiry_date, office_file_no, access_card_no, bank_code, iban_no, account_no, highest_education_qualification, year_of_passing, passport_no, place_of_issue, issue_date, expiry_date, licenses_type, driving_licenses_no, expiry_date_2, insurance_card_no, issue_date_2, expiry_date_3, hra, food_allowance, mobile_allowance, special_allowance, over_time, total, created_at, updated_at) FROM stdin;
1	Jassim Al-Thani	2024-01-15	Active	Senior HR Manager	Human Resources	18000.00	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-17 21:54:28.664546	2026-06-17 21:54:28.664546
2	Fatima Al-Kuwari	2024-03-01	Active	Senior Software Engineer	Engineering	15500.00	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-17 21:54:28.664546	2026-06-17 21:54:28.664546
3	Mohammed Al-Sulaiti	2023-06-10	Active	Finance Director	Finance	25000.00	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-17 21:54:28.664546	2026-06-17 21:54:28.664546
4	Aisha Al-Marri	2025-02-15	Terminated	Sales Representative	Sales	9000.00	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-06-17 21:54:28.664546	2026-06-17 21:54:28.664546
\.


--
-- Data for Name: employment_history; Type: TABLE DATA; Schema: public; Owner: hr_user
--

COPY public.employment_history (id, employee_id, effective_date, change_type, previous_value, new_value, notes) FROM stdin;
1	1	2024-01-15	Onboarding	\N	16000.00	Onboarded as HR Specialist with starting salary of 16,000 QAR
2	2	2024-03-01	Onboarding	\N	13000.00	Onboarded as Software Engineer with starting salary of 13,000 QAR
3	3	2023-06-10	Onboarding	\N	25000.00	Onboarded as Finance Director with starting salary of 25,000 QAR
4	4	2025-02-15	Onboarding	\N	9000.00	Onboarded as Sales Representative with starting salary of 9,000 QAR
\.


--
-- Data for Name: payroll_records; Type: TABLE DATA; Schema: public; Owner: hr_user
--

COPY public.payroll_records (id, employee_id, processed_month, processed_year, base_salary, allowances, deductions, net_pay, processed_at) FROM stdin;
1	1	5	2026	18000.00	1500.00	500.00	19000.00	2026-06-17 21:54:28.676329
2	2	5	2026	15500.00	1000.00	300.00	16200.00	2026-06-17 21:54:28.676329
3	3	5	2026	25000.00	2000.00	1000.00	26000.00	2026-06-17 21:54:28.676329
4	3	6	2026	25000.00	0.00	0.00	25000.00	2026-06-17 21:55:44.569957
\.


--
-- Name: departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hr_user
--

SELECT pg_catalog.setval('public.departments_id_seq', 112, true);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hr_user
--

SELECT pg_catalog.setval('public.employees_id_seq', 4, true);


--
-- Name: employment_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hr_user
--

SELECT pg_catalog.setval('public.employment_history_id_seq', 4, true);


--
-- Name: payroll_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hr_user
--

SELECT pg_catalog.setval('public.payroll_records_id_seq', 4, true);


--
-- Name: departments departments_name_key; Type: CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_name_key UNIQUE (name);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: employment_history employment_history_pkey; Type: CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.employment_history
    ADD CONSTRAINT employment_history_pkey PRIMARY KEY (id);


--
-- Name: payroll_records payroll_records_pkey; Type: CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.payroll_records
    ADD CONSTRAINT payroll_records_pkey PRIMARY KEY (id);


--
-- Name: payroll_records unique_employee_month_year; Type: CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.payroll_records
    ADD CONSTRAINT unique_employee_month_year UNIQUE (employee_id, processed_month, processed_year);


--
-- Name: idx_employees_department; Type: INDEX; Schema: public; Owner: hr_user
--

CREATE INDEX idx_employees_department ON public.employees USING btree (department);


--
-- Name: idx_employees_status; Type: INDEX; Schema: public; Owner: hr_user
--

CREATE INDEX idx_employees_status ON public.employees USING btree (status);


--
-- Name: idx_employment_history_employee; Type: INDEX; Schema: public; Owner: hr_user
--

CREATE INDEX idx_employment_history_employee ON public.employment_history USING btree (employee_id);


--
-- Name: idx_payroll_records_date; Type: INDEX; Schema: public; Owner: hr_user
--

CREATE INDEX idx_payroll_records_date ON public.payroll_records USING btree (processed_year, processed_month);


--
-- Name: employment_history employment_history_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.employment_history
    ADD CONSTRAINT employment_history_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- Name: payroll_records payroll_records_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hr_user
--

ALTER TABLE ONLY public.payroll_records
    ADD CONSTRAINT payroll_records_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict O2zRXTWCkCx1POXcNbIpEmyw8kHS24iroNyRj4t7xtoahNmIgjdJjbEGecUyllm

