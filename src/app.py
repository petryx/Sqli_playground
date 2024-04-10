from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
    c.execute('INSERT INTO tasks (task) VALUES (?)', ('Corrigir o prj x1',))
    c.execute('INSERT INTO tasks (task) VALUES (?)', ('Validar a implementação da tabela secret com a coluna secret',))
    c.execute('INSERT INTO tasks (task) VALUES (?)', ('Melhorar o código linha 2',))
    c.execute('INSERT INTO tasks (task) VALUES (?)', ('Validar se a app é vulnerável a SQLi',))
    c.execute('INSERT INTO tasks (task) VALUES (?)', ('Implementar Authenticação',))
    c.execute('INSERT INTO tasks (task) VALUES (?)', ('Implementar Autorização',))
    c.execute('INSERT INTO tasks (task) VALUES (?)', ('Automatizar o deploy',))
    
    c.execute('''CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, secret TEXT)''')
    c.execute('INSERT INTO secrets (secret) VALUES (?)', ('API_KEY: 923hjfbn74fjf940rffu888',))
    c.execute('INSERT INTO secrets (secret) VALUES (?)', ('root:VouAnotarEssaSenha2024',))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<string:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
        
    if request.method == 'POST':
        task = request.form['task']
        c.execute('UPDATE tasks SET task = ? WHERE id = ?', (task, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    try:
        # Adding this line to prevent SQLi, cast the task_id to int
        task_id_int = int(task_id)
    except:
        return 'Invalid task id'

    c.execute(f'SELECT * FROM tasks WHERE id = {task_id}')
    task = c.fetchone()
    conn.close()
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    create_database()
    app.run(debug=True,host='0.0.0.0')