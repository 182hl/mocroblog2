from app import app,db
from app.model import User,Post

#shell上下文处理，无需每次在shell中做一些重复的导入
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}
if __name__ == '__main__':
    app.run(debug=True)