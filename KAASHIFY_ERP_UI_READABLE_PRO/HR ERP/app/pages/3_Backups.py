import streamlit as st
import os
import subprocess
import datetime
import pandas as pd
from main import get_db_connection
from ui_theme import render_page_header

# Page Configuration
st.set_page_config(layout="wide", page_title="Backups - Kaashify ERP", page_icon="💾")

# Custom Styles
render_page_header("Database Backup Management", "Create, download and manage local PostgreSQL backup snapshots for Kaashify ERP.", "Kaashify ERP · Backups")

# Define directories
backup_dir = "./hr_documents/backups"
os.makedirs(backup_dir, exist_ok=True)

# Layout Columns
col_action, col_list = st.columns([1, 2])

with col_action:
    st.markdown("### Backup Operations")
    st.write("""
    Generate snapshot backups of the Kaashify ERP PostgreSQL database. 
    Backups are saved as standard SQL scripts locally in your workstation's host directory under:
    `./hr_documents/backups/`
    """)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Trigger backup button
    run_backup = st.button("🚀 Create Database Backup", use_container_width=True, type="primary")
    
    if run_backup:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hr_erp_backup_{timestamp}.sql"
        filepath = os.path.join(backup_dir, filename)
        
        # Prepare environment with database password
        env = os.environ.copy()
        env["PGPASSWORD"] = os.getenv("DB_PASSWORD", "hr_password_secure_123")
        
        # Build pg_dump command (Plain text SQL, includes table creation and inserts)
        cmd = [
            "pg_dump",
            "-h", os.getenv("DB_HOST", "db"),
            "-p", os.getenv("DB_PORT", "5432"),
            "-U", os.getenv("DB_USER", "hr_user"),
            "-d", os.getenv("DB_NAME", "hr_erp"),
            "-F", "p", # Plain-text SQL script
            "-c",      # Clean (drop) database objects before recreating (useful for restore)
            "-f", filepath
        ]
        
        with st.spinner("Executing pg_dump engine..."):
            try:
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                if result.returncode == 0:
                    st.success(f"Backup created successfully!")
                    st.info(f"**Filename:** {filename}\n\n**Path:** /app/hr_documents/backups/{filename}")
                else:
                    st.error(f"Backup failed: {result.stderr}")
            except Exception as e:
                st.error(f"Failed to execute backup process: {str(e)}")

    st.markdown("---")
    st.markdown("### Database Connection Status")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                db_ver = cur.fetchone()[0]
                st.success("🟢 Connected to PostgreSQL database cluster.")
                st.caption(f"Engine: {db_ver.split(' on ')[0]}")
    except Exception as e:
        st.error("🔴 Disconnected from PostgreSQL database.")
        st.caption(f"Error: {str(e)}")

with col_list:
    st.markdown("### Local Backup Catalog")
    st.write("Below is a catalog of historical backups found on the local filesystem.")
    
    # Read files in backup directory
    try:
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith(".sql")]
    except Exception as e:
        st.error(f"Failed to read backup folder: {str(e)}")
        backup_files = []
        
    if not backup_files:
        st.info("No backups found in ./hr_documents/backups/")
    else:
        # Build tabular catalog
        backup_data = []
        for file in backup_files:
            path = os.path.join(backup_dir, file)
            stat = os.stat(path)
            size_kb = stat.st_size / 1024.0
            modified_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            backup_data.append({
                "Filename": file,
                "Size (KB)": f"{size_kb:,.2f} KB",
                "Created At": modified_time,
                "_raw_size": stat.st_size
            })
            
        df = pd.DataFrame(backup_data)
        
        # Display list in dataframe
        st.dataframe(df[["Filename", "Size (KB)", "Created At"]], use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### Export / Download Backup File")
        
        # File selector to download
        selected_file = st.selectbox("Select backup to download:", df["Filename"].tolist())
        
        if selected_file:
            selected_path = os.path.join(backup_dir, selected_file)
            try:
                with open(selected_path, "rb") as f:
                    file_data = f.read()
                    
                st.download_button(
                    label=f"📥 Download {selected_file}",
                    data=file_data,
                    file_name=selected_file,
                    mime="text/plain",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error reading file for download: {str(e)}")
                
        # Optional Restore Utility (highly useful for local ERP systems)
        st.markdown("### ⚠️ Database Restore Utility")
        st.warning("Warning: Restoring the database will overwrite all current data. Make sure to back up your current state before proceeding.")
        
        confirm_restore = st.checkbox("I confirm that I want to restore the selected backup and overwrite current database state.")
        
        if confirm_restore:
            restore_btn = st.button("🔥 Run Database Restore", type="primary", use_container_width=True)
            
            if restore_btn:
                # Prepare environment with database password
                env = os.environ.copy()
                env["PGPASSWORD"] = os.getenv("DB_PASSWORD", "hr_password_secure_123")
                
                # Command: psql -h db -U hr_user -d hr_erp -f filepath
                cmd_restore = [
                    "psql",
                    "-h", os.getenv("DB_HOST", "db"),
                    "-p", os.getenv("DB_PORT", "5432"),
                    "-U", os.getenv("DB_USER", "hr_user"),
                    "-d", os.getenv("DB_NAME", "hr_erp"),
                    "-f", os.path.join(backup_dir, selected_file)
                ]
                
                with st.spinner("Restoring database dump..."):
                    try:
                        result = subprocess.run(cmd_restore, env=env, capture_output=True, text=True)
                        if result.returncode == 0:
                            st.success(f"Database restored successfully from {selected_file}!")
                            st.rerun() # Refresh dashboard stats
                        else:
                            st.error(f"Restore failed: {result.stderr}")
                    except Exception as e:
                        st.error(f"Failed to execute restore: {str(e)}")
