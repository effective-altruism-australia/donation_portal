"""donation_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from donation.views import upload_donations_file, accounting_reconciliation, download_transactions, donation_counter

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload_donations', upload_donations_file, name='upload-donations-file'),
    url(r'^accounting_reconciliation', accounting_reconciliation, name='accounting-reconciliation'),
    url(r'^secret_donation_counter', donation_counter, name='donation_counter'),
    url(r'^download_transactions', download_transactions, name='download-transactions'),
]
