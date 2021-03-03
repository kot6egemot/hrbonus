from django.http import JsonResponse
from rest_framework.views import APIView

filters = {
    "Year": {
        "component_name": "YearFilter",
        "state": ""
    },
    "Month": {
        "component_name": "MonthFilter",
        "state": ""
    }
}

navigation = [{
    "title": "Премирование",
    "icon": "mdi-account-multiple",
    "entity": "bonus",
    "is_paginate": True,
    "is_search": True,
    "filters": filters,
    "items_per_page_options": [100, 200, 300, 400],
    "actions": {
        "add": False,
        "delete": False
    }
},
    {
        "title": "План-Факт",
        "icon": "mdi-city",
        "entity": "line",
        "is_paginate": False,
        "is_search": False,
        "filters": filters,
        "items_per_page_options": [10, 20, 30],
        "actions": {
            "add": False,
            "delete": False
        }
    },
    {
        "title": "Константы",
        "icon": "mdi-cog",
        "entity": "constant",
        "is_paginate": True,
        "is_search": False,
        "filters": filters,
        "items_per_page_options": [10, 20, 30],
        "actions": {
            "add": False,
            "delete": False
        }
    },
    {
        "title": "Индивидуальные изменения",
        "icon": "mdi-account-cog",
        "entity": "individual_change",
        "is_paginate": True,
        "is_search": True,
        "filters": filters,
        "items_per_page_options": [10, 20, 30, 40],
        "actions": {
            "add": True,
            "delete": True
        }
    },
    {
        "title": "Выгрузка данных",
        "icon": "mdi-download",
        "entity": "csv_upload"
    },
    {
        "title": "Пользователи",
        "icon": "mdi-download",
        "entity": "users"
    }
]


class NavigationView(APIView):

    def get(self, request):
        return JsonResponse({"result": True, "navigation_links": navigation})
