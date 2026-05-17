# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'raduga_energo_secret_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raduga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модели базы данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    work_hours = db.Column(db.String(200))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Новая')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Админ панель
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

admin = Admin(app, name='Радуга Энерго - Админ панель', index_view=MyAdminIndexView())
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(News, db.session))
admin.add_view(AdminModelView(Gallery, db.session))
admin.add_view(AdminModelView(Contact, db.session))
admin.add_view(AdminModelView(Request, db.session))

# Создаем таблицы БД при запуске
with app.app_context():
    db.create_all()
    # Создаем админа по умолчанию
    if not User.query.filter_by(email='admin@radugaenergo.ru').first():
        admin_user = User(
            name='Администратор',
            email='admin@radugaenergo.ru',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        
        contact = Contact(
            address='г. Радужный, квартал 9',
            phone='+7 (495) 123-45-67',
            email='info@radugaenergo.ru',
            work_hours='Пн-Пт: 8:00 - 17:00'
        )
        db.session.add(contact)
        
        db.session.commit()
    # Создаём демо-новости, если нет
    if not News.query.first():
        demo_news = [
            News(title='Запуск новой водонапорной станции',
                 content='Мы рады сообщить о завершении строительства и запуске новой современной водонапорной станции в г. Радужный. Станция оснащена оборудованием последнего поколения, что позволит обеспечить бесперебойную подачу воды для 5000 жителей. Проект реализован в рамках программы модернизации системы водоснабжения региона.',
                 image='images/news_photo.png',
                 created_at=datetime(2026, 5, 10)),
            News(title='Модернизация системы водоснабжения',
                 content='Компания «Радуга Энерго» завершила плановую модернизацию системы водоснабжения в северном микрорайоне. Были заменены магистральные трубопроводы общей протяжённостью 2,5 км, установлены современные системы фильтрации и автоматики. Жители микрорайона отметили значительное улучшение качества воды.',
                 image='images/news_photo.png',
                 created_at=datetime(2026, 4, 25)),
            News(title='Наши специалисты прошли сертификацию',
                 content='Вся команда инженеров «Радуга Энерго» успешно прошла ежегодную сертификацию и повышение квалификации. Наши специалисты освоили новые технологии монтажа и обслуживания систем водоснабжения, что позволит нам предлагать клиентам ещё более качественные услуги.',
                 image='images/news_photo.png',
                 created_at=datetime(2026, 4, 10)),
            News(title='График отключения воды на май 2026',
                 content='Публикуем плановый график профилактических работ и отключения водоснабжения на май 2026 года. Работы будут проводиться в соответствии с требованиями Роспотребнадзора для обеспечения санитарной безопасности. Приносим извинения за временные неудобства.',
                 image='images/news_photo.png',
                 created_at=datetime(2026, 4, 1)),
            News(title='Экологическая акция «Чистая вода»',
                 content='Компания «Радуга Энерго» выступила спонсором городской экологической акции «Чистая вода». В рамках акции были очищены берега городского озера, высажены молодые деревья, а также проведены образовательные лекции о важности сохранения водных ресурсов для школьников.',
                 image='images/news_photo.png',
                 created_at=datetime(2026, 3, 15)),
            News(title='Новые тарифы на водоснабжение с 1 апреля',
                 content='С 1 апреля 2026 года вступают в силу новые тарифы на холодное и горячее водоснабжение. Тарифы утверждены региональной энергетической комиссией и проиндексированы на уровень инфляции. Актуальные тарифы: холодная вода — 42,30 ₽/м³, горячая вода — 198,50 ₽/м³.',
                 image='images/news_photo.png',
                 created_at=datetime(2026, 3, 1))
        ]
        for n in demo_news:
            db.session.add(n)
        db.session.commit()
        print("OK: Демо-новости созданы")
    
    contact = Contact.query.first()
    if contact:
        contact.address = 'г. Радужный, квартал 9'
        contact.work_hours = 'Пн-Пт: 8:00 - 17:00'
        db.session.commit()
        print("OK: Контакты обновлены")
    print("OK: База данных инициализирована")

# Маршруты сайта
@app.route('/')
def index():
    news = News.query.order_by(News.created_at.desc()).limit(3).all()
    return render_template('index.html', news=news)

@app.route('/about')
def about():
    gallery = Gallery.query.all()
    return render_template('about.html', gallery=gallery)

@app.route('/news')
def news():
    news = News.query.order_by(News.created_at.desc()).all()
    return render_template('news.html', news=news)

@app.route('/news/<int:id>')
def news_single(id):
    news = News.query.get_or_404(id)
    return render_template('news_single.html', news=news)

@app.route('/contacts')
def contacts():
    contact = Contact.query.first()
    return render_template('contacts.html', contact=contact)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Неверный логин или пароль')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует')
            return redirect(url_for('register'))
        
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    requests = Request.query.filter_by(user_id=current_user.id).order_by(Request.created_at.desc()).all()
    return render_template('dashboard.html', requests=requests)

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/send_request', methods=['POST'])
def send_request():
    data = request.get_json()
    new_request = Request(
        user_id=current_user.id if current_user.is_authenticated else None,
        name=data['name'],
        phone=data['phone'],
        email=data.get('email', ''),
        message=data.get('message', '')
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("\n=== SITE RADUGA ENERGO STARTED ===")
    print("Website:      http://localhost:5000")
    print("Admin panel:  http://localhost:5000/admin")
    print("Admin login:  admin@radugaenergo.ru")
    print("Admin pass:   admin123")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
