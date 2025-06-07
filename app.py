import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

def get_db_config():
    return {
        'host': os.getenv('MYSQL_HOST'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DB'),
        'auth_plugin': 'mysql_native_password' 
    }

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            conn = mysql.connector.connect(**get_db_config())
            cursor = conn.cursor()
            
            sql = """
            INSERT INTO users (
                city, 
                birth_date, 
                last_name, 
                first_name, 
                middle_name, 
                email, 
                telegram_id, 
                vk_link
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            data = (
                form.city.data,
                form.birth_date.data,
                form.last_name.data,
                form.first_name.data,
                form.middle_name.data or None,  
                form.email.data,
                form.telegram_id.data,
                form.vk_link.data
            )
            
            cursor.execute(sql, data)
            conn.commit()
            
            flash('✅ Данные успешно сохранены!', 'success')
            return redirect(url_for('register'))
            
        except mysql.connector.Error as err:
            flash(f'❌ Ошибка базы данных: {err}', 'danger')
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)