import streamlit as st
from datetime import datetime
import pandas as pd
from db_config import get_connection, initialize_db_from_csv
from authentication import authenticate_user, register_user

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="Client Query Management System", layout="wide")

if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- Initialize DB from CSV ----------------
initialize_db_from_csv("queriesdata.csv")

# ---------------- LOGIN / REGISTER ----------------
if st.session_state.role is None:
    st.title("Client Query Management System")
    action = st.radio("Choose Action", ["Login", "Register"])

    # -------- REGISTER --------
    if action == "Register":
        st.subheader("User Registration")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Client", "Support"])

        if st.button("Register"):
            if not username or not password:
                st.error("All fields are required")
            else:
                try:
                    register_user(username, password, role)
                    st.success("User registered successfully")
                except Exception as e:
                    st.error(str(e))

    # -------- LOGIN --------
    else:
        st.subheader("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = authenticate_user(username, password)
            if role:
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid username or password")

# ---------------- CLIENT PAGE ----------------
elif st.session_state.role == "Client":
    st.title("Client Query Submission")

    email = st.text_input("Email ID")
    mobile = st.text_input("Mobile Number")
    category = st.text_input("Category")
    heading = st.text_input("Query Heading")
    description = st.text_area("Query Description")

    if st.button("Submit Query"):
        if not all([email, mobile, category, heading, description]):
            st.error("Please fill all fields")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO queries
                (mail_id, mobile_number, category, query_heading,
                 query_description, status, query_created_time)
                VALUES (%s,%s,%s,%s,%s,'Open',%s)
            """, (email, mobile, category, heading, description, datetime.now()))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Query submitted successfully")

    if st.button("Logout"):
        st.session_state.role = None
        st.rerun()

# ---------------- SUPPORT DASHBOARD ----------------
elif st.session_state.role == "Support":
    st.title("Support Team Dashboard")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM queries", conn)
    conn.close()

    # Calculate resolution time
    df['query_created_time'] = pd.to_datetime(df['query_created_time'])
    df['query_closed_time'] = pd.to_datetime(df['query_closed_time'])
    df['resolution_time'] = df['query_closed_time'] - df['query_created_time']

    # Filters
    status_filter = st.selectbox("Filter by Status", ["All", "Open", "Closed"])
    category_filter = st.selectbox("Filter by Category", ["All"] + df["category"].dropna().unique().tolist())

    filtered_df = df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["category"] == category_filter]

    st.subheader("Query Table")
    st.dataframe(filtered_df, use_container_width=True)

    # Close Query
    open_queries = filtered_df[filtered_df["status"] == "Open"]
    if not open_queries.empty:
        query_id = st.selectbox("Select Query ID to Close", open_queries["query_id"])
        if st.button("Close Query"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE queries
                SET status='Closed', query_closed_time=%s
                WHERE query_id=%s
            """, (datetime.now(), query_id))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Query Closed Successfully")
            st.rerun()
  # Refresh dashboard

    # Metrics
    st.subheader("Support Metrics")
    total_open = df[df["status"]=="Open"].shape[0]
    total_closed = df[df["status"]=="Closed"].shape[0]
    avg_resolution = df["resolution_time"].dropna().mean()
    st.metric("Open Queries", total_open)
    st.metric("Closed Queries", total_closed)
    if pd.notna(avg_resolution):
        st.metric("Average Resolution Time", str(avg_resolution))

    if st.button("Logout"):
        st.session_state.role = None
        st.rerun()
