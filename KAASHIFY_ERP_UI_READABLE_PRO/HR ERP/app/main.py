import streamlit as st
import os
import datetime
from psycopg2 import pool
from contextlib import contextmanager


def get_config_value(name, default=None):
    """Read config from environment variables first, then Streamlit secrets."""
    value = os.getenv(name)
    if value not in (None, ""):
        return value
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default

# 0. Database schema bootstrap
# PostgreSQL treats CURRENT_ROLE as a reserved/special keyword. The employee role
# column is therefore named role_title to avoid SQL syntax errors.
def ensure_database_schema():
    """Create/upgrade required tables even when an old Docker volume already exists."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employees (
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
            """)
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS employee_code TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS employee_category TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS first_name TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS last_name TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS work_shift TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS company TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS sponsor_name TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS wps_sponsor TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS lob TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS grade_band TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS date_of_birth DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS reporting_manager_employee_code_name TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS family_status_yes_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS leave_policy TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS last_rejoin_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS annual_leave_balance_as_on_date NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS annual_leave_balance NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS lop_days_loss_of_pay_days NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS business_unit TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS working_company_name TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS cost_centre TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS nationality TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS rp_id_number TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS rp_id_profession TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS qid_expiry_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS visa_type TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS hire_type TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS confirmation_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS esb_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS gender TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS marital_status TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS office_mobile_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS personal_mobile_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS e_mail_id_work TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS no_of_dependents NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS blood_group TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS building_villa TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS street TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS zone TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS apartment TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS building TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS floor TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS street_2 TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS state TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS country TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS zip_code TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS name TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS relationship TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS mobile_no_with_country_code TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS travel_sector TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS travel_cost NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS no_of_tickets_employee_year NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS ticket_balance NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS no_of_tickets_family NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS salary_pay_type_cash_bank_transfer_pay_card TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS company_accommodation TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS company_transportation TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS overtime TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS company_food TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS company_fuel_card TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS work_permit_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS work_permit_issue_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS work_permit_expiry_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS office_file_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS access_card_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS bank_code TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS iban_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS account_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS highest_education_qualification TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS year_of_passing DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS passport_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS place_of_issue DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS issue_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS expiry_date DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS licenses_type TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS driving_licenses_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS expiry_date_2 DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS insurance_card_no TEXT;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS issue_date_2 DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS expiry_date_3 DATE;")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS hra NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS food_allowance NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS mobile_allowance NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS special_allowance NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS over_time NUMERIC(12,2);")
            cur.execute("ALTER TABLE employees ADD COLUMN IF NOT EXISTS total NUMERIC(12,2);")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employment_history (
                    id SERIAL PRIMARY KEY,
                    employee_id INT NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
                    effective_date DATE NOT NULL,
                    change_type VARCHAR(50) NOT NULL,
                    previous_value VARCHAR(255),
                    new_value VARCHAR(255),
                    notes TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS payroll_records (
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
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_employees_status ON employees(status);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_employment_history_employee ON employment_history(employee_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_payroll_records_date ON payroll_records(processed_year, processed_month);")
            for dept in ['Human Resources','Engineering','Finance','Sales','IT','Operations','Administration']:
                cur.execute("INSERT INTO departments (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (dept,))
# 1. Establish a cached database connection pool
@st.cache_resource
def get_connection_pool():
    return pool.ThreadedConnectionPool(
        1, 15,
        host=get_config_value("DB_HOST", "db"),
        database=get_config_value("DB_NAME", "hr_erp"),
        user=get_config_value("DB_USER", "hr_user"),
        password=get_config_value("DB_PASSWORD", "hr_password_secure_123"),
        port=get_config_value("DB_PORT", "5432"),
        sslmode=get_config_value("DB_SSLMODE", "prefer")
    )

# 2. Connection manager context manager to safely acquire/release connections
@contextmanager
def get_db_connection():
    pool_obj = get_connection_pool()
    conn = pool_obj.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        pool_obj.putconn(conn)

# Ensure the database exists even when an old Docker volume is reused.
try:
    ensure_database_schema()
except Exception as bootstrap_error:
    # Displayed on pages where Streamlit is available; normal during DB startup race.
    pass

def run_main_page():
    # Ensure schema before dashboard queries
    try:
        ensure_database_schema()
    except Exception as e:
        st.warning(f"Database is starting or not ready yet: {e}")

    # Inject Custom Enterprise CSS
    from ui_theme import render_hero, apply_kaashify_theme
    apply_kaashify_theme()
    st.markdown("""
    <style>
        /* Base styles */
        .main {
            background-color: #FFFFFF;
        }
        
        /* Banner Styling */
        .banner-container {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 35px;
            border-radius: 12px;
            margin-bottom: 30px;
            color: #FFFFFF;
            box-shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.1);
        }
        .banner-title {
            margin: 0;
            font-size: 2.2rem;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .banner-subtitle {
            margin: 8px 0 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
            font-weight: 400;
        }
        
        /* Premium Card styling for st.metric */
        div[data-testid="metric-container"] {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 20px 25px;
            border-radius: 10px;
            box-shadow: 0 4px 10px -1px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px -1px rgba(0, 0, 0, 0.05);
            border-color: #CBD5E1;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: 700;
            color: #1E3A8A !important;
            font-size: 2.2rem !important;
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: 500;
            color: #475569 !important;
            font-size: 0.95rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Grid section header */
        .section-header {
            color: #1E293B;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 1.4rem;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 15px;
            border-left: 5px solid #1E3A8A;
            padding-left: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    apply_kaashify_theme()

    # 1. Header Banner
    render_hero(
        title="Kaashify ERP",
        subtitle="A polished local HR ERP workspace for employee onboarding, department management, payroll, documents and secure database operations.",
        kicker="Secure HR Operations"
    )

    # Fetch metrics from PostgreSQL database
    active_count = 0
    terminated_count = 0
    latest_payroll_label = "No Payroll History"
    latest_payroll_value = "0.00 QAR"

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Active Headcount
                cur.execute("SELECT COUNT(*) FROM employees WHERE status = 'Active'")
                active_count = cur.fetchone()[0]

                # Terminated Headcount
                cur.execute("SELECT COUNT(*) FROM employees WHERE status = 'Terminated'")
                terminated_count = cur.fetchone()[0]

                # Latest Processed Monthly Payroll Liabilities
                cur.execute("""
                    SELECT processed_month, processed_year, SUM(net_pay) 
                    FROM payroll_records 
                    GROUP BY processed_month, processed_year 
                    ORDER BY processed_year DESC, processed_month DESC 
                    LIMIT 1
                """)
                payroll_row = cur.fetchone()
                if payroll_row:
                    month_num = int(payroll_row[0])
                    year_num = int(payroll_row[1])
                    total_net = float(payroll_row[2])
                    
                    month_name = datetime.date(1900, month_num, 1).strftime('%B')
                    latest_payroll_label = f"Payroll Liabilities ({month_name} {year_num})"
                    latest_payroll_value = f"{total_net:,.2f} QAR"
    except Exception as e:
        st.error(f"Failed to load dashboard metrics from database: {str(e)}")

    # 2. KPI Metrics Columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Active Headcount", value=str(active_count))
    with col2:
        st.metric(label="Terminated Employees", value=str(terminated_count))
    with col3:
        st.metric(label=latest_payroll_label, value=latest_payroll_value)

    st.markdown("<div class='section-header'>Kaashify Operations Center</div>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("""
        ### System Overview
        Kaashify ERP is running in an **isolated Docker container ecosystem** hosted on your local workstation. 
        It is configured to adhere strictly to air-gapped security guardrails:
        
        *   **Zero External Connectivity**: No connections are made to public cloud networks.
        *   **Local Loopback Only**: The PostgreSQL database and Streamlit frontend are bound strictly to `127.0.0.1` interfaces, blocking external network access.
        *   **Local File Storage**: Uploaded documents and database backups are written directly to your workspace.
        *   **Currency Conformity**: All base rates, allowances, deductions, and financial statistics are calculated and reported in **Qatari Riyal (QAR)**.
        """)
    with col_right:
        st.info("""
        **Quick Navigation:**
        *   Use the sidebar to navigate to **Core HR** to manage employee profiles and onboarding.
        *   Use **Payroll** to process monthly compensation and export high-quality corporate PDF payslips.
        *   Use **Backups** to run local database archives and restore the system state.
        """)

if __name__ == '__main__':
    st.set_page_config(
        layout="wide",
        page_title="Kaashify ERP",
        page_icon="ðŸ¢"
    )
    run_main_page()




