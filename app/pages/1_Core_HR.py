import streamlit as st
import os
import pandas as pd
import datetime
import re
import io
from xml.sax.saxutils import escape
from psycopg2 import sql
from main import get_db_connection, ensure_database_schema
from ui_theme import render_page_header
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(layout="wide", page_title="Core HR - Kaashify ERP", page_icon="👥")
try:
    ensure_database_schema()
except Exception as e:
    st.warning(f"Database is starting or not ready yet: {e}")

os.makedirs("./hr_documents", exist_ok=True)

EXCEL_FIELDS = [{'label': 'Employee Code', 'column': 'employee_code', 'type': 'text'}, {'label': 'Employee Category', 'column': 'employee_category', 'type': 'text'}, {'label': 'First Name ', 'column': 'first_name', 'type': 'text'}, {'label': 'Last Name', 'column': 'last_name', 'type': 'text'}, {'label': 'Work Shift', 'column': 'work_shift', 'type': 'text'}, {'label': 'Company', 'column': 'company', 'type': 'text'}, {'label': 'Sponsor Name', 'column': 'sponsor_name', 'type': 'text'}, {'label': 'WPS Sponsor', 'column': 'wps_sponsor', 'type': 'text'}, {'label': 'LOB', 'column': 'lob', 'type': 'text'}, {'label': 'Grade/Band', 'column': 'grade_band', 'type': 'text'}, {'label': 'Date of Birth', 'column': 'date_of_birth', 'type': 'date'}, {'label': 'Reporting Manager Employee Code/Name', 'column': 'reporting_manager_employee_code_name', 'type': 'text'}, {'label': 'Family Status(Yes/No)', 'column': 'family_status_yes_no', 'type': 'text'}, {'label': 'Leave Policy', 'column': 'leave_policy', 'type': 'text'}, {'label': 'Last rejoin Date ', 'column': 'last_rejoin_date', 'type': 'date'}, {'label': 'Annual Leave Balance (As on date) ', 'column': 'annual_leave_balance_as_on_date', 'type': 'number'}, {'label': 'Annual Leave Balance ', 'column': 'annual_leave_balance', 'type': 'number'}, {'label': 'LOP days( Loss of pay days)', 'column': 'lop_days_loss_of_pay_days', 'type': 'number'}, {'label': 'Business Unit', 'column': 'business_unit', 'type': 'text'}, {'label': 'Working Company Name', 'column': 'working_company_name', 'type': 'text'}, {'label': 'Cost Centre', 'column': 'cost_centre', 'type': 'text'}, {'label': 'Nationality', 'column': 'nationality', 'type': 'text'}, {'label': 'RP / ID Number', 'column': 'rp_id_number', 'type': 'text'}, {'label': 'RP/ID Profession', 'column': 'rp_id_profession', 'type': 'text'}, {'label': 'QID Expiry Date', 'column': 'qid_expiry_date', 'type': 'date'}, {'label': 'Visa Type', 'column': 'visa_type', 'type': 'text'}, {'label': 'Hire Type', 'column': 'hire_type', 'type': 'text'}, {'label': 'Confirmation Date', 'column': 'confirmation_date', 'type': 'date'}, {'label': 'ESB Date', 'column': 'esb_date', 'type': 'date'}, {'label': 'Gender', 'column': 'gender', 'type': 'text'}, {'label': 'Marital Status', 'column': 'marital_status', 'type': 'text'}, {'label': 'Office Mobile No.', 'column': 'office_mobile_no', 'type': 'text'}, {'label': 'Personal Mobile No.', 'column': 'personal_mobile_no', 'type': 'text'}, {'label': 'E-Mail ID (Work)', 'column': 'e_mail_id_work', 'type': 'text'}, {'label': 'No. of Dependents', 'column': 'no_of_dependents', 'type': 'number'}, {'label': 'Blood Group', 'column': 'blood_group', 'type': 'text'}, {'label': 'Building/Villa #', 'column': 'building_villa', 'type': 'text'}, {'label': 'Street #', 'column': 'street', 'type': 'text'}, {'label': 'Zone #', 'column': 'zone', 'type': 'text'}, {'label': 'Apartment', 'column': 'apartment', 'type': 'text'}, {'label': 'Building', 'column': 'building', 'type': 'text'}, {'label': 'Floor', 'column': 'floor', 'type': 'text'}, {'label': 'Street', 'column': 'street_2', 'type': 'text'}, {'label': 'State', 'column': 'state', 'type': 'text'}, {'label': 'Country', 'column': 'country', 'type': 'text'}, {'label': 'Zip Code', 'column': 'zip_code', 'type': 'text'}, {'label': 'Name', 'column': 'name', 'type': 'text'}, {'label': 'Relationship', 'column': 'relationship', 'type': 'text'}, {'label': 'Mobile No with country code', 'column': 'mobile_no_with_country_code', 'type': 'text'}, {'label': 'Travel Sector', 'column': 'travel_sector', 'type': 'text'}, {'label': 'Travel Cost', 'column': 'travel_cost', 'type': 'number'}, {'label': 'No. of Tickets Employee (YEAR)', 'column': 'no_of_tickets_employee_year', 'type': 'number'}, {'label': 'Ticket balance (%)', 'column': 'ticket_balance', 'type': 'number'}, {'label': 'No. Of tickets Family ', 'column': 'no_of_tickets_family', 'type': 'number'}, {'label': 'Salary Pay Type (Cash/Bank Transfer/Pay Card)', 'column': 'salary_pay_type_cash_bank_transfer_pay_card', 'type': 'text'}, {'label': 'Company Accommodation', 'column': 'company_accommodation', 'type': 'text'}, {'label': 'Company  Transportation', 'column': 'company_transportation', 'type': 'text'}, {'label': 'Overtime', 'column': 'overtime', 'type': 'text'}, {'label': 'Company Food', 'column': 'company_food', 'type': 'text'}, {'label': 'Company Fuel Card', 'column': 'company_fuel_card', 'type': 'text'}, {'label': 'Work Permit No.', 'column': 'work_permit_no', 'type': 'text'}, {'label': 'Work Permit Issue Date', 'column': 'work_permit_issue_date', 'type': 'date'}, {'label': 'Work Permit Expiry Date', 'column': 'work_permit_expiry_date', 'type': 'date'}, {'label': 'Office File No.', 'column': 'office_file_no', 'type': 'text'}, {'label': 'Access Card No.', 'column': 'access_card_no', 'type': 'text'}, {'label': 'Bank Code', 'column': 'bank_code', 'type': 'text'}, {'label': 'IBAN No.', 'column': 'iban_no', 'type': 'text'}, {'label': 'Account No.', 'column': 'account_no', 'type': 'text'}, {'label': 'Highest Education Qualification ', 'column': 'highest_education_qualification', 'type': 'text'}, {'label': 'Year of Passing', 'column': 'year_of_passing', 'type': 'date'}, {'label': 'Passport No', 'column': 'passport_no', 'type': 'text'}, {'label': 'Place Of issue', 'column': 'place_of_issue', 'type': 'date'}, {'label': 'Issue Date', 'column': 'issue_date', 'type': 'date'}, {'label': 'Expiry Date', 'column': 'expiry_date', 'type': 'date'}, {'label': 'Licenses Type', 'column': 'licenses_type', 'type': 'text'}, {'label': 'Driving Licenses No', 'column': 'driving_licenses_no', 'type': 'text'}, {'label': 'Expiry Date', 'column': 'expiry_date_2', 'type': 'date'}, {'label': 'Insurance Card No', 'column': 'insurance_card_no', 'type': 'text'}, {'label': 'Issue Date', 'column': 'issue_date_2', 'type': 'date'}, {'label': 'Expiry Date', 'column': 'expiry_date_3', 'type': 'date'}, {'label': 'HRA', 'column': 'hra', 'type': 'number'}, {'label': 'Food Allowance', 'column': 'food_allowance', 'type': 'number'}, {'label': 'Mobile Allowance', 'column': 'mobile_allowance', 'type': 'number'}, {'label': 'Special Allowance', 'column': 'special_allowance', 'type': 'number'}, {'label': 'Over time', 'column': 'over_time', 'type': 'number'}, {'label': 'Total', 'column': 'total', 'type': 'number'}]
REQUIRED_CORE_FIELDS = {"Full Name", "Joining Date", "Designation", "Basic"}
DOCUMENT_TYPES = ["passport", "national_id", "visa", "contract", "qid", "work_permit", "other"]
CORE_FIELD_LABELS = {
    "id": "ID",
    "full_name": "Full Name",
    "join_date": "Joining Date",
    "status": "Status",
    "role_title": "Designation",
    "department": "Department",
    "base_salary": "Base Salary (QAR)",
    "created_at": "Created At",
    "updated_at": "Updated At",
}
FIELD_LABEL_OVERRIDES = {
    "street": "Street Number",
    "street_2": "Street Name",
    "name": "Emergency Contact Name",
    "issue_date": "Passport Issue Date",
    "expiry_date": "Passport Expiry Date",
    "expiry_date_2": "Driving License Expiry Date",
    "issue_date_2": "Insurance Issue Date",
    "expiry_date_3": "Insurance Expiry Date",
}
FIELD_LABELS = {
    **CORE_FIELD_LABELS,
    **{field["column"]: field["label"].strip() for field in EXCEL_FIELDS},
    **FIELD_LABEL_OVERRIDES,
}
DISPLAY_FIRST_COLUMNS = [
    "id", "employee_code", "full_name", "join_date", "status", "role_title",
    "department", "base_salary", "company", "nationality", "rp_id_number",
    "e_mail_id_work", "date_of_birth", "personal_mobile_no",
]
PDF_SECTIONS = [
    ("Core Employment Details", ["id", "employee_code", "full_name", "join_date", "status", "role_title", "department", "base_salary", "employee_category", "work_shift", "company", "lob", "grade_band"]),
    ("Personal & Identity", ["first_name", "last_name", "date_of_birth", "nationality", "gender", "marital_status", "blood_group", "rp_id_number", "rp_id_profession", "qid_expiry_date", "visa_type", "hire_type"]),
    ("Contact & Address", ["office_mobile_no", "personal_mobile_no", "e_mail_id_work", "building_villa", "street", "zone", "apartment", "building", "floor", "street_2", "state", "country", "zip_code"]),
    ("Sponsor, Reporting & Leave", ["sponsor_name", "wps_sponsor", "reporting_manager_employee_code_name", "family_status_yes_no", "leave_policy", "last_rejoin_date", "annual_leave_balance_as_on_date", "annual_leave_balance", "lop_days_loss_of_pay_days", "business_unit", "working_company_name", "cost_centre"]),
    ("Emergency, Travel & Benefits", ["name", "relationship", "mobile_no_with_country_code", "travel_sector", "travel_cost", "no_of_tickets_employee_year", "ticket_balance", "no_of_tickets_family", "salary_pay_type_cash_bank_transfer_pay_card", "company_accommodation", "company_transportation", "overtime", "company_food", "company_fuel_card"]),
    ("Documents, Bank & Education", ["work_permit_no", "work_permit_issue_date", "work_permit_expiry_date", "office_file_no", "access_card_no", "bank_code", "iban_no", "account_no", "highest_education_qualification", "year_of_passing", "passport_no", "place_of_issue", "issue_date", "expiry_date", "licenses_type", "driving_licenses_no", "expiry_date_2", "insurance_card_no", "issue_date_2", "expiry_date_3"]),
    ("Salary Components", ["hra", "food_allowance", "mobile_allowance", "special_allowance", "over_time", "total", "created_at", "updated_at"]),
]

def display_label(column_name):
    return FIELD_LABELS.get(column_name, column_name.replace("_", " ").title())

def format_employee_value(column_name, value):
    if value is None or pd.isna(value):
        return "Not provided"
    if hasattr(value, "strftime") and ("date" in column_name or column_name in ["created_at", "updated_at"]):
        return value.strftime("%Y-%m-%d")
    if column_name in ["base_salary", "travel_cost", "hra", "food_allowance", "mobile_allowance", "special_allowance", "over_time", "total"]:
        try:
            return f"{float(value):,.2f} QAR"
        except Exception:
            return str(value)
    return str(value)

def order_employee_columns(columns):
    ordered = [col for col in DISPLAY_FIRST_COLUMNS if col in columns]
    ordered.extend([col for col in columns if col not in ordered])
    return ordered

def display_employee_dataframe(df):
    if df.empty:
        return df
    ordered_cols = order_employee_columns(df.columns.tolist())
    display_df = df[ordered_cols].copy()
    for col in display_df.columns:
        if col in ["base_salary", "travel_cost", "hra", "food_allowance", "mobile_allowance", "special_allowance", "over_time", "total"]:
            display_df[col] = display_df[col].map(lambda x: "" if pd.isna(x) else f"{float(x):,.2f}")
    renamed_columns = []
    seen_labels = {}
    for col in display_df.columns:
        label = display_label(col)
        seen_labels[label] = seen_labels.get(label, 0) + 1
        if seen_labels[label] > 1:
            label = f"{label} ({col})"
        renamed_columns.append(label)
    display_df.columns = renamed_columns
    return display_df

def employee_pdf_filename(employee):
    employee_name = re.sub(r"[^A-Za-z0-9_-]+", "_", str(employee.get("full_name") or "employee")).strip("_")
    return f"employee_profile_{employee.get('id')}_{employee_name}.pdf"

render_page_header(
    "Core HR Management",
    "Onboard employees, bulk import Excel data, manage employee records, documents and departments from one clean workspace.",
    "Kaashify ERP · People Operations"
)

def get_departments():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM departments ORDER BY name ASC")
                rows=[r[0] for r in cur.fetchall()]
                if rows:
                    return rows
    except Exception:
        pass
    return ["Human Resources", "Finance", "IT", "Operations", "Sales"]

def render_dynamic_field(field, key_prefix, value=None):
    label = field["label"].strip()
    key = f"{key_prefix}_{field['column']}"
    if field["type"] == "number":
        v = float(value) if value not in (None, "") else 0.0
        return st.number_input(label, value=v, step=1.0, format="%.2f", key=key)
    if field["type"] == "date":
        v = value
        if isinstance(v, str):
            try: v = datetime.date.fromisoformat(v[:10])
            except Exception: v = None
        min_date = datetime.date(1900, 1, 1)
        max_date = datetime.date.today() if field["column"] == "date_of_birth" else datetime.date(2100, 12, 31)
        return st.date_input(label, value=v, min_value=min_date, max_value=max_date, key=key) if v else st.date_input(label, value=None, min_value=min_date, max_value=max_date, key=key)
    return st.text_input(label, value="" if value is None else str(value), key=key)

def field_value_for_db(field, value):
    if value in (None, ""):
        return None
    if field["type"] == "date" and hasattr(value, "isoformat"):
        return value
    return value

def fetch_employee(employee_id):
    with get_db_connection() as conn:
        return pd.read_sql_query("SELECT * FROM employees WHERE id=%s", conn, params=[employee_id])

def generate_employee_profile_pdf(employee):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "EmployeeProfileTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=15,
        alignment=2
    )
    section_style = ParagraphStyle(
        "EmployeeProfileSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=8,
        spaceAfter=8
    )
    label_style = ParagraphStyle(
        "EmployeeProfileLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=colors.HexColor("#475569")
    )
    value_style = ParagraphStyle(
        "EmployeeProfileValue",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        textColor=colors.HexColor("#1F2937"),
        leading=11
    )

    header_data = [
        [Paragraph("<b>KAASHIFY ERP</b><br/><font size=8 color='#64748B'>LOCAL SECURE HR OPERATIONS</font>", styles["Normal"]),
         Paragraph("EMPLOYEE PROFILE", title_style)]
    ]
    header_table = Table(header_data, colWidths=[250, 280])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    divider = Table([[""]], colWidths=[530], rowHeights=[2])
    divider.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), colors.HexColor("#1E3A8A")),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(divider)
    story.append(Spacer(1, 15))

    summary_data = [
        [Paragraph("Employee ID:", label_style), Paragraph(escape(format_employee_value("id", employee.get("id"))), value_style),
         Paragraph("Status:", label_style), Paragraph(escape(format_employee_value("status", employee.get("status"))), value_style)],
        [Paragraph("Employee Name:", label_style), Paragraph(escape(format_employee_value("full_name", employee.get("full_name"))), value_style),
         Paragraph("Department:", label_style), Paragraph(escape(format_employee_value("department", employee.get("department"))), value_style)],
        [Paragraph("Designation:", label_style), Paragraph(escape(format_employee_value("role_title", employee.get("role_title"))), value_style),
         Paragraph("Base Salary:", label_style), Paragraph(escape(format_employee_value("base_salary", employee.get("base_salary"))), value_style)],
    ]
    summary_table = Table(summary_data, colWidths=[110, 160, 100, 160])
    summary_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F8FAFC")),
        ("BACKGROUND", (2,0), (2,-1), colors.HexColor("#F8FAFC")),
        ("PADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    for section_index, (section_title, columns) in enumerate(PDF_SECTIONS):
        rows = []
        available_columns = [col for col in columns if col in employee]
        for i in range(0, len(available_columns), 2):
            left = available_columns[i]
            right = available_columns[i + 1] if i + 1 < len(available_columns) else None
            row = [
                Paragraph(escape(display_label(left)), label_style),
                Paragraph(escape(format_employee_value(left, employee.get(left))), value_style),
            ]
            if right:
                row.extend([
                    Paragraph(escape(display_label(right)), label_style),
                    Paragraph(escape(format_employee_value(right, employee.get(right))), value_style),
                ])
            else:
                row.extend(["", ""])
            rows.append(row)
        if not rows:
            continue
        if section_index == 4:
            story.append(PageBreak())
        story.append(Paragraph(section_title, section_style))
        section_table = Table(rows, colWidths=[120, 145, 120, 145], repeatRows=0)
        section_table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F8FAFC")),
            ("BACKGROUND", (2,0), (2,-1), colors.HexColor("#F8FAFC")),
            ("PADDING", (0,0), (-1,-1), 6),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(section_table)
        story.append(Spacer(1, 10))

    story.append(Spacer(1, 18))
    sig_data = [
        [Paragraph("_____________________________<br/><b>HR Officer</b>", styles["Normal"]),
         Paragraph("_____________________________<br/><b>Employee Signature</b>", styles["Normal"])]
    ]
    sig_table = Table(sig_data, colWidths=[265, 265])
    sig_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(sig_table)

    doc.build(story)
    buffer.seek(0)
    return buffer


def normalize_excel_header(value):
    """Normalize Excel headers so small spacing/case differences do not break imports."""
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())

def build_excel_column_map(df):
    return {normalize_excel_header(col): col for col in df.columns}

def get_excel_value(row, column_map, possible_headers, default=None):
    for header in possible_headers:
        source_col = column_map.get(normalize_excel_header(header))
        if source_col is not None:
            value = row.get(source_col)
            if pd.notna(value) and str(value).strip() != "":
                return value
    return default

def clean_excel_value(field_type, value):
    if value is None or pd.isna(value) or str(value).strip() == "":
        return None
    if field_type == "date":
        try:
            return pd.to_datetime(value, errors="coerce").date()
        except Exception:
            return None
    if field_type == "number":
        try:
            cleaned = str(value).replace(",", "").strip()
            return float(cleaned) if cleaned else None
        except Exception:
            return None
    return str(value).strip()

def row_to_employee_payload(row, column_map, default_department, default_status):
    first_name = clean_excel_value("text", get_excel_value(row, column_map, ["First Name", "First Name "]))
    last_name = clean_excel_value("text", get_excel_value(row, column_map, ["Last Name"]))
    full_name = clean_excel_value("text", get_excel_value(row, column_map, ["Full Name", "Employee Name", "Name of Employee"]))
    if not full_name:
        full_name = " ".join([x for x in [first_name, last_name] if x]).strip()

    join_date = clean_excel_value("date", get_excel_value(row, column_map, ["Joining Date", "Join Date", "Date of Joining"])) or datetime.date.today()
    role_title = clean_excel_value("text", get_excel_value(row, column_map, ["Designation", "Role", "Role Title", "Job Title"])) or "Not Specified"
    department = clean_excel_value("text", get_excel_value(row, column_map, ["Department", "Business Unit", "LOB"])) or default_department
    status = clean_excel_value("text", get_excel_value(row, column_map, ["Status", "Employee Status"])) or default_status
    if status not in ["Active", "Terminated"]:
        status = default_status
    base_salary = clean_excel_value("number", get_excel_value(row, column_map, ["Basic", "Basic Salary", "Starting Base Salary (QAR)", "Base Salary", "Total"])) or 0.0

    dynamic_cols = []
    dynamic_vals = []
    for field in EXCEL_FIELDS:
        if field["column"] in ["full_name", "joining_date", "designation", "basic"]:
            continue
        dynamic_cols.append(field["column"])
        dynamic_vals.append(clean_excel_value(field["type"], get_excel_value(row, column_map, [field["label"], field["column"]])))

    all_cols = ["full_name", "join_date", "status", "role_title", "department", "base_salary"] + dynamic_cols
    all_vals = [full_name, join_date, status, role_title, department, base_salary] + dynamic_vals
    return all_cols, all_vals, full_name, department, role_title, join_date, base_salary

def import_employees_from_excel(uploaded_excel, default_department, default_status):
    df = pd.read_excel(uploaded_excel, engine="openpyxl")
    df = df.dropna(how="all")
    if df.empty:
        return 0, 0, ["The uploaded Excel file has no employee rows with data."]
    column_map = build_excel_column_map(df)
    imported = 0
    skipped = 0
    errors = []
    inserted_names = []
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for idx, row in df.iterrows():
                try:
                    all_cols, all_vals, full_name, department, role_title, join_date, base_salary = row_to_employee_payload(row, column_map, default_department, default_status)
                    if not full_name:
                        skipped += 1
                        errors.append(f"Row {idx + 2}: skipped because Full Name is missing.")
                        continue
                    cur.execute("INSERT INTO departments (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (department,))
                    placeholders = sql.SQL(',').join(sql.Placeholder() * len(all_cols))
                    columns = sql.SQL(',').join(map(sql.Identifier, all_cols))
                    cur.execute(sql.SQL("INSERT INTO employees ({}) VALUES ({}) RETURNING id").format(columns, placeholders), all_vals)
                    employee_id = cur.fetchone()[0]
                    cur.execute(
                        "INSERT INTO employment_history (employee_id, effective_date, change_type, previous_value, new_value, notes) VALUES (%s,%s,'Bulk Excel Onboarding',NULL,%s,%s)",
                        (employee_id, join_date, str(base_salary), f"Imported {full_name} into {department} as {role_title} from Excel upload.")
                    )
                    imported += 1
                    inserted_names.append(full_name)
                except Exception as exc:
                    skipped += 1
                    errors.append(f"Row {idx + 2}: {exc}")
    return imported, skipped, errors[:25]

tab_dir, tab_onboard, tab_manage, tab_depts = st.tabs(["📂 Employee Directory", "➕ Employee Onboarding", "✏️ Modify / Delete", "🏢 Departments"])

with tab_dir:
    st.write("Browse, search, filter, and export the employee registry database.")
    col_search, col_dept, col_status = st.columns([2,1,1])
    with col_search:
        search_query = st.text_input("Search Employee Name / Code", placeholder="Type name or employee code...")
    with col_dept:
        selected_dept = st.selectbox("Department", ["All Departments"] + get_departments())
    with col_status:
        selected_status = st.selectbox("Status", ["All Statuses", "Active", "Terminated"])
    try:
        with get_db_connection() as conn:
            query = "SELECT * FROM employees WHERE 1=1"
            params=[]
            if search_query:
                query += " AND (full_name ILIKE %s OR employee_code ILIKE %s)"
                params.extend([f"%{search_query}%", f"%{search_query}%"])
            if selected_dept != "All Departments":
                query += " AND department=%s"; params.append(selected_dept)
            if selected_status != "All Statuses":
                query += " AND status=%s"; params.append(selected_status)
            query += " ORDER BY id ASC"
            df=pd.read_sql_query(query, conn, params=params)
        if not df.empty:
            display_df = display_employee_dataframe(df)
            st.caption("Select a row to open the full employee profile and download a complete details PDF.")
            table_event = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="employee_directory_table"
            )
            selected_rows = getattr(getattr(table_event, "selection", None), "rows", [])
            if selected_rows:
                selected_employee = df.iloc[selected_rows[0]].to_dict()
                st.markdown("### Employee Full Details")
                st.write(f"**{selected_employee.get('full_name')}** · {selected_employee.get('role_title')} · {selected_employee.get('department')}")
                pdf_col, meta_col = st.columns([1, 2])
                with pdf_col:
                    st.download_button(
                        "Download Employee Details PDF",
                        data=generate_employee_profile_pdf(selected_employee),
                        file_name=employee_pdf_filename(selected_employee),
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                with meta_col:
                    st.info(
                        f"Base Salary: {format_employee_value('base_salary', selected_employee.get('base_salary'))}\n\n"
                        f"Status: {format_employee_value('status', selected_employee.get('status'))}"
                    )

                for section_title, columns in PDF_SECTIONS:
                    section_rows = []
                    for col in columns:
                        if col in selected_employee:
                            section_rows.append({
                                "Field": display_label(col),
                                "Value": format_employee_value(col, selected_employee.get(col))
                            })
                    if section_rows:
                        with st.expander(section_title, expanded=section_title == "Core Employment Details"):
                            st.dataframe(pd.DataFrame(section_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No employee records found.")
    except Exception as e:
        st.error(f"Database error reading employee directory: {e}")

with tab_onboard:
    st.write("Add a new employee using the uploaded Excel field structure.")
    st.markdown("### Bulk Onboarding from Excel")
    st.caption("Upload an Excel file using the same column headers as the employee template. Each row with data will be inserted into the employee database.")
    bulk_col1, bulk_col2, bulk_col3 = st.columns([2, 1, 1])
    with bulk_col1:
        bulk_excel = st.file_uploader("Upload Employee Excel", type=["xlsx"], key="bulk_employee_excel")
    with bulk_col2:
        bulk_default_department = st.selectbox("Default Department for Missing Rows", get_departments(), key="bulk_default_department")
    with bulk_col3:
        bulk_default_status = st.selectbox("Default Status", ["Active", "Terminated"], key="bulk_default_status")
    if bulk_excel is not None:
        try:
            preview_df = pd.read_excel(bulk_excel, engine="openpyxl").dropna(how="all")
            st.info(f"Detected {len(preview_df)} employee row(s) with data. Review the first rows below, then click Import.")
            st.dataframe(preview_df.head(10), use_container_width=True)
            bulk_excel.seek(0)
            if st.button("Import Excel Employees into Database", type="primary"):
                imported, skipped, errors = import_employees_from_excel(bulk_excel, bulk_default_department, bulk_default_status)
                if imported:
                    st.success(f"Imported {imported} employee(s) successfully.")
                if skipped:
                    st.warning(f"Skipped {skipped} row(s).")
                    if errors:
                        st.write("Import issues:")
                        for err in errors:
                            st.write(f"- {err}")
                st.rerun()
        except Exception as e:
            st.error(f"Could not read/import Excel file: {e}")
    st.divider()
    st.markdown("### Manual Employee Onboarding")
    with st.form("onboarding_form", clear_on_submit=True):
        st.markdown("### Required Employee Details")
        c1,c2=st.columns(2)
        with c1:
            full_name=st.text_input("Full Name *")
            join_date=st.date_input("Joining Date *", value=datetime.date.today())
            department=st.selectbox("Department *", get_departments())
        with c2:
            role_title=st.text_input("Designation *")
            base_salary=st.number_input("Basic / Starting Salary (QAR) *", min_value=0.0, step=500.0, format="%.2f")
            status=st.selectbox("Status", ["Active", "Terminated"])
        values={}
        groups=[("Employment Details", EXCEL_FIELDS[:24]), ("ID / Personal / Contact", EXCEL_FIELDS[24:52]), ("Travel / Benefits / Work Permit", EXCEL_FIELDS[52:70]), ("Bank / Education / Passport / License / Salary", EXCEL_FIELDS[70:])]
        for title, fields in groups:
            with st.expander(title, expanded=False):
                for i in range(0, len(fields), 3):
                    cols_ui=st.columns(3)
                    for col_ui, field in zip(cols_ui, fields[i:i+3]):
                        with col_ui:
                            values[field['column']] = render_dynamic_field(field, "new")
        st.markdown("### Verification Document")
        dc1,dc2=st.columns(2)
        with dc1:
            doc_type=st.selectbox("Verification Document Type", DOCUMENT_TYPES)
        with dc2:
            uploaded_file=st.file_uploader("Upload Document PDF", type=["pdf"])
        submit_btn=st.form_submit_button("Submit Employee Onboarding")
        if submit_btn:
            if not full_name.strip(): st.error("Full Name is required.")
            elif not role_title.strip(): st.error("Designation is required.")
            elif base_salary <= 0: st.error("Basic salary must be greater than 0 QAR.")
            else:
                try:
                    dynamic_cols=[f['column'] for f in EXCEL_FIELDS if f['column'] not in ['full_name','joining_date','designation','basic']]
                    dynamic_vals=[field_value_for_db(f, values.get(f['column'])) for f in EXCEL_FIELDS if f['column'] not in ['full_name','joining_date','designation','basic']]
                    all_cols=['full_name','join_date','status','role_title','department','base_salary'] + dynamic_cols
                    all_vals=[full_name.strip(), join_date, status, role_title.strip(), department, base_salary] + dynamic_vals
                    placeholders=sql.SQL(',').join(sql.Placeholder()*len(all_cols))
                    columns=sql.SQL(',').join(map(sql.Identifier, all_cols))
                    with get_db_connection() as conn:
                        with conn.cursor() as cur:
                            cur.execute(sql.SQL("INSERT INTO employees ({}) VALUES ({}) RETURNING id").format(columns, placeholders), all_vals)
                            employee_id=cur.fetchone()[0]
                            cur.execute("INSERT INTO employment_history (employee_id, effective_date, change_type, previous_value, new_value, notes) VALUES (%s,%s,'Onboarding',NULL,%s,%s)", (employee_id, join_date, str(base_salary), f"Onboarded {full_name} into {department} as {role_title}."))
                    if uploaded_file is not None:
                        filename=f"{employee_id}_{doc_type}.pdf"
                        with open(os.path.join("./hr_documents", filename), "wb") as f: f.write(uploaded_file.getbuffer())
                    st.success(f"Employee {full_name} onboarded successfully with ID: {employee_id}.")
                except Exception as e:
                    st.error(f"Error onboarding employee: {e}")

with tab_manage:
    st.write("Modify or delete employee records.")
    try:
        with get_db_connection() as conn:
            employees=pd.read_sql_query("SELECT id, full_name, employee_code FROM employees ORDER BY id", conn)
        if employees.empty:
            st.info("No employees available to modify.")
        else:
            employees['label']=employees.apply(lambda r: f"{int(r['id'])} - {r['full_name']}" + (f" ({r['employee_code']})" if pd.notna(r.get('employee_code')) and r.get('employee_code') else ""), axis=1)
            selected_label=st.selectbox("Select employee", employees['label'].tolist())
            employee_id=int(selected_label.split(' - ')[0])
            emp_df=fetch_employee(employee_id)
            emp=emp_df.iloc[0].to_dict()
            action=st.radio("Action", ["Modify Employee", "Delete Employee"], horizontal=True)
            if action == "Modify Employee":
                with st.form("modify_employee_form"):
                    c1,c2=st.columns(2)
                    with c1:
                        edit_full_name=st.text_input("Full Name *", value=str(emp.get('full_name') or ''))
                        edit_join_date=st.date_input("Joining Date *", value=emp.get('join_date') or datetime.date.today())
                        edit_department=st.selectbox("Department *", get_departments(), index=max(0, get_departments().index(emp.get('department')) if emp.get('department') in get_departments() else 0))
                    with c2:
                        edit_role=st.text_input("Designation *", value=str(emp.get('role_title') or ''))
                        edit_salary=st.number_input("Basic / Starting Salary (QAR) *", value=float(emp.get('base_salary') or 0), step=500.0, format="%.2f")
                        edit_status=st.selectbox("Status", ["Active", "Terminated"], index=0 if emp.get('status')=='Active' else 1)
                    edit_values={}
                    with st.expander("Edit all Excel-based fields", expanded=False):
                        for i in range(0, len(EXCEL_FIELDS), 3):
                            cols_ui=st.columns(3)
                            for col_ui, field in zip(cols_ui, EXCEL_FIELDS[i:i+3]):
                                if field['column'] in ['full_name','joining_date','designation','basic']:
                                    continue
                                with col_ui:
                                    edit_values[field['column']] = render_dynamic_field(field, f"edit_{employee_id}", emp.get(field['column']))
                    save=st.form_submit_button("Save Changes")
                    if save:
                        try:
                            update_cols=['full_name','join_date','status','role_title','department','base_salary'] + [f['column'] for f in EXCEL_FIELDS if f['column'] not in ['full_name','joining_date','designation','basic']]
                            update_vals=[edit_full_name.strip(), edit_join_date, edit_status, edit_role.strip(), edit_department, edit_salary] + [field_value_for_db(f, edit_values.get(f['column'])) for f in EXCEL_FIELDS if f['column'] not in ['full_name','joining_date','designation','basic']]
                            assignments=sql.SQL(',').join(sql.SQL("{} = %s").format(sql.Identifier(c)) for c in update_cols) + sql.SQL(", updated_at = CURRENT_TIMESTAMP")
                            with get_db_connection() as conn:
                                with conn.cursor() as cur:
                                    cur.execute(sql.SQL("UPDATE employees SET {} WHERE id=%s").format(assignments), update_vals + [employee_id])
                                    cur.execute("INSERT INTO employment_history (employee_id, effective_date, change_type, previous_value, new_value, notes) VALUES (%s,%s,'Profile Update',NULL,%s,%s)", (employee_id, datetime.date.today(), edit_status, 'Employee profile updated from Modify/Delete tab.'))
                            st.success("Employee record updated successfully.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating employee: {e}")
            else:
                st.warning("Deleting an employee also deletes linked history and payroll records.")
                confirm=st.checkbox(f"I confirm I want to permanently delete {emp.get('full_name')}")
                if st.button("Delete Employee", type="primary", disabled=not confirm):
                    try:
                        with get_db_connection() as conn:
                            with conn.cursor() as cur:
                                cur.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
                        st.success("Employee deleted successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting employee: {e}")
    except Exception as e:
        st.error(f"Error loading modify/delete section: {e}")

with tab_depts:
    st.write("Add or remove departments used during onboarding and filtering.")
    col_add, col_remove=st.columns(2)
    with col_add:
        with st.form("add_department_form"):
            new_dept=st.text_input("New Department Name")
            desc=st.text_area("Description", height=100)
            if st.form_submit_button("Add Department"):
                if not new_dept.strip(): st.error("Department name is required.")
                else:
                    try:
                        with get_db_connection() as conn:
                            with conn.cursor() as cur:
                                cur.execute("INSERT INTO departments (name, description) VALUES (%s,%s) ON CONFLICT (name) DO UPDATE SET description=EXCLUDED.description", (new_dept.strip(), desc.strip() or None))
                        st.success("Department added/updated."); st.rerun()
                    except Exception as e: st.error(f"Error adding department: {e}")
    with col_remove:
        depts=get_departments()
        dept_to_remove=st.selectbox("Department to Remove", depts)
        replacement=st.selectbox("Move existing employees to", [d for d in depts if d != dept_to_remove] or ["Unassigned"])
        if st.button("Remove Department", type="secondary"):
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE employees SET department=%s WHERE department=%s", (replacement, dept_to_remove))
                        cur.execute("DELETE FROM departments WHERE name=%s", (dept_to_remove,))
                st.success("Department removed and existing employees reassigned."); st.rerun()
            except Exception as e: st.error(f"Error removing department: {e}")
    st.markdown("### Current Departments")
    st.dataframe(pd.DataFrame({"Department": get_departments()}), use_container_width=True, hide_index=True)
