from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


# 异步发送邮件，第三方服务器比较耗时
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


# python标准库有提供email的模块，但是比较复杂，
# flask给我们提供了一个插件，flask-email，要注册到app上
def send_mail(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='1207656050@qq.com', body='test', recipients=['1207656050@qq.com'])
    msg = Message('[鱼书]'+' '+subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()  # 拿到真实的flask app对象
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()

