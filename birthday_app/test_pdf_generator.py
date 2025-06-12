from pdf_generator import create_congratulation_pdf

test_user = {
    'id': 1,
    'last_name': 'Тестов',
    'first_name': 'Тест',
    'middle_name': 'Тестович',
    'city': 'Москва',
    'birth_date': '1990-01-01',
    'email': 'test@test.com',
    'telegram_id': '@test_user',
    'vk_link': 'https://vk.com/test'
}

create_congratulation_pdf(test_user, "test_output.pdf")
print("PDF создан. Проверьте визуально: test_output.pdf")