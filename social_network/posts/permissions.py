from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAuthenticatedOrSafe(BasePermission):
    """
    Пользовательское разрешение (Custom permission), которое разрешает доступ
    к созданию объекта (публикации или комментарию) всем авторизованным
    пользователям, к изменению или удалению - только его автору, а к чтению
    (и др. "безопасным методам") - без ограничений
    """
    def has_object_permission(self, request, view, obj):
        #GET, HEAD и OPTIONS - все пользователи
        if request.method in SAFE_METHODS:
            return True
        #PATCH и DELETE - автор поста/комментария
        elif request.method in ('PATCH', 'DELETE',):
            edit_permission = False
            try:
                edit_permission = obj.owner == request.user
            except:
                pass
            try:
                edit_permission = obj.author == request.user
            except:
                pass
            return edit_permission
        #CREATE - авторизованные пользователи
        elif (request.method == 'CREATE') and request.user and request.user.is_authenticated:
            return True
        #Все остальные случаи, в том числе:
        #для не указанных здесь в явном виде запросов по умолчанию ДОСТУП ЗАПРЕЩЁН
        else:
            return False