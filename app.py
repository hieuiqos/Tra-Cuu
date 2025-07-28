from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép frontend truy cập API

def tra_cuu_phat_nguoi(bien_so: str):
    session = requests.Session()
    url = "https://www.csgt.vn/tra-cuu-nhanh"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = session.post(url, headers=headers, data={"keyword": bien_so}, timeout=10)
        if response.status_code != 200:
            return "Lỗi kết nối với máy chủ CSGT."

        soup = BeautifulSoup(response.text, "html.parser")
        ket_qua_div = soup.find("div", class_="result")
        if not ket_qua_div:
            return "Không tìm thấy kết quả hoặc biển số không hợp lệ."

        return ket_qua_div.get_text(strip=True)
    except Exception as e:
        return f"Lỗi hệ thống: {str(e)}"

@app.route("/api/phat-nguoi", methods=["POST"])
def phat_nguoi_api():
    data = request.get_json()
    bien_so = data.get("bienso", "").strip().upper()

    if not bien_so:
        return jsonify({"error": "Biển số không hợp lệ."}), 400

    result = tra_cuu_phat_nguoi(bien_so)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
