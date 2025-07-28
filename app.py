from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import urllib3

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)  # Cho phép gọi từ frontend

def tra_cuu_phat_nguoi(bien_so: str):
    session = requests.Session()
    url = "https://www.csgt.vn/tra-cuu-nhanh"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = session.post(
            url,
            headers=headers,
            data={"keyword": bien_so},
            timeout=10,
            verify=False  # ⚠️ Bỏ kiểm tra chứng chỉ SSL
        )

        if response.status_code != 200:
            return "⚠️ Lỗi kết nối đến máy chủ CSGT."

        soup = BeautifulSoup(response.text, "html.parser")
        ket_qua_div = soup.find("div", class_="result")
        if not ket_qua_div:
            return "🚫 Không tìm thấy kết quả hoặc biển số không hợp lệ."

        return ket_qua_div.get_text(strip=True)

    except Exception as e:
        return f"❌ Lỗi hệ thống: {str(e)}"

@app.route("/api/phat-nguoi", methods=["POST"])
def phat_nguoi_api():
    data = request.get_json()
    bien_so = data.get("bienso", "").strip().upper()

    if not bien_so:
        return jsonify({"error": "⚠️ Vui lòng nhập biển số xe."}), 400

    result = tra_cuu_phat_nguoi(bien_so)
    return jsonify({"result": result})

if __name__ == "__main__":
    # RẤT QUAN TRỌNG: để Render.com truy cập được, bạn phải dùng host=0.0.0.0 và port=10000
    app.run(host="0.0.0.0", port=10000)
