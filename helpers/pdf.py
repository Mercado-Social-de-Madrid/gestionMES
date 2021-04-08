from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration


def render_pdf_response(request, pdf_template, context_params, filename='temp'):
    html_string = render_to_string(pdf_template, context_params)
    #return HttpResponse(html_string)

    font_config = FontConfiguration()
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{filename}.pdf"'.format(filename=filename)

    html.write_pdf(response, font_config=font_config)

    return response
