from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import SalesOrder, Invoice, Discount
from .serializers import SalesOrderSerializer, InvoiceSerializer, DiscountSerializer
from customauth.permissions import IsSales, IsAdminRole
from rest_framework.decorators import action

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsSales()]
        if self.action in ['approve_order', 'reject_order']:  
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        total_price = product.price * quantity
        serializer.save(user=self.request.user, total_price=total_price, status='pending')

    @action(detail=True, methods=['post'])
    def approve_order(self, request, pk=None):
        order = self.get_object()
        order.status = 'approved'
        order.save()
        return Response({'message': 'Order approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject_order(self, request, pk=None):
        order = self.get_object()
        order.status = 'rejected'
        order.save()
        return Response({'message': 'Order rejected'}, status=status.HTTP_200_OK)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminRole | IsSales]

    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        order = get_object_or_404(SalesOrder, pk=pk)

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 750, f"Invoice for Order {order.id}")
        pdf.drawString(100, 730, f"Customer: {order.user.username}")
        pdf.drawString(100, 710, f"Total Price: {order.total_price} KZT")
        pdf.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'invoice_{order.id}.pdf')


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminRole]
