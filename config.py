import os


# 使用类存储配置变量
class Config:
    # SECRET_KEY 这个配置变量，会被FLASK及其扩展使用其值作为加密密钥，用于生产签名或令牌，Flask-wtf使用它来保护Web表单免受CSFR攻击
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'