import csv
import datetime

from django.core.exceptions import FieldDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import classonlymethod
from django.views import View
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django_filters.views import BaseFilterView, FilterView


class ReportAsCSVMixin(TemplateView):
    csv_filename = 'data'
    report_fields = []
    field_labels = {}
    __csv_fields = None


    def export_csv(self, request, *args, **kwargs):

        now = datetime.datetime.now()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}_{}.csv'.format(self.csv_filename, now.strftime('%Y%m%d'))

        response.write(u'\ufeff'.encode('utf-8'))
        writer = csv.writer(response, dialect='excel', delimiter=str(';'), quotechar=str('"'))

        filter_list = self.available_fields

        final_fields = []
        header_row = []

        for field in filter_list:
            if field in self.__csv_fields:
                header_row.append(self.__csv_fields[field])
                final_fields.append(field)

        writer.writerow(header_row)

        for elem in self.object_list:
            results = []
            for field in final_fields:
                value = getattr(elem, field)
                value = str(value).strip() if value else ''
                results.append( value )
            writer.writerow(results)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


    def get(self, request, *args, **kwargs):

        if self.request.is_ajax():
            return JsonResponse(self.get_context_data())

        if request.GET.get('export','') == 'csv':
            if 'o' in request.GET:
                request.GET = request.GET.copy()
                del request.GET['o']

            return self.export_csv(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)