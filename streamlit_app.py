import datetime

import streamlit as st

st.set_page_config(page_title="SQL Server Desktop Client", page_icon="🗄️", layout="wide")

st.title("🗄️ SQL Server Procedure Runner")
st.write(
    "Use this desktop-style Streamlit app to connect to SQL Server and run the "
    "`shiftwisevlcwiselossgain` stored procedure."
)

with st.sidebar:
    st.header("Connection")
    server = st.text_input("Server", value="122.185.20.98")
    port = st.number_input("Port", min_value=1, max_value=65535, value=1433, step=1)
    username = st.text_input("Username", value="sa")
    password = st.text_input("Password", value="ytXfNa24R3mPLpa", type="password")
    database = st.text_input("Database", value="EIPLSMC2223")

st.subheader("Procedure Parameters")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", value=datetime.date(2026, 2, 1))
    start_time = st.time_input("Start time", value=datetime.time(11, 0))
with col2:
    end_date = st.date_input("End date", value=datetime.date(2026, 2, 10))
    end_time = st.time_input("End time", value=datetime.time(13, 0))

param_col1, param_col2 = st.columns(2)
with param_col1:
    machine_id = st.number_input("Machine ID", value=2004647, step=1)
with param_col2:
    shift_id = st.number_input("Shift ID", value=200, step=1)

start_dt = datetime.datetime.combine(start_date, start_time)
end_dt = datetime.datetime.combine(end_date, end_time)

try:
    import pymssql
except ModuleNotFoundError:  # pragma: no cover - runtime guard for missing dependency
    pymssql = None

run_button = st.button(
    "Run procedure",
    type="primary",
    disabled=pymssql is None,
)

if pymssql is None:
    st.warning(
        "The `pymssql` dependency is not installed. Run `pip install -r requirements.txt` "
        "to enable SQL Server connectivity."
    )

if run_button:
    with st.spinner("Connecting and running stored procedure..."):
        try:
            connection = pymssql.connect(
                server=server,
                user=username,
                password=password,
                database=database,
                port=int(port),
                login_timeout=10,
                timeout=30,
            )
            with connection:
                with connection.cursor(as_dict=True) as cursor:
                    query = (
                        "EXECUTE shiftwisevlcwiselossgain %s, %s, %s, %s"
                    )
                    cursor.execute(query, (start_dt, end_dt, int(machine_id), int(shift_id)))
                    rows = cursor.fetchall()
            st.success("Procedure executed successfully.")
            if rows:
                st.dataframe(rows, use_container_width=True)
            else:
                st.info("No rows returned for the selected parameters.")
        except pymssql.Error as exc:
            st.error(f"Database error: {exc}")
        except ValueError as exc:
            st.error(f"Invalid input: {exc}")

st.divider()
st.caption(
    "Tip: You can save this app as a desktop shortcut by running Streamlit "
    "locally and pinning the browser window or using a wrapper like Nativefier."
)
