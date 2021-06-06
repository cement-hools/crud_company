from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CompanyViewSet

company_router = DefaultRouter()
company_router.register('companies', CompanyViewSet, basename='companies')

# transaction_router = DefaultRouter()
# transaction_router.register('transactions', WalletTransactionViewSet,
#                             basename='transactions')

# transactions_all_router = DefaultRouter()
# transactions_all_router.register('transactions', UserTransactionViewSet,
#                                  basename='user_transactions')

urlpatterns = [

    path('v1/', include(company_router.urls)),
    # path('v2/all/', include(transactions_all_router.urls)),
    # path('v2/wallets/<int:wallet_id>/', include(transaction_router.urls)),

]
