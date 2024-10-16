from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'

mysql = MySQL(app)

@app.route('/')
def index():
    search_query = request.args.get('search')
    cur = mysql.connection.cursor()
    if search_query:
        cur.execute("SELECT * FROM drugs WHERE id LIKE %s OR name LIKE %s", (f"%{search_query}%", f"%{search_query}%"))
    else:
        cur.execute("SELECT * FROM drugs")
    drugs = cur.fetchall()
    cur.close()
    return render_template('index.html', drugs=drugs)

@app.route('/add', methods=['GET', 'POST'])
def add_drug():
    if request.method == 'POST':
        name = request.form['name']
        stock_level = request.form['stock_level']
        cost = request.form['cost']
        shelf_life = request.form['shelf_life']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO drugs (name, stock_level, cost, shelf_life) VALUES (%s, %s, %s, %s)", (name, stock_level, cost, shelf_life))
        mysql.connection.commit()
        cur.close()
        flash('Drug added successfully!')
        return redirect(url_for('index'))
    return render_template('add_drug.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_drug(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM drugs WHERE id = %s", (id,))
    drug = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        name = request.form['name']
        stock_level = request.form['stock_level']
        cost = request.form['cost']
        shelf_life = request.form['shelf_life']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE drugs SET name = %s, stock_level = %s, cost = %s, shelf_life = %s WHERE id = %s", (name, stock_level, cost, shelf_life, id))
        mysql.connection.commit()
        cur.close()
        flash('Drug updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_drug.html', drug=drug)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_drug(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM drugs WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Drug deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)