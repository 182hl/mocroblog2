from app import create_app,db
from app.auth.routes import register
from app.model import User,Post
from app import cli
from config import Config


app = create_app(Config)
cli.register(app)

#shell上下文处理，无需每次在shell中做一些重复的导入
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}
if __name__ == '__main__':
    app.run(debug=True)
    # centos-7-x86_64-Minimal-1611