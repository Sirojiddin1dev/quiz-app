from django.contrib import admin
from .models import Category,Task,Taskusers
from customusers.models import CustomUser
from django.contrib.auth.models import Group

admin.site.unregister(Group)




@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "gender", "phone_number", "test_access", "certificate", "passed", "country", "created_at")
    list_filter = ('phone_number', 'gender', 'country')
    list_editable = ('test_access', "certificate", 'passed') 
    
    # save_as = True
    # save_on_top = True
    # change_list_template = 'change_list_graph.html'



@admin.register(Taskusers)
class TaskusersAdmin(admin.ModelAdmin):
    list_display = ("username", "all", "attempts", "result1", "result2", "final_result","date")
    list_filter = ("checking", "checking2", "username", "attempts")

    @admin.display(description="Result 1-2-Modul")
    def result1(self, obj):
        total_task_1 = 26  # or use obj.category.count_task if it is dynamically determined
        natija1 = obj.natija1 or 0
        procent1 = round((natija1 / 26) * 100, 2) if total_task_1 else 0
        return f"{procent1}%"

    @admin.display(description="Result 3-Modul")
    def result2(self, obj):
        total_task_2 = 65  # or use obj.category.count_task if it is dynamically determined
        natija2 = obj.natija2 or 0
        procent2 = round((natija2 / 65) * 100, 2) if total_task_2 else 0
        return f"{procent2}%"

    @admin.display(description="Final Result")
    def final_result(self, obj):
        total_task_1 = 26  # or use obj.category.count_task if it is dynamically determined
        total_task_2 = 65  # or use obj.category.count_task if it is dynamically determined
        natija1 = obj.natija1 or 0
        natija2 = obj.natija2 or 0
        procent1 = round((natija1 / total_task_1) * 100, 2) if total_task_1 else 0
        procent2 = round((natija2 / total_task_2) * 100, 2) if total_task_2 else 0
        combined_percentage = (procent1 + procent2) / 2
        if combined_percentage >= 60:
            return "✅ Success"
        else:
            return "❌ Failed"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ( "title","category",)
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title","count_task","timer","is_active")
    list_editable = ("count_task","is_active")
