import streamlit as st
import hashlib

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Core Banking System", page_icon="🏦")

# --- HÀM BỔ TRỢ ---
def hash_data(data):
    """Băm dữ liệu bằng SHA-256 để bảo mật."""
    return hashlib.sha256(str(data).encode()).hexdigest()

# --- KHỞI TẠO DỮ LIỆU (Giả lập Database) ---
# Sử dụng st.session_state để dữ liệu không bị mất khi giao diện load lại
if 'transaction_db' not in st.session_state:
    st.session_state.transaction_db = {
        "GD001": "Chuyển tiền 5.000.000 VND",
        "GD002": "Thanh toán tiền điện",
        "GD003": "Rút tiền ATM"
    }

if 'blacklist_db' not in st.session_state:
    # Blacklist chứa mã băm của tài khoản '123456789'
    st.session_state.blacklist_db = {hash_data("123456789")}

# --- GIAO DIỆN NGƯỜI DÙNG (UI) ---
st.title("🏦 Hệ thống Core Banking Mini")
st.markdown("Ứng dụng cấu trúc dữ liệu **Hash Table** trong quản lý giao dịch và bảo mật AML.")

# Chia cột cho giao diện chuyên nghiệp
tab1, tab2, tab3 = st.tabs(["🔍 Tra cứu GD", "🛡️ Check AML", "📊 Database"])

# --- TAB 1: TRA CỨU NHANH ---
with tab1:
    st.header("Tra cứu giao dịch nhanh")
    ma_gd = st.text_input("Nhập mã giao dịch (VD: GD001, GD002...):")
    
    if st.button("Kiểm tra"):
        # Độ phức tạp O(1) nhờ Hash Table (Dictionary)
        ket_qua = st.session_state.transaction_db.get(ma_gd)
        if ket_qua:
            st.success(f"**Kết quả:** {ket_qua}")
        else:
            st.error("Không tìm thấy mã giao dịch này!")

# --- TAB 2: KIỂM TRA AML (Chống rửa tiền) ---
with tab2:
    st.header("Hệ thống sàng lọc AML")
    st.info("Nhập số tài khoản để kiểm tra xem có nằm trong danh sách đen (Blacklist) hay không.")
    
    stk = st.text_input("Nhập số tài khoản cần check:")
    
    if st.button("Sàng lọc hệ thống"):
        if stk:
            stk_hash = hash_data(stk)
            # Kiểm tra trong Set (Hash Table) với thời gian thực thi cực nhanh
            if stk_hash in st.session_state.blacklist_db:
                st.error("🚨 CẢNH BÁO: Tài khoản nằm trong Blacklist -> HÀNH VI BỊ CHẶN!")
            else:
                st.success("✅ Tài khoản hợp lệ -> Giao dịch được DUYỆT.")
        else:
            st.warning("Vui lòng nhập số tài khoản.")

# --- TAB 3: QUẢN TRỊ ---
with tab3:
    st.header("Dữ liệu hệ thống")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bảng giao dịch")
        st.json(st.session_state.transaction_db)
        
    with col2:
        st.subheader("Mã băm Blacklist")
        st.write("Dữ liệu được lưu dưới dạng băm (SHA-256):")
        for h in st.session_state.blacklist_db:
            st.code(h)

# Sidebar hướng dẫn
st.sidebar.title("Hướng dẫn")
st.sidebar.info("""
1. Thử tra cứu: `GD001`
2. Thử tài khoản vi phạm: `123456789`
3. Thử tài khoản sạch: `987654321`
""")
