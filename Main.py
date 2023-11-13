import json
import sqlite3
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)
# 定义你的路由

app.config['JSON_AS_ASCII'] = False
app.config['DEFAULT_CHARSET'] = 'utf-8'
token = "xiaozong"


@app.route('/api', methods=['GET', 'POST'])
def api():
    data = request.get_json() if request.method == 'POST' else request.args

    if token != data.get("token"):
        return Response(json.dumps({'message': 'Failed Token'}), status=500)

    msg = 'Hello from GET method' if request.method == 'GET' else 'Hello from POST method'
    return jsonify({'message': msg}), 200


def execute_query(query, args=()):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(query, args)
    output = c.fetchall()
    conn.close()

    return output


@app.route('/management/org/orgAll', methods=['GET'])
def orgTree():

    if token != request.args.get("token"):
        return Response(json.dumps({'message': 'Failed Token'}), status=500)

    query = "SELECT name,nocheck,open,open,pid FROM OrgTree"
    rows = execute_query(query)
    Org = [{"text": row[0], "selected": False, "extraField1": "null", "extraField2": "null", "value": row[4]} for row in
           rows]

    json_data = json.dumps(Org, ensure_ascii=False)
    return Response(json_data, status=200, content_type='application/json;charset=utf-8')


@app.route('/management/org/getOrgTree', methods=['POST'])
def getorgTree():
    if token != request.args.get("token"):
        return Response(json.dumps({'message': 'Failed Token'}), status=500)

    # request.data gets raw data,无值为0，乱值为{1,1}，有id值但不正确为全部。
    raw_data = request.data.decode('utf-8')
    if not raw_data:
        data_dict = 0
    else:
        try:
            # 分离id和它的值
            key,value = raw_data.split('=') if "=" in raw_data else (1,1)
            # 创建字典
            dict_data = {key:int(value)}
        except ValueError:
            return jsonify({"error": "Invalid JSON"}), 40
        data_dict = dict_data.get('id', None) if dict_data else 0

    if data_dict and (not str(data_dict).isnumeric() or int(data_dict) < 1):
        return jsonify({"error": "ID must be a positive integer"}), 400

    base_query = "SELECT pid,isParent,open,nocheck,level,name,id FROM OrgTree"
    query = base_query if data_dict is None else f"{base_query} WHERE pid={data_dict}"
    rows = execute_query(query)
    Org = [{"pid": row[0], "isParent": row[1], "open": row[2], "nocheck": row[3], "level": row[4], "name": row[5],
            "id": row[6]} for row in rows]

    json_data = json.dumps(Org, ensure_ascii=False)
    return Response(json_data, status=200, content_type='application/json;charset=utf-8')


@app.route('/accountmainten/paccount/seladdfrom', methods=['GET'])
def seladdfrom():
    if token != request.args.get("token"):
        return Response(json.dumps({'message': 'Failed Token'}), status=500)

    rows = execute_query("SELECT ADDFROM FROM AddFrom")
    Org = [{"ADDFROM": row[0]} for row in rows]

    json_data = json.dumps(Org, ensure_ascii=False)
    return Response(json_data, status=200, content_type='application/json;charset=utf-8')


@app.route('/accountmainten/paccount/selusertype', methods=['GET'])
def selusertype():
    if token != request.args.get("token"):
        return Response(json.dumps({'message': 'Failed Token'}), status=500)

    rows = execute_query("SELECT ID,NAME FROM UserTypes")
    Org = [{"ID": row[0], "NAME": row[1]} for row in rows]

    json_data = json.dumps(Org, ensure_ascii=False)
    return Response(json_data, status=200, content_type='application/json;charset=utf-8')

@app.route('/admin/page', methods=['GET'])
def userdata():
    if token != request.args.get("token"):
        return Response(json.dumps({'message': 'Failed Token'}), status=500)

    field_names = [
        "id", "userid", "cn", "passwd", "security", "lifetime",
        "departmetname", "usertype", "usertypename", "email",
        "outemail", "telnum", "cardid", "lockstatus", "academy",
        "academyname", "xgmmsj", "addfrom", "container", "petname",
        "modifyEmailFlag", "pwdstrength", "qqopenid", "pwdpolicy",
        "telVcode", "wxopenid", "inetuserstatus", "departmet",
        "userPswd", "telttime"
    ]

    args_dict = {
        "userid": unquote(request.args.get("userid", "")),
        "cn": unquote(request.args.get("cn", "")),
        "departmet": unquote(request.args.get("departmet", "")),
        "departmet_NAME": unquote(request.args.get("departmet_NAME", "")),
        "usertype": unquote(request.args.get("usertype", "")),
        "addfrom": unquote(request.args.get("addfrom", "")),
        "lockstatus": unquote(request.args.get("lockstatus", "")),
    }
    request_data = {k: f"%{v}%" for k, v in args_dict.items() if v}

    page_str = request.args.get("page", "1")
    rows_str = request.args.get("rows", "15")

    # Check if page and rows are positive integers
    if not (page_str.isdigit() and int(page_str) > 0 and rows_str.isdigit() and int(rows_str) > 0):
        return jsonify({"error": "Page and Rows must be positive integers"}), 400

    page = int(page_str)
    rows = int(rows_str)
    offset = (page - 1) * rows

    where_clause = ' AND '.join([f"{k} LIKE ?" for k in request_data.keys()])
    query = f"SELECT * FROM Users WHERE {where_clause} LIMIT {rows} OFFSET {offset}" if where_clause else f"SELECT * FROM Users LIMIT {rows} OFFSET {offset}"

    rows = execute_query(query, tuple(request_data.values()))
    sum_rows = execute_query('SELECT COUNT(*) FROM Users')[0][0]
    Org = [dict(zip(field_names, row)) for row in rows]

    json_data = json.dumps({"rows": Org,"total": sum_rows}, ensure_ascii=False)
    return Response(json_data, status=200, content_type='application/json;charset=utf-8')


if __name__ == '__main__':
    app.run(debug=True)
