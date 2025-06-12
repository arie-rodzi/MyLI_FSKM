
import streamlit as st
import pandas as pd
import hashlib
import os

# Paths
USER_FILE = "users.csv"
LOGBOOK_DIR = "logbook"
PLACEMENT_DIR = "placement"
EVALUATION_DIR = "evaluation"

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users
@st.cache_data
def load_users():
    return pd.read_csv(USER_FILE)

# Load CSV file safely
def load_csv(filepath):
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return pd.DataFrame()

# Save logbook
def save_logbook(user_id, df):
    df.to_csv(os.path.join(LOGBOOK_DIR, f"{user_id}_logbook.csv"), index=False)

# Main app
def main():
    st.title("MyLI-FSKM: Sistem Latihan Industri")

    df_users = load_users()

    user_id = st.text_input("ID Pengguna")
    password = st.text_input("Kata Laluan", type="password")
    login_btn = st.button("Log Masuk")

    if login_btn:
        hashed_pwd = hash_password(password)
        user = df_users[(df_users['user_id'] == user_id) & (df_users['password'] == hashed_pwd)]

        if not user.empty:
            user_info = user.iloc[0]
            st.success(f"Selamat datang, {user_info['name']} ({user_info['role']})")

            role = user_info['role']

            if role == 'student':
                st.subheader("📌 Maklumat Tempat LI")
                placement_file = os.path.join(PLACEMENT_DIR, f"{user_id}_placement.csv")
                df_place = load_csv(placement_file)
                st.dataframe(df_place)

                st.subheader("📒 Logbook Mingguan")
                logbook_file = os.path.join(LOGBOOK_DIR, f"{user_id}_logbook.csv")
                df_log = load_csv(logbook_file)
                if not df_log.empty:
                    st.dataframe(df_log)

                with st.expander("Kemaskini / Tambah Logbook"):
                    week = st.number_input("Minggu Ke-", min_value=1, step=1)
                    date_start = st.date_input("Tarikh Mula")
                    date_end = st.date_input("Tarikh Tamat")
                    activity = st.text_area("Aktiviti Dijalankan")
                    if st.button("Simpan Logbook"):
                        new_entry = {
                            "week": week,
                            "date_start": date_start,
                            "date_end": date_end,
                            "activity": activity,
                            "supervisor_comment": ""
                        }
                        df_log = df_log.append(new_entry, ignore_index=True)
                        save_logbook(user_id, df_log)
                        st.success("Logbook berjaya dikemaskini.")

            elif role == 'lecturer' or role == 'admin':
                st.subheader("🧾 Penilaian Pelajar")
                student_id = st.text_input("Masukkan ID Pelajar")
                if student_id:
                    eval_file = os.path.join(EVALUATION_DIR, f"{student_id}_evaluation.csv")
                    df_eval = load_csv(eval_file)
                    st.dataframe(df_eval)
        else:
            st.error("ID atau kata laluan salah.")

if __name__ == '__main__':
    main()
