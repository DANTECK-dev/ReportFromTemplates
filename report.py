from docxtpl import DocxTemplate

def generate_report(report_type, content, user_data):
    template = DocxTemplate(f"templates/{report_type}.docx")
    context = { 'content': content, 'user': user_data }
    template.render(context)
    file_path = f"reports/{report_type}_report_{user_data['student_name']}.docx"
    template.save(file_path)
    return file_path
