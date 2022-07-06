from rest_framework import permissions

from project_management.models import Contributor, Project




class IsCreator(permissions.BasePermission):
    # message = 'nononon !!!!!!'

    def has_object_permission(self, request, view, obj):

        contributor = Contributor.objects.filter(user=request.user, project=obj).first()
        print(contributor)

        if request.method == 'GET' and contributor:
            return True

        elif (request.method == 'PUT' or request.method == 'DELETE') and contributor.permission == Contributor.Role.CREATOR:
            return True

        else:
            return False


    def has_permission(self, request, view):


        print(f'nuirasetrnauisee ------ {request.method}')
        print(f'−−−−−−−−−−−−−−−−−−− {request.data}')

        match request.method:

            case 'GET':

                return True

            case 'POST':
                
                return True

            case 'PUT':
                return True


        return True
