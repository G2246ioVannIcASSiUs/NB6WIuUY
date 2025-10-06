# 代码生成时间: 2025-10-06 20:48:44
{
  """
  Net Security Monitor Django app component
  """
  
  from django.db import models
  from django.shortcuts import render
  from django.http import HttpResponse, Http404
  from django.urls import path
  from django.views import View
  from django.utils import timezone
  from datetime import datetime
  
  class SecurityIncident(models.Model):
      """
      A model to represent a security incident.
      """
      title = models.CharField(max_length=200)
      description = models.TextField()
      timestamp = models.DateTimeField(default=timezone.now)
      
      def __str__(self):
          return self.title
  
  class SecurityIncidentListView(View):
      """
      A view to display a list of security incidents.
      """
      def get(self, request):
          incidents = SecurityIncident.objects.all().order_by('-timestamp')
          return render(request, 'net_security_monitor/incident_list.html', {'incidents': incidents})
  
  class SecurityIncidentDetailView(View):
      """
      A view to display a single security incident.
      """
      def get(self, request, incident_id):
          try:
              incident = SecurityIncident.objects.get(pk=incident_id)
          except SecurityIncident.DoesNotExist:
              raise Http404("Incident does not exist")
          return render(request, 'net_security_monitor/incident_detail.html', {'incident': incident})
  
  def error_404_view(request, exception):
      """
      A custom 404 error handler.
      """
      return render(request, 'net_security_monitor/404.html', {}, status=404)
  
  urlpatterns = [
      path('incidents/', SecurityIncidentListView.as_view(), name='incident_list'),
      path('incidents/<int:incident_id>/', SecurityIncidentDetailView.as_view(), name='incident_detail'),
  ]
}
