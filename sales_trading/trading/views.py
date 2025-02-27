from rest_framework import viewsets, permissions
from .models import Order, Trade
from .serializers import OrderSerializer, TradeSerializer
from customauth.permissions import IsAdminRole, IsAdminOrTrader, IsSales, IsTrader
from .tasks import send_trade_notification

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']: 
            permission_classes = [IsAdminOrTrader]
        elif self.action in ['create', 'update', 'partial_update']: 
            permission_classes = [IsTrader]
        elif self.action in ['destroy']: 
            permission_classes = [IsAdminRole]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAdminRole | IsSales]
    
    def perform_create(self, serializer):
        trade = serializer.save()
        send_trade_notification.delay(trade.buy_order.user.email, trade.id, trade.price, trade.quantity)
        send_trade_notification.delay(trade.sell_order.user.email, trade.id, trade.price, trade.quantity)
