import csv
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from .models import TradeReport
from .serializers import TradeReportSerializer

class TradeReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TradeReport.objects.all()
    serializer_class = TradeReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="trade_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['User', 'Created At', 'Trading Volume', 'Revenue', 'Profit/Loss'])

        for report in TradeReport.objects.all():
            writer.writerow([report.user.username, report.created_at, report.total_trading_volume, report.total_revenue, report.profit_loss])

        return response

    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="trade_report.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, "Trade Report")

        y = 780
        for report in TradeReport.objects.all():
            text = f"{report.user.username} | {report.created_at} | {report.total_trading_volume} | {report.total_revenue} | {report.profit_loss}"
            p.drawString(100, y, text)
            y -= 20

        p.showPage()
        p.save()
        return response
