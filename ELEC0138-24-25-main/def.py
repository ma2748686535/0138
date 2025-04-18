import sys
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 决定是否开启限速
use_limiter = "--on" in sys.argv
if use_limiter:
    limiter = Limiter(get_remote_address, default_limits=["100 per minute"])
    limiter.init_app(app)
    print("✅ Rate Limiting ENABLED")
else:
    print("⚠️ Rate Limiting DISABLED")

# 示例攻击目标接口
@app.route("/search-doctor")
def search_doctor():
    keyword = request.args.get("q", "")
    if use_limiter:
        # 每秒 5 次限制，仅当开启防御时生效
        @limiter.limit("5 per second")
        def limited_response():
            return f"Search results for '{keyword}'"
        return limited_response()
    else:
        return f"Search results for '{keyword}'"

if __name__ == "__main__":
    app.run(debug=True)
