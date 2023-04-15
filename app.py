from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
# from neo4j import GraphDatabase

import sqlite3
from flask import jsonify
from pathlib import Path
import json

import z
import wt
import cx

from werkzeug.utils import secure_filename
app = Flask(__name__)
from flask import send_from_directory

# # 设置Neo4j连接
# uri = "bolt://localhost:7687"
# user = "neo4j"
# password = "123456"
# driver = GraphDatabase.driver(uri, auth=(user, password))


# 初始化数据库
def init_db():
    if not Path("history.db").is_file():
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("""
        CREATE TABLE history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()
init_db()

# 配置文件上传
pdfs = UploadSet('pdfs', DOCUMENTS)
app.config['UPLOADED_PDFS_DEST'] = 'json/uploads'
configure_uploads(app, pdfs)


def process_question(question):
    QW = cx.cx(question)

    if QW in wt.wt:
        answer = z.A[QW]
    # 生成回答
    answer = answer.strip()
    if answer:
        # 将问题和答案存入数据库
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("INSERT INTO history (question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()
        conn.close()

    return answer

# 主页
@app.route("/", methods=["GET", "POST"])
def index():
    default_answer = "请在输入框中输入您的问题。"
    if request.method == "POST":
        question = request.form["question"]
        answer = process_question(question)
        return render_template("index.html", answer=answer)
    return render_template("index.html", answer=default_answer)

# 历史记录
@app.route("/history")
def history():
    # 从数据库中获取历史记录
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT question, answer FROM history")
    records = c.fetchall()
    conn.close()

    return render_template("history.html", records=records)

# pdf上传
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'pdf' in request.files:
        filename = pdfs.save(request.files['pdf'])
        # return redirect(url_for('index'))
    return render_template('upload.html')



# # 添加一个新的路由来处理知识图谱的上传
# @app.route('/upload_kg', methods=['POST'])
# def upload_kg():
#     if 'file' not in request.files:
#         return 'No file part', 400
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file', 400
#
#     # 读取上传的JSON文件
#     knowledge_graph_data = json.load("test.json")
#
#     # 将知识图谱导入Neo4j数据库
#     with driver.session() as session:
#         for node in knowledge_graph_data['type']:
#             query = f"MERGE (n:Entity {{name: '{node['type']}', type: '{node['type']}'}})"
#             session.run(query)
#
#         for edge in knowledge_graph_data['edges']:
#             query = f"""
#             MATCH (a:Entity {{id: {edge['source']}}}), (b:Entity {{id: {edge['target']}}})
#             MERGE (a)-[r:RELATIONSHIP {{type: '{edge['relationship']}'}}]->(b)
#             """
#             session.run(query)
#
#     return 'Knowledge graph uploaded and imported successfully', 200

# 添加一个新的路由来显示知识图谱可视化
#
# @app.route("/api/get_kg_data")
# def get_kg_data():
#     query_nodes = "MATCH (n) RETURN n"
#     query_links = "MATCH (a)-[r]->(b) RETURN a, r, b"
#
#     # 查询节点和链接
#     with driver.session() as session:
#         result_nodes = session.run(query_nodes)
#         result_links = session.run(query_links)
#
#     # 转换节点数据
#     nodes = []
#     for record in result_nodes:
#         node = record["n"]
#         nodes.append({"id": node.id, "name": node["name"], "type": node["type"]})
#
#     # 转换链接数据
#     links = []
#     for record in result_links:
#         source = record["a"]
#         target = record["b"]
#         relationship = record["r"]
#         links.append({"source": source.id, "target": target.id, "type": relationship.type})
#
#     # 返回JSON数据
#     return jsonify({"nodes": nodes, "links": links})

if __name__ == "__main__":
    app.run(debug=True)