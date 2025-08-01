# 代码生成时间: 2025-08-02 00:06:20
import bottle
import sqlite3
from bottle import run, request, response, template
from contextlib import closing

# 数据库迁移工具的配置信息
DB_NAME = 'migration.db'
MIGRATION_DIR = 'migrations'

# 用于存放迁移文件的列表
migrations = []

bottle.TEMPLATE_PATH.insert(0, 'views')

# 获取数据库连接
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 运行迁移文件
def run_migrations():
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        # 检查迁移记录表是否存在
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS migrations
            (id INTEGER PRIMARY KEY, name TEXT NOT NULL)
        ''')
        conn.commit()
        # 读取所有迁移文件
        for filename in sorted(migration_files(MIGRATION_DIR)):
            migration_name = filename.split('.')[0]
            # 检查是否已迁移
            if not has_migrated(migration_name, cursor):
                with open(os.path.join(MIGRATION_DIR, filename), 'r') as f:
                    cursor.executescript(f.read())
                cursor.execute('INSERT INTO migrations (name) VALUES (?)', (migration_name,))
                conn.commit()

# 检查是否已迁移
def has_migrated(name, cursor):
    cursor.execute('SELECT id FROM migrations WHERE name=?', (name,))
    return cursor.fetchone() is not None

# 获取所有迁移文件
def migration_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.sql') and f[0] != '.']

# 迁移路由
@bottle.route('/migrate', method='GET')
def migrate():
    try:
        run_migrations()
        return template('migrate_success', message='Migrations completed successfully.')
    except Exception as e:
        return template('migrate_error', error=str(e))

# 启动应用
if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)
