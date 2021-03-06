# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from students.models import Student
from courses.models import Course
from students.forms import StudentModelForm

import logging
logger = logging.getLogger(__name__)

class SrudentListView(ListView):
    model = Student
    paginate_by = 2
    #context_object_name = 'students'
    #template_name = 'students/list_view.html'

    def get_queryset(self):
        course_id = self.request.GET.get('course_id',None)

        if course_id:
            students = Student.objects.filter(courses__id=course_id)
        else:
            students = Student.objects.all()    
        return students



class StudentDetailView(DetailView):
    model = Student
    
    def get_context_data(self, **kwargs):
        logger.debug("Students detail view has been debugged")
        logger.info("Logger of students detail view informs you!")
        logger.warning("Logger of students detail view warns you!")
        logger.error("Students detail view went wrong!")
        student = self.get_object()
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['title'] = u"Student %s %s detail" % (student.name, student.surname)
        return context





class StudentCreateView(CreateView):
    model = Student
    success_url = reverse_lazy('students:list_view')

    def form_valid(self, form):
        message = super(StudentCreateView, self).form_valid(form)
        messages.success(self.request, u"Student %s %s has been successfully added."
                         % (self.object.name, self.object.surname))
        return message

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        context['title'] = "Student registration"
        return context    


class StudentUpdateView(UpdateView):
    model = Student
    success_url = reverse_lazy('students:list_view')
    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Student info update"
        return context

    def form_valid(self, form):
        message = super(StudentUpdateView, self).form_valid(form)
        messages.success(self.request, u"Student %s %s has been successfully updated."
                         % (self.object.name, self.object.surname))
        return message    

class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list_view')

    def get_context_data(self, **kwargs):
        context = super(StudentDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Student info suppression"
        return context

    def delete(self, request, pk):
        student = self.get_object()
        message =  u"Info on %s %s has been sucessfully deleted." % (student.name, student.surname)
        student.delete()
        messages.success(self.request, message)
        return redirect('students:list_view')



