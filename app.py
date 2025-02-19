import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set page config
st.set_page_config(page_title="🚀 Growth Mindset - File Transformer by Ramsha Noshad", layout='wide')

# Initialize session state for dark mode
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Dark mode toggle
dark_mode = st.toggle("🌙 Toggle Dark Mode", value=st.session_state["dark_mode"])
st.session_state["dark_mode"] = dark_mode

# Apply dark mode styles
if dark_mode:
    st.markdown(
        """
        <style>
            body { background-color: #222; color: #FFF; }
            .stApp { background-color: #222; color: #FFF; }
            .stTextInput, .stButton>button, .stDownloadButton>button, .stRadio>div {
                background-color: #444 !important; 
                color: white !important; 
                border-radius: 8px;
            }
            .stDataFrame { background-color: #333 !important; color: white !important; }
            h1, h2, h3, h4, h5, h6 { color: #FFD700 !important; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Title & Description
st.markdown("<h1 style='text-align: center;'>🛠 Growth Mindset - File Transformer 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>📂 Convert & Clean CSV/Excel Files with Built-in Data Processing & Visualization</p>", unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("📤 **Upload your files (CSV or Excel):**", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        try:
            # Read file
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue

            # File Summary
            st.subheader(f"📄 File Summary: {file.name}")
            st.write(f"📏 **File Size:** {len(file.getvalue()) / 1024:.2f} KB")
            st.write(f"🔢 **Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")
            st.write("📊 **Data Types:**")
            st.write(df.dtypes)

            # Preview Data
            st.subheader(f"👀 Data Preview - {file.name}")
            st.dataframe(df.head())

            # Data Cleaning Options
            st.subheader("🧼 Data Cleaning Options")
            if st.checkbox(f'🛠 Clean Data for {file.name}'):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f'🚀 Remove Duplicates from {file.name}'):
                        df.drop_duplicates(inplace=True)
                        st.success("✅ Duplicates Removed!")

                with col2:
                    if st.button(f'🔍 Fill Missing Values for {file.name}'):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing Values Filled!")

            # Column Selection
            st.subheader('🎛 Select Columns to Keep')
            columns = st.multiselect(f'📌 Choose Columns for {file.name}', df.columns, default=df.columns.tolist())
            if columns:
                df = df[columns]

            # Column Statistics
            st.subheader("📊 Column Statistics")
            selected_column = st.selectbox(f"📈 Select a column for stats", df.columns)
            if selected_column:
                st.write(f"🔹 Min: {df[selected_column].min()}")
                st.write(f"🔹 Max: {df[selected_column].max()}")
                st.write(f"🔹 Mean: {df[selected_column].mean()}")
                st.write(f"🔹 Standard Deviation: {df[selected_column].std()}")

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📈 Show Visualization for {file.name}"):
                numeric_df = df.select_dtypes(include='number')
                if not numeric_df.empty:
                    st.bar_chart(numeric_df.iloc[:, :2])
                else:
                    st.warning("⚠️ No numeric columns available for visualization.")

            # File Conversion
            st.subheader("🔄 File Conversion")
            conversion_type = st.radio(f"🔁 Convert {file.name} to:", ['CSV', 'Excel'], key=file.name)

            if st.button(f"📥 Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine='xlsxwriter')
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.download_button(
                    label=f"📥 Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

        except Exception as e:
            st.error(f"⚠️ Error processing {file.name}: {str(e)}")

    st.success("✅ All files processed successfully!")
