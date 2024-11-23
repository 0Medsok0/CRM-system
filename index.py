from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, pagination
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message
import logging
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'you mail'
app.config['MAIL_PASSWORD'] = 'you mail pass'
app.config['SECRET_KEY'] = 'your-secret-key'
mail = Mail(app)
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    region = db.Column(db.String(50), nullable=False)
    industry = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, phone, region, industry):
        self.name = name
        self.email = email
        self.phone = phone
        self.region = region
        self.industry = industry


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    region = StringField('Region', validators=[DataRequired(), Length(max=50)])
    industry = StringField('Industry', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Contact')


class ContactSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone', 'region', 'industry')


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        region = form.region.data
        industry = form.industry.data

        new_contact = Contact(name, email, phone, region, industry)

        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_contact.html', form=form)


@app.route('/contacts')
def contacts():
    page = request.args.get('page', 1, type=int)
    contacts = Contact.query.paginate(page=page, per_page=10)
    return render_template('contacts.html', contacts=contacts)


@app.route('/search_contacts', methods=['GET', 'POST'])
def search_contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        region = request.form['region']
        industry = request.form['industry']

        query = Contact.query

        if name:
            query = query.filter(Contact.name.ilike(f'%{name}%'))
        if email:
            query = query.filter(Contact.email.ilike(f'%{email}%'))
        if phone:
            query = query.filter(Contact.phone.ilike(f'%{phone}%'))
        if region:
            query = query.filter(Contact.region == region)
        if industry:
            query = query.filter(Contact.industry == industry)

        contacts = query.all()

        return render_template('contacts.html', contacts=contacts)

    return render_template('search_contacts.html')


@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        contact_id = request.form['contact_id']
        subject = request.form['subject']
        body = request.form['body']
        file = request.files['file']

        contact = Contact.query.get(contact_id)

        if not contact:
            return redirect(url_for('home'))

        msg = Message(subject, sender='--email--', recipients=[contact.email])
        msg.body = body

        if file:
            msg.attach(file.filename, file.read(), file.content_type)

        mail.send(msg)

        return redirect(url_for('home'))

    return render_template('send_email.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
