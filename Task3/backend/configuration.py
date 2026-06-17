from flask import request, jsonify
from db import get_db

def init_app(app):

    # ---------------- BATCH ---------------- #

    # Create Batch
    @app.route('/create_batch', methods=['POST'])
    def create_batch():
        data = request.json
        conn = get_db()
        conn.execute("INSERT INTO batch VALUES (NULL,?,?,?)",
                     (data['name'], data['start'], data['end']))
        conn.commit()
        return jsonify({"msg": "Batch created"})

    # View Batches
    @app.route('/view_batch', methods=['GET'])
    def view_batch():
        conn = get_db()
        data = conn.execute("SELECT * FROM batch").fetchall()
        return jsonify([dict(row) for row in data])

    # Update Batch
    @app.route('/update_batch', methods=['PUT'])
    def update_batch():
        data = request.json
        conn = get_db()
        conn.execute("UPDATE batch SET name=?, start=?, end=? WHERE id=?",
                     (data['name'], data['start'], data['end'], data['id']))
        conn.commit()
        return jsonify({"msg": "Batch updated"})

    # Delete Batch
    @app.route('/delete_batch/<int:id>', methods=['DELETE'])
    def delete_batch(id):
        conn = get_db()
        conn.execute("DELETE FROM batch WHERE id=?", (id,))
        conn.commit()
        return jsonify({"msg": "Batch deleted"})


    # ---------------- TECHNOLOGY ---------------- #

    # Create Technology
    @app.route('/create_tech', methods=['POST'])
    def create_tech():
        data = request.json
        conn = get_db()
        conn.execute("INSERT INTO technology VALUES (NULL,?)",
                     (data['name'],))
        conn.commit()
        return jsonify({"msg": "Technology added"})

    # View Technology
    @app.route('/view_tech', methods=['GET'])
    def view_tech():
        conn = get_db()
        data = conn.execute("SELECT * FROM technology").fetchall()
        return jsonify([dict(row) for row in data])

    # Update Technology
    @app.route('/update_tech', methods=['PUT'])
    def update_tech():
        data = request.json
        conn = get_db()
        conn.execute("UPDATE technology SET name=? WHERE id=?",
                     (data['name'], data['id']))
        conn.commit()
        return jsonify({"msg": "Technology updated"})

    # Delete Technology
    @app.route('/delete_tech/<int:id>', methods=['DELETE'])
    def delete_tech(id):
        conn = get_db()
        conn.execute("DELETE FROM technology WHERE id=?", (id,))
        conn.commit()
        return jsonify({"msg": "Technology deleted"})


    # ---------------- ROUNDS ---------------- #

    # Configure Rounds
    @app.route('/set_rounds', methods=['POST'])
    def set_rounds():
        data = request.json
        conn = get_db()
        conn.execute("INSERT INTO rounds VALUES (NULL,?,?,?)",
                     (data['batch'], data['technology'], data['rounds']))
        conn.commit()
        return jsonify({"msg": "Rounds configured"})