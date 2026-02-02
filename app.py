import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS 
import pyodbc

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
    )
    return pyodbc.connect(conn_str)
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Title, BookAuthor, ReviewAuthor, Review, PublicationDate, Stars, LinkBookCover FROM Reviews")

        rows = cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append({
                "title": row[0],
                "bookAuthor": row[1],
                "reviewAuthor": row[2],
                "review": row[3],
                "publicationDate": row[4].strftime('%d.%m.%Y') if row[4] else None,
                "stars": row[5],
                "image": row[6]
            })
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/forum', methods=['GET'])
def get_forum():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CommentAuthor, Comment, CommentDate FROM Forum")

        rows = cursor.fetchall()
        reviews = []
        for row in rows:
            reviews.append({
                "commentAuthor": row[0],
                "comment": row[1],
                "commentDate": row[2].strftime('%d.%m.%Y') if row[2] else None
            })
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/premieres', methods=['GET'])
def get_premieres():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Title, Author, Description, PremiereDate, LinkBookCover FROM Premieres")

        rows = cursor.fetchall()
        premieres = []
        for row in rows:
            premieres.append({
                "title": row[0],
                "author": row[1],
                "description": row[2],
                "premiereDate": row[3].strftime('%d.%m.%Y') if row[3] else None,
                "image": row[4]
            })
        conn.close()
        return jsonify(premieres)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)