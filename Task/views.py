from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)

from .forms import TaskForm
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer



@login_required
def HomeView(request):
    now = timezone.now()

    today_start = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    today_end = now.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )

    user_tasks = Task.objects.filter(user=request.user)

    today_deadlines = user_tasks.filter(
        deadline__range=(today_start, today_end)
    )

    context = {
        "total_tasks": user_tasks.count(),
        "new_tasks_count": user_tasks.filter(status="new").count(),
        "progress_tasks_count": user_tasks.filter(
            status="in-progress"
        ).count(),
        "completed_tasks_count": user_tasks.filter(
            status="done"
        ).count(),
        "today_deadlines": today_deadlines,
    }

    return render(request, "task/home.html", context)


@login_required
def TaskListView(request):
    tasks = Task.objects.filter(
        user=request.user
    ).order_by("deadline")

    search_input = request.GET.get("search-area", "").strip()

    if search_input:
        tasks = tasks.filter(
            title__icontains=search_input
        )

    status_filter = request.GET.get("status", "all")

    if status_filter in ["new", "in-progress", "done"]:
        tasks = tasks.filter(status=status_filter)

    context = {
        "tasks": tasks,
        "search_input": search_input,
        "status_filter": status_filter,
    }

    return render(
        request,
        "task/task_list.html",
        context,
    )


@login_required
def change_status(request, task_id, new_status):
    if new_status not in ["new", "in-progress", "done"]:
        messages.error(request, "Noto'g'ri status!")
        return redirect(
            request.META.get("HTTP_REFERER", "task_list")
        )

    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.status = new_status
    task.save(update_fields=["status"])

    return redirect(
        request.META.get("HTTP_REFERER", "task_list")
    )


@login_required
def TaskCreateView(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.status = "new"
            task.save()

            messages.success(
                request,
                "Vazifa muvaffaqiyatli yaratildi."
            )

            return redirect("task_list")
    else:
        form = TaskForm()

    return render(
        request,
        "task/task_form.html",
        {
            "form": form,
            "is_edit": False,
        },
    )


@login_required
def TaskUpdateView(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Vazifa yangilandi."
            )

            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "task/task_form.html",
        {
            "form": form,
            "is_edit": True,
        },
    )


@login_required
def ProfileView(request):
    tasks = Task.objects.filter(
        user=request.user
    )

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        status="done"
    ).count()

    progress_percentage = (
        int(completed_tasks / total_tasks * 100)
        if total_tasks
        else 0
    )

    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress_percentage": progress_percentage,
    }

    return render(
        request,
        "task/profile.html",
        context,
    )


def RegisterView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!"
            )

            return redirect("login")
    else:
        form = UserCreationForm()

    return render(
        request,
        "task/register.html",
        {
            "form": form
        }
    )


# ---------------- API ----------------

class RegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(
            request,
            *args,
            **kwargs
        )

        user = User.objects.get(
            username=response.data["username"] # type: ignore
        )

        token, _ = Token.objects.get_or_create(
            user=user
        )

        response.data["token"] = token.key # type: ignore

        return response


class LoginAPIView(ObtainAuthToken):
    permission_classes = [AllowAny]


class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Task.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class TaskRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    serializer_class = TaskSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Task.objects.filter(
            user=self.request.user
        )


class TaskStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    VALID_STATUSES = [
        "new",
        "in-progress",
        "done",
    ]

    def patch(self, request, id):
        task = get_object_or_404(
            Task,
            id=id,
            user=request.user
        )

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {
                    "error":
                    "Status maydoni yuborilmadi!"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_status not in self.VALID_STATUSES:
            return Response(
                {
                    "error":
                    "Noto'g'ri status qiymati!"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = new_status
        task.save(update_fields=["status"])

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK,
        )