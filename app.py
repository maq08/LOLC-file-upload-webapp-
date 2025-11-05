import os
import uuid
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from sqlalchemy import text
from db_connection import get_engine

app = Flask(__name__)
app.secret_key = 'super_secret_key'

engine = get_engine()

UPLOAD_TEMP = 'uploads/temp'
UPLOAD_PERM = 'uploads/permanent'
MAX_FILE_SIZE = 500 * 1024  # 500 KB
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'txt', 'csv', 'png', 'jpg'}

os.makedirs(UPLOAD_TEMP, exist_ok=True)
os.makedirs(UPLOAD_PERM, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    upload_id = request.form.get('upload_id')
    file = request.files.get('file')

    if not upload_id or not file:
        return jsonify({'success': False, 'message': 'Missing upload ID or file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file type'}), 400

    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    if size > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': 'File exceeds 500KB limit'}), 400

    filename = secure_filename(file.filename)
    stored_name = f"{uuid.uuid4().hex}_{filename}"
    temp_path = os.path.join(UPLOAD_TEMP, stored_name)
    file.save(temp_path)

    with engine.begin() as conn:
        existing_count = conn.execute(
            text("SELECT COUNT(*) FROM UploadedFiles WHERE upload_id=:uid"),
            {'uid': upload_id}
        ).scalar()

        if existing_count >= 10:
            os.remove(temp_path)
            return jsonify({'success': False, 'message': 'Maximum 10 files allowed'}), 400

        conn.execute(text("""
            INSERT INTO UploadedFiles (upload_id, filename, stored_name, path, size_bytes, status)
            VALUES (:upload_id, :filename, :stored_name, :path, :size_bytes, 'uploaded')
        """), {
            'upload_id': upload_id,
            'filename': filename,
            'stored_name': stored_name,
            'path': temp_path,
            'size_bytes': size
        })

    return jsonify({'success': True, 'message': f'✅ "{filename}" uploaded successfully!'})


@app.route('/list', methods=['GET'])
def list_files():
    upload_id = request.args.get('upload_id')
    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT filename, stored_name, size_bytes, status FROM UploadedFiles WHERE upload_id=:id"),
            {'id': upload_id}
        )
        files = [dict(row._mapping) for row in rows]
    return jsonify({'success': True, 'files': files})


@app.route('/remove', methods=['POST'])
def remove_file():
    upload_id = request.form.get('upload_id')
    stored_name = request.form.get('stored_name')
    temp_path = os.path.join(UPLOAD_TEMP, stored_name)
    perm_path = os.path.join(UPLOAD_PERM, stored_name)

    deleted = False
    for path in [temp_path, perm_path]:
        if os.path.exists(path):
            os.remove(path)
            deleted = True

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM UploadedFiles WHERE upload_id=:uid AND stored_name=:sn"),
                     {'uid': upload_id, 'sn': stored_name})

    if deleted:
        return jsonify({'success': True, 'message': '✅ File removed successfully'})
    else:
        return jsonify({'success': False, 'message': '❌ File not found on server'})


@app.route('/final_submit', methods=['POST'])
def final_submit():
    upload_id = request.form.get('upload_id')

    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT stored_name, path FROM UploadedFiles WHERE upload_id=:uid"),
            {'uid': upload_id}
        )
        files = rows.fetchall()
        if not files:
            return jsonify({'success': False, 'message': 'No files to submit'}), 400

        for f in files:
            old_path = f.path
            new_path = os.path.join(UPLOAD_PERM, f.stored_name)
            if os.path.exists(old_path):
                os.replace(old_path, new_path)
            conn.execute(text("""
                UPDATE UploadedFiles SET path=:p, status='saved'
                WHERE upload_id=:uid AND stored_name=:sn
            """), {'p': new_path, 'uid': upload_id, 'sn': f.stored_name})

    return jsonify({'success': True, 'message': '✅ Files successfully saved to server!'})


@app.route('/cancel', methods=['POST'])
def cancel_upload():
    upload_id = request.form.get('upload_id')

    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT path FROM UploadedFiles WHERE upload_id=:uid"),
            {'uid': upload_id}
        )
        for r in rows:
            if os.path.exists(r.path):
                os.remove(r.path)
        conn.execute(text("DELETE FROM UploadedFiles WHERE upload_id=:uid"), {'uid': upload_id})

    return jsonify({'success': True, 'message': '❌ All uploaded files have been removed.'})


if __name__ == '__main__':
    app.run(debug=True)
