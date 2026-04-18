import streamlit as st
import pdfplumber
import pandas as pd
import re
import requests
import io

st.set_page_config(page_title="HUB Data Analytics", layout="wide")

st.title("📊 Hệ thống Trích xuất Dữ liệu Nghiên cứu")
st.markdown("---")

# Hàm xử lý PDF từ code gốc của bạn
def process_pdf(file_obj):
    results = {}
    with pdfplumber.open(file_obj) as pdf:
        # 1. Trích xuất Bảng 2 (Thống kê mô tả) - Trang 5 (index 4)
        page4 = pdf.pages[4]
        table2 = page4.extract_table()
        if table2:
            df2 = pd.DataFrame(table2[1:], columns=table2[0])
            results['desc'] = df2
            
        # 2. Trích xuất Kiểm định Đa cộng tuyến (VIF) - Trang 6 (index 5)
        page5 = pdf.pages[5]
        text5 = page5.extract_text()
        vif_list = []
        target_vars = ["SIZE", "ROA", "ROS", "ROE", "DR", "AS", "WCR", "GDP"]
        for line in text5.split('\n'):
            for var in target_vars:
                if var in line:
                    numbers = re.findall(r'\d+[\.,]\d+', line)
                    if len(numbers) >= 2:
                        vif_list.append({"Biến": var, "Tolerance": numbers[-2], "VIF": numbers[-1]})
        results['vif'] = pd.DataFrame(vif_list)
        
    return results

# Giao diện Sidebar
st.sidebar.header("Cấu hình")
source_type = st.sidebar.radio("Nguồn file:", ["Upload trực tiếp", "Link Google Drive"])

file_to_process = None

if source_type == "Upload trực tiếp":
    uploaded_file = st.sidebar.file_uploader("Chọn file PDF", type="pdf")
    if uploaded_file:
        file_to_process = io.BytesIO(uploaded_file.read())
else:
    drive_url = st.sidebar.text_input("Dán link Drive vào đây:", "https://drive.google.com/file/d/1ryF9_RvO8yL7MFIt7F66qYsMBWY0kxeB/view")
    if st.sidebar.button("Tải file từ Drive"):
        try:
            file_id = drive_url.split('/')[-2]
            direct_link = f'https://drive.google.com/uc?id={file_id}'
            response = requests.get(direct_link)
            file_to_process = io.BytesIO(response.content)
        except:
            st.error("Link Drive không hợp lệ hoặc không ở chế độ công khai.")

# Hiển thị kết quả
if file_to_process:
    with st.spinner('Đang phân tích dữ liệu...'):
        data = process_pdf(file_to_process)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Thống kê mô tả mẫu")
            if 'desc' in data:
                st.dataframe(data['desc'], use_container_width=True)
        
        with col2:
            st.subheader("🔍 Kiểm định VIF")
            if not data['vif'].empty:
                st.table(data['vif'])
                
        st.success("Trích xuất hoàn tất!")
else:
    st.info("Vui lòng cung cấp file PDF để hệ thống làm việc.")
