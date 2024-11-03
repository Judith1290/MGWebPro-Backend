from io import BytesIO

from django.template.loader import get_template
from xhtml2pdf import pisa


# crea un pdf a partir de una template
def create_pdf(template, context):
    template = get_template(template)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None
