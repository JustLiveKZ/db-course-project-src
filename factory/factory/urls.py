from django.conf.urls import patterns, url

from views import HomeView, PurchaseView, ManufactureView, SaleView, ProductPartialView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^purchase/$', PurchaseView.as_view(), name='purchase'),
    url(r'^product/(?P<pk>\d+)/$', ProductPartialView.as_view(), name='product'),
    url(r'^manufacture/$', ManufactureView.as_view(), name='manufacture'),
    url(r'^sale/$', SaleView.as_view(), name='sale'),
)