# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.template.loader import render_to_string

# import os

# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

# from weasyprint import HTML

# def html_to_pdf_view(request):
#     paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
#     html_string = render_to_string('core/pdf_template.html', {'paragraphs': paragraphs})

#     html = HTML(string=html_string)
#     html.write_pdf(target='/tmp/mypdf.pdf');

#     fs = FileSystemStorage('/tmp')
#     with fs.open('mypdf.pdf') as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
#         return response

#     return response