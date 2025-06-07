from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

def create_congratulation_pdf(user_data, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        name='RussianTitle',
        parent=styles['Title'],
        fontName='Arial', 
        fontSize=16,
        leading=24,
        spaceAfter=24
    )
    
    greeting_style = ParagraphStyle(
        name='RussianGreeting',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=14,
        leading=20,
        spaceAfter=0
    )
    
    middle_name = user_data.get('middle_name', '')
    full_name = f"{user_data['last_name']} {user_data['first_name']} {middle_name}".strip()
    
    content = []
    content.append(Paragraph("Поздравление с Днем Рождения!", title_style))
    content.append(Spacer(1, 24))
    
    greeting_text = (
        f"Уважаемый(ая) {full_name}!<br/><br/>"
        "От имени руководства и всего коллектива "
        "сердечно поздравляем Вас с Днём Рождения!<br/><br/>"
        "Желаем здоровья, счастья и профессиональных успехов!<br/><br/>"
        "С уважением,<br/>"
        "Ректор Института<br/>"
        "А.И. Петров"
    )
    
    content.append(Paragraph(greeting_text, greeting_style))
    
    doc.build(content)
    print(f"PDF создан: {os.path.abspath(output_path)}")
    
test_user = {
    'last_name': 'Иванов',
    'first_name': 'Иван',
    'middle_name': 'Иванович',
    'birth_date': '1990-05-15',
    'city': 'Москва',
    'email': 'test@example.com',
    'telegram_id': '@ivanov',
    'vk_link': 'https://vk.com/ivanov'
}

create_congratulation_pdf(test_user, "test.pdf")