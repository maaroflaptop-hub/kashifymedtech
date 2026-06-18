-- Database Initialization Schema
DROP TABLE IF EXISTS payroll_records CASCADE;
DROP TABLE IF EXISTS employment_history CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    join_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Terminated')),
    role_title VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    base_salary NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    employee_code TEXT,
    employee_category TEXT,
    first_name TEXT,
    last_name TEXT,
    work_shift TEXT,
    company TEXT,
    sponsor_name TEXT,
    wps_sponsor TEXT,
    lob TEXT,
    grade_band TEXT,
    date_of_birth DATE,
    reporting_manager_employee_code_name TEXT,
    family_status_yes_no TEXT,
    leave_policy TEXT,
    last_rejoin_date DATE,
    annual_leave_balance_as_on_date NUMERIC(12,2),
    annual_leave_balance NUMERIC(12,2),
    lop_days_loss_of_pay_days NUMERIC(12,2),
    business_unit TEXT,
    working_company_name TEXT,
    cost_centre TEXT,
    nationality TEXT,
    rp_id_number TEXT,
    rp_id_profession TEXT,
    qid_expiry_date DATE,
    visa_type TEXT,
    hire_type TEXT,
    confirmation_date DATE,
    esb_date DATE,
    gender TEXT,
    marital_status TEXT,
    office_mobile_no TEXT,
    personal_mobile_no TEXT,
    e_mail_id_work TEXT,
    no_of_dependents NUMERIC(12,2),
    blood_group TEXT,
    building_villa TEXT,
    street TEXT,
    zone TEXT,
    apartment TEXT,
    building TEXT,
    floor TEXT,
    street_2 TEXT,
    state TEXT,
    country TEXT,
    zip_code TEXT,
    name TEXT,
    relationship TEXT,
    mobile_no_with_country_code TEXT,
    travel_sector TEXT,
    travel_cost NUMERIC(12,2),
    no_of_tickets_employee_year NUMERIC(12,2),
    ticket_balance NUMERIC(12,2),
    no_of_tickets_family NUMERIC(12,2),
    salary_pay_type_cash_bank_transfer_pay_card TEXT,
    company_accommodation TEXT,
    company_transportation TEXT,
    overtime TEXT,
    company_food TEXT,
    company_fuel_card TEXT,
    work_permit_no TEXT,
    work_permit_issue_date DATE,
    work_permit_expiry_date DATE,
    office_file_no TEXT,
    access_card_no TEXT,
    bank_code TEXT,
    iban_no TEXT,
    account_no TEXT,
    highest_education_qualification TEXT,
    year_of_passing DATE,
    passport_no TEXT,
    place_of_issue DATE,
    issue_date DATE,
    expiry_date DATE,
    licenses_type TEXT,
    driving_licenses_no TEXT,
    expiry_date_2 DATE,
    insurance_card_no TEXT,
    issue_date_2 DATE,
    expiry_date_3 DATE,
    hra NUMERIC(12,2),
    food_allowance NUMERIC(12,2),
    mobile_allowance NUMERIC(12,2),
    special_allowance NUMERIC(12,2),
    over_time NUMERIC(12,2),
    total NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employment_history (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    effective_date DATE NOT NULL,
    change_type VARCHAR(50) NOT NULL,
    previous_value VARCHAR(255),
    new_value VARCHAR(255),
    notes TEXT
);

CREATE TABLE payroll_records (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    processed_month INT NOT NULL CHECK (processed_month BETWEEN 1 AND 12),
    processed_year INT NOT NULL,
    base_salary NUMERIC(12, 2) NOT NULL,
    allowances NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    deductions NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    net_pay NUMERIC(12, 2) NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_employee_month_year UNIQUE (employee_id, processed_month, processed_year)
);

CREATE INDEX idx_employees_status ON employees(status);
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employment_history_employee ON employment_history(employee_id);
CREATE INDEX idx_payroll_records_date ON payroll_records(processed_year, processed_month);

INSERT INTO departments (name) VALUES
('Human Resources'),('Engineering'),('Finance'),('Sales'),('IT'),('Operations'),('Administration')
ON CONFLICT (name) DO NOTHING;

INSERT INTO employees (id, full_name, join_date, status, role_title, department, base_salary) VALUES
(1, 'Jassim Al-Thani', '2024-01-15', 'Active', 'Senior HR Manager', 'Human Resources', 18000.00),
(2, 'Fatima Al-Kuwari', '2024-03-01', 'Active', 'Senior Software Engineer', 'Engineering', 15500.00),
(3, 'Mohammed Al-Sulaiti', '2023-06-10', 'Active', 'Finance Director', 'Finance', 25000.00),
(4, 'Aisha Al-Marri', '2025-02-15', 'Terminated', 'Sales Representative', 'Sales', 9000.00);
SELECT setval('employees_id_seq', (SELECT MAX(id) FROM employees));

INSERT INTO employment_history (employee_id, effective_date, change_type, previous_value, new_value, notes) VALUES
(1, '2024-01-15', 'Onboarding', NULL, '16000.00', 'Onboarded as HR Specialist with starting salary of 16,000 QAR'),
(2, '2024-03-01', 'Onboarding', NULL, '13000.00', 'Onboarded as Software Engineer with starting salary of 13,000 QAR'),
(3, '2023-06-10', 'Onboarding', NULL, '25000.00', 'Onboarded as Finance Director with starting salary of 25,000 QAR'),
(4, '2025-02-15', 'Onboarding', NULL, '9000.00', 'Onboarded as Sales Representative with starting salary of 9,000 QAR');

INSERT INTO payroll_records (employee_id, processed_month, processed_year, base_salary, allowances, deductions, net_pay) VALUES
(1, 5, 2026, 18000.00, 1500.00, 500.00, 19000.00),
(2, 5, 2026, 15500.00, 1000.00, 300.00, 16200.00),
(3, 5, 2026, 25000.00, 2000.00, 1000.00, 26000.00);
