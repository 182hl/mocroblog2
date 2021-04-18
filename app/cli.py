import click

from app import app
import os


#命令的名称来自装饰器函数的命令，并且帮助消息来自docstring（文档字符串）。由于这是存在为子命令提供一个基础的父命令，因此这个函数本身不需要执行任何操作
@app.cli.group()
def translate():
    #翻译和本地化命令
   pass

#translate装饰器  更新命令
@translate.command()
def update():
    #更新所有语言
    #相当于在终端输入命令执行
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

#编译所有语言
@translate.command()
def compile():
    #编译所有语言
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

#初始化命令
@translate.command()
@click.argument('lang')
def init(lang):
    #初始化一个新语言
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations -l '+lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')

