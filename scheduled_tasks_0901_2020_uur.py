# 代码生成时间: 2025-09-01 20:20:10
from django.utils import timezone
from django.db import models
from django.http import JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
# 扩展功能模块
logger = logging.getLogger(__name__)

class Task(models.Model):
    """Model to store scheduled tasks."""
    name = models.CharField(max_length=200, unique=True, help_text="Name of the task")
    interval_seconds = models.IntegerField(help_text="Task interval in seconds")
    last_run = models.DateTimeField(null=True, blank=True, help_text="Last time the task was run")

    def __str__(self):
        return self.name

    def schedule(self):
        """Schedules the task to run at an interval."""
        trigger = IntervalTrigger(seconds=self.interval_seconds)
# 增强安全性
        scheduler.add_job(self.run, trigger)
        logger.info(f"Task {self.name} scheduled to run every {self.interval_seconds} seconds.")

    def run(self):
        """Run the task."""
        self.last_run = timezone.now()
        self.save()
        logger.info(f"Task {self.name} executed at {self.last_run}.")
# 优化算法效率


class ScheduledTasksApp:
    """Application component for scheduled tasks."""
# FIXME: 处理边界情况
    def __init__(self):
# FIXME: 处理边界情况
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Scheduler started.")

    def schedule_all_tasks(self):
        """Schedule all tasks from the database."""
        tasks = Task.objects.all()
# TODO: 优化性能
        for task in tasks:
            task.schedule()

    def stop_scheduler(self):
        """Stop the scheduler."""
        self.scheduler.shutdown(wait=False)
        logger.info("Scheduler shutdown.")

    def add_task(self, name, interval_seconds):
        """Add a new task to the database and schedule it."""
        try:
            task = Task.objects.create(name=name, interval_seconds=interval_seconds)
            task.schedule()
            return JsonResponse({'status': 'success', 'message': f'Task {name} added and scheduled.'})
        except Exception as e:
            logger.error(f'Failed to add task {name}: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)})
# 优化算法效率

    def remove_task(self, task_id):
        "