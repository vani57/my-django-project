# records/views/base.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q # Q is used for complex queries
from django.core.paginator import Paginator
import json
from django.db.models import CharField, TextField, IntegerField, FloatField


class BaseModelView(APIView):
    model = None
    serializer_class = None
    pagination_page_size = 10

    def get_model_fields(self):
        return [f.name for f in self.model._meta.get_fields()] # Returns a list of field names for the model

    def get_queryset(self):
        queryset = self.model.objects.all()
        params = self.request.query_params
        
        if params.get("filters"):
            queryset = self.apply_filtering(queryset, params)

        if params.get("search"):
            queryset = self.apply_searching(queryset, params)
            
        if params.get("ordering"):
            queryset = self.apply_ordering(queryset, params)
        return queryset
    
    

    def apply_filtering(self, queryset, params):
        filters_json = params.get("filters")
        model_fields = self.get_model_fields() 

        if filters_json:
            try:
                filters_dict = json.loads(filters_json)
                for key, value in filters_dict.items():
                    if key in model_fields:
                        try:
                            queryset = queryset.filter({key: value}) #filter({key: value}) applies the filter to the queryset
                        except Exception:
                            pass  # Optionally log the error
            except json.JSONDecodeError:
                pass  # Optionally log invalid JSON

        return queryset

    def apply_searching(self, queryset, params):
        search_term = params.get('search') # Get the search term from query parameters
        if not search_term:
            return queryset

        q = Q() # Initialize an empty Q object for complex queries
        for field in self.model._meta.get_fields():
            if not hasattr(field, 'get_internal_type'): # Check if the field has a get_internal_type method
                continue

            field_name = field.name
            field_type = field.get_internal_type()

            try:
                if field_type in ['CharField', 'TextField']:
                    q |= Q({f"{field_name}__icontains": search_term})
                elif field_type == 'IntegerField' and search_term.isdigit():
                    q |= Q({field_name: int(search_term)})
            except:
                continue

        return queryset.filter(q) 

    def apply_ordering(self, queryset, params):
        order_field = params.get('ordering')
        model_fields = self.get_model_fields()

        if order_field:
            clean_field = order_field.lstrip('-')
            if clean_field in model_fields:
                return queryset.order_by(order_field)

        return queryset  # return as-is if no valid ordering param

    

    def paginate_queryset(self, queryset):
        page = int(self.request.query_params.get('page', 1))
        page_size = int(self.request.query_params.get('page_size', self.pagination_page_size))

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page) # Get the page object for the requested page(get_page())

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'results': page_obj.object_list
        }
    
   

    '''def get(self, request):
        queryset = self.get_queryset()
        paginated = self.paginate_queryset(queryset)
        serializer = self.serializer_class(paginated['results'], many=True)

        return Response({
            'count': paginated['count'],
            'total_pages': paginated['total_pages'],
            'current_page': paginated['current_page'],
            'results': serializer.data
        })'''
    
    def get(self, request, id=None):
        queryset = self.get_queryset()

        if id is not None:
            # Fetch single record by ID
            instance = get_object_or_404(queryset, id=id)
            serializer = self.serializer_class(instance)
            return Response(serializer.data) 

        # Fetch all records
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
      

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=id)
            instance.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)