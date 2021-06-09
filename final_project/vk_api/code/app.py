import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db_user = os.environ.get('MYSQL_USER', 'test_qa')
db_password = os.environ.get('MYSQL_PASSWORD', 'qa_test')
db_host = os.environ.get('MYSQL_HOST', 'mysql')
db_port = os.environ.get('MYSQL_PORT', '3306')
db_name = os.environ.get('MYSQL_DB', 'myapp_test_db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class VkUser(db.Model):
    __tablename__ = 'vk_users'

    def __repr__(self):
        return f"<VK_User(" \
               f"id='{self.id}'," \
               f"username='{self.username}'," \
               f"vk_id='{self.vk_id}'," \
               f")>"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False)
    vk_id = db.Column(db.String(200), nullable=False)


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_vk_id(username):
    if user := VkUser.query.filter_by(username=username).first():
        return jsonify({'vk_id': user.vk_id}), 200
    else:
        return jsonify({}), 404


if __name__ == '__main__':
    host = os.environ.get('VK_API_HOST', '0.0.0.0')
    port = os.environ.get('VK_API_PORT', '80')

    db.create_all()
    app.run(host, port)
