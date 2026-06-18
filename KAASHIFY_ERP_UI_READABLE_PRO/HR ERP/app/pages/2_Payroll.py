import streamlit as st
import datetime
import pandas as pd
import io
from main import get_db_connection, ensure_database_schema
from ui_theme import render_page_header

# ReportLab imports for professional PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Page Configuration
st.set_page_config(layout="wide", page_title="Payroll - Kaashify ERP", page_icon="💳")

# Ensure required database tables exist before running page queries
try:
    ensure_database_schema()
except Exception as e:
    st.warning(f"Database is starting or not ready yet: {e}")

# Custom UI Styles
render_page_header("Interactive Payroll Workspace", "Process monthly compensation, allowances, deductions and generate professional PDF payslips.", "Kaashify ERP · Payroll")

# Helper function to generate PDF Payslip
def generate_payslip_pdf(employee_info, month, year, base_salary, allowances, deductions, net_pay):
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
    
    # Custom styles
    title_style = ParagraphStyle(
        'PayslipTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=15,
        alignment=2 # Right aligned
    )
    
    label_style = ParagraphStyle(
        'PayslipLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#475569')
    )
    
    value_style = ParagraphStyle(
        'PayslipValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#1F2937')
    )
    
    # 1. Header Section
    header_data = [
        [Paragraph("<b>KAASHIFY ERP</b><br/><font size=8 color='#64748B'>LOCAL SECURE HR OPERATIONS</font>", styles['Normal']),
         Paragraph("PAYROLL PAYSLIP", title_style)]
    ]
    header_table = Table(header_data, colWidths=[250, 280])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    
    # 2. Divider Line
    divider = Table([[""]], colWidths=[530], rowHeights=[2])
    divider.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#1E3A8A')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(divider)
    story.append(Spacer(1, 15))
    
    # 3. Employee Info Block
    month_name = datetime.date(1900, month, 1).strftime('%B')
    info_data = [
        [Paragraph("Employee ID:", label_style), Paragraph(str(employee_info['id']), value_style),
         Paragraph("Pay Period:", label_style), Paragraph(f"{month_name} {year}", value_style)],
        [Paragraph("Employee Name:", label_style), Paragraph(employee_info['name'], value_style),
         Paragraph("Department:", label_style), Paragraph(employee_info['dept'], value_style)],
        [Paragraph("Designation:", label_style), Paragraph(employee_info['role'], value_style),
         Paragraph("Payment Currency:", label_style), Paragraph("Qatari Riyal (QAR)", value_style)]
    ]
    info_table = Table(info_data, colWidths=[110, 160, 100, 160])
    info_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # 4. Earnings & Deductions Grid
    grid_data = [
        [Paragraph("<b>Description</b>", label_style), Paragraph("<b>Earnings (QAR)</b>", label_style), Paragraph("<b>Deductions (QAR)</b>", label_style)],
        [Paragraph("Base Salary", value_style), Paragraph(f"{base_salary:,.2f}", value_style), Paragraph("0.00", value_style)],
        [Paragraph("Allowances", value_style), Paragraph(f"{allowances:,.2f}", value_style), Paragraph("0.00", value_style)],
        [Paragraph("Deductions", value_style), Paragraph("0.00", value_style), Paragraph(f"{deductions:,.2f}", value_style)],
        [Paragraph("<b>Total Calculations</b>", label_style), Paragraph(f"<b>{(base_salary+allowances):,.2f}</b>", label_style), Paragraph(f"<b>{deductions:,.2f}</b>", label_style)]
    ]
    grid_table = Table(grid_data, colWidths=[250, 140, 140])
    grid_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 25))
    
    # 5. Net Pay Block
    net_data = [
        [Paragraph("<font size=11><b>TOTAL NET PAYABLE (QAR)</b></font>", label_style),
         Paragraph(f"<font size=13><b>{net_pay:,.2f} QAR</b></font>", ParagraphStyle('NetStyle', parent=styles['Normal'], alignment=2, fontName='Helvetica-Bold', textColor=colors.HexColor('#1E3A8A')))]
    ]
    net_table = Table(net_data, colWidths=[280, 250])
    net_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#1E3A8A')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(net_table)
    story.append(Spacer(1, 40))
    
    # 6. Signature Lines
    sig_data = [
        [Paragraph("_____________________________<br/><b>HR & Payroll Director</b>", styles['Normal']),
         Paragraph("_____________________________<br/><b>Employee Signature</b>", styles['Normal'])]
    ]
    sig_table = Table(sig_data, colWidths=[265, 265])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(sig_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


# Fetch Employees list
employees_options = {}
try:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, full_name, base_salary, role_title, department 
                FROM employees 
                WHERE status = 'Active' 
                ORDER BY full_name ASC
            """)
            for row in cur.fetchall():
                emp_id = row[0]
                emp_name = row[1]
                emp_salary = float(row[2])
                emp_role = row[3]
                emp_dept = row[4]
                
                label = f"{emp_name} (ID: {emp_id} - {emp_role})"
                employees_options[label] = {
                    'id': emp_id,
                    'name': emp_name,
                    'salary': emp_salary,
                    'role': emp_role,
                    'dept': emp_dept
                }
except Exception as e:
    st.error(f"Error loading employee database: {str(e)}")

# UI Execution
if not employees_options:
    st.warning("No active employees found. Please onboard employees first.")
else:
    col_sel, col_calc = st.columns([1, 2])
    
    with col_sel:
        st.markdown("### Select Employee")
        selected_label = st.selectbox("Active Directory Select", list(employees_options.keys()))
        selected_emp = employees_options[selected_label]
        
        st.info(f"""
        **Profile Details:**
        *   **Department:** {selected_emp['dept']}
        *   **Role:** {selected_emp['role']}
        *   **Base Salary:** {selected_emp['salary']:,.2f} QAR
        """)
        
        # Historical Base rates fetch
        st.markdown("### Base Rate & Role History")
        try:
            with get_db_connection() as conn:
                hist_query = """
                    SELECT effective_date, change_type, previous_value, new_value, notes 
                    FROM employment_history 
                    WHERE employee_id = %s 
                    ORDER BY effective_date DESC
                """
                df_hist = pd.read_sql_query(hist_query, conn, params=[selected_emp['id']])
                if not df_hist.empty:
                    df_hist.columns = ["Effective Date", "Event Type", "Prev Value", "New Value", "Change Notes"]
                    st.dataframe(df_hist, use_container_width=True, hide_index=True)
                else:
                    st.write("No recorded job history events.")
        except Exception as e:
            st.error(f"Error reading history: {str(e)}")
            
    with col_calc:
        st.markdown("### Process Payroll")
        
        # Payroll Period
        col_month, col_year = st.columns(2)
        with col_month:
            current_month_index = datetime.date.today().month - 1
            month = st.selectbox("Payroll Month", list(range(1, 13)), index=current_month_index, format_func=lambda m: datetime.date(1900, m, 1).strftime('%B'))
        with col_year:
            year = st.number_input("Payroll Year", min_value=2020, max_value=2050, value=datetime.date.today().year, step=1)
            
        # Adjacent input columns
        col_base, col_allow, col_ded = st.columns(3)
        with col_base:
            base_salary_val = st.number_input("Base Salary (QAR) [Read-Only]", value=selected_emp['salary'], disabled=True, format="%.2f")
        with col_allow:
            allowances = st.number_input("Allowances (QAR)", min_value=0.0, step=100.0, value=0.0, format="%.2f")
        with col_ded:
            deductions = st.number_input("Deductions (QAR)", min_value=0.0, step=100.0, value=0.0, format="%.2f")
            
        # Calculation formula
        net_pay = base_salary_val + allowances - deductions
        
        # Warning if deductions exceed earnings
        if net_pay < 0:
            st.warning("Warning: Deductions exceed total base salary and allowances. Net Pay will be negative.")
            
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-container'>Calculated Net Pay: <span class='net-pay-val'>{net_pay:,.2f} QAR</span></div>", unsafe_allow_html=True)
        
        # Submit Button
        submit_payroll = st.button("Process Payroll & Generate Payslip", use_container_width=True, type="primary")
        
        # Check if payroll has already been run for this month/year
        is_already_run = False
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id FROM payroll_records 
                        WHERE employee_id = %s AND processed_month = %s AND processed_year = %s
                    """, (selected_emp['id'], month, year))
                    if cur.fetchone():
                        is_already_run = True
        except Exception:
            pass
            
        if is_already_run:
            st.info(f"Notice: Payroll for this employee for {datetime.date(1900, month, 1).strftime('%B')} {year} was processed previously. Submitting again will update the record.")

        if submit_payroll:
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        # Process / Commit transaction
                        cur.execute("""
                            INSERT INTO payroll_records (employee_id, processed_month, processed_year, base_salary, allowances, deductions, net_pay)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (employee_id, processed_month, processed_year) 
                            DO UPDATE SET 
                                base_salary = EXCLUDED.base_salary,
                                allowances = EXCLUDED.allowances,
                                deductions = EXCLUDED.deductions,
                                net_pay = EXCLUDED.net_pay
                        """, (selected_emp['id'], month, year, base_salary_val, allowances, deductions, net_pay))
                
                st.success(f"Success! Payroll processed for {selected_emp['name']} for period {datetime.date(1900, month, 1).strftime('%B')} {year}.")
                
                # Generate ReportLab PDF
                pdf_buffer = generate_payslip_pdf(selected_emp, month, year, base_salary_val, allowances, deductions, net_pay)
                
                # Present download option
                pdf_filename = f"payslip_{selected_emp['id']}_{year}_{month:02d}.pdf"
                st.download_button(
                    label="📥 Download Professional Payslip PDF",
                    data=pdf_buffer,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error committing payroll database entry: {str(e)}")
                
        # Historical payroll records display
        st.markdown("<br/><h3>Past Payroll Runs</h3>", unsafe_allow_html=True)
        try:
            with get_db_connection() as conn:
                hist_pr = """
                    SELECT processed_year, processed_month, base_salary, allowances, deductions, net_pay, processed_at
                    FROM payroll_records 
                    WHERE employee_id = %s 
                    ORDER BY processed_year DESC, processed_month DESC
                """
                df_pr = pd.read_sql_query(hist_pr, conn, params=[selected_emp['id']])
                if not df_pr.empty:
                    df_pr.columns = ["Year", "Month", "Base Salary (QAR)", "Allowances (QAR)", "Deductions (QAR)", "Net Pay (QAR)", "Processed Date"]
                    
                    # Format float columns
                    float_cols = ["Base Salary (QAR)", "Allowances (QAR)", "Deductions (QAR)", "Net Pay (QAR)"]
                    for col in float_cols:
                        df_pr[col] = df_pr[col].map(lambda x: f"{float(x):,.2f}")
                    
                    # Map month numbers to names
                    df_pr["Month"] = df_pr["Month"].map(lambda m: datetime.date(1900, int(m), 1).strftime('%B'))
                    
                    st.dataframe(df_pr, use_container_width=True, hide_index=True)
                else:
                    st.write("No payroll records found for this employee.")
        except Exception as e:
            st.error(f"Error retrieving payroll records: {str(e)}")
