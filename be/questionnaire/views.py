from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from be.responses import response_200, response_400, response_500
from questionnaire.models import Category, Field, VotedField
from questionnaire.request_utils import check_add_category_request, check_add_field_request
from questionnaire.serializers import MyFieldSerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_category(request):
    if not request.user.is_superuser:
        return response_400("you can't create category")

    if not check_add_category_request(request.data):
        return response_400("bad request")

    category_name = request.data.get("category_name")

    category_max_field = request.data.get("max_field")

    category_started_at = request.data.get("started_at")

    category_ended_at = request.data.get("ended_at")
    try:
        Category.objects.get(name=category_name)
        return response_400("this category is already exist")
    except ObjectDoesNotExist as e:
        Category.objects.create(
            name=category_name,
            max_field=category_max_field,
            started_at=category_started_at,
            ended_at=category_ended_at
        )

    return response_200("success", None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_field(request):
    if not request.user.is_superuser:
        return response_400("you can't create category")

    if not check_add_field_request(request.data):
        return response_400("bad request")

    category_name = request.data.get("category_name")

    try:
        my_category = Category.objects.get(name=category_name)
    except ObjectDoesNotExist as e:
        return response_400("this category is not valid, please firstly create new category")

    if my_category.current_field >= my_category.max_field:
        return response_400("you can't add this field")
    field_name = request.data.get("field_name")

    field_image = request.data.get("image")

    Field.objects.create(
        category=my_category,
        name=field_name,
        image=field_image
    )

    return response_200("success", None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def edit_category(request):
    if not request.user.is_superuser:
        return response_400("you can't create category")

    category_name = request.data.get("category_name")

    try:
        category_obj = Category.objects.get(name=category_name)
    except ObjectDoesNotExist as e:
        return response_400("category is not valid")

    new_category_name = request.data.get("new_category_name")

    try:
        Category.objects.get(name=new_category_name)
        return response_400("edited category is already valid")
    except ObjectDoesNotExist as e:
        category_obj.name = new_category_name
        category_max_field = request.data.get("max_field")
        category_obj.max_field = category_max_field
        category_obj.save()

    return response_200("success", None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def edit_field(request):
    if not request.user.is_superuser:
        return response_400("you can't create category")

    field_name = request.data.get("field_name")

    try:
        field_obj = Field.objects.get(name=field_name)
    except ObjectDoesNotExist as e:
        return response_400("there is no such this field")

    new_category_name = request.data.get("new_category_name")

    try:
        category_obj = Category.objects.get(name=new_category_name)
    except ObjectDoesNotExist as e:
        return response_400("there is no such category")

    new_name = request.data.get("new_field_name")

    try:
        Field.objects.get(name=new_name)
    except ObjectDoesNotExist as e:
        return response_400("this field name is already exist")

    new_image = request.data.get("new_image")

    field_obj.category = category_obj
    field_obj.name = new_name
    field_obj.image = new_image
    field_obj.save()

    return response_200("success", None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def remove_category(request):
    if not request.user.is_superuser:
        return response_400("you can't create category")

    category_name = request.data.get("category_name")

    try:
        category_obj = Category.objects.get(name=category_name)
    except ObjectDoesNotExist as e:
        return response_400("there is no such category")

    category_obj.delete()

    return response_200("success", None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def remove_field(request):
    if not request.user.is_superuser:
        return response_400("you can't create category")

    field_name = request.data.get("field_name")

    try:
        field_obj = Field.objects.get(name=field_name)
    except ObjectDoesNotExist as e:
        return response_400("there is no such field")

    try:
        category_obj = Category.objects.get(name=field_obj.category.name)
    except ObjectDoesNotExist as e:
        return response_400("there is no such category")

    field_obj.delete()

    category_obj.current_field = category_obj.current_field-1
    category_obj.save()

    return response_200("success", None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_current_categories(request):
    categories_obj = Category.objects.all()

    this_time = datetime.timestamp(datetime.now())
    list = []
    for category_obj in categories_obj:
        if datetime.timestamp(category_obj.started_at) < this_time and this_time < datetime.timestamp(category_obj.ended_at):
            fields_obj = Field.objects.filter(category=category_obj)
            serializer = MyFieldSerializer(fields_obj, many=True)
            return_obj = {"category": category_obj.name,
                          "fields": serializer.data}
            list.append(return_obj)

    return response_200("success", list)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    categories_obj = Category.objects.all()
    list = []
    for category_obj in categories_obj:
        fields_obj = Field.objects.filter(category=category_obj)
        serializer = MyFieldSerializer(fields_obj, many=True)
        return_obj = {"category": category_obj.name,
                      "fields": serializer.data}
        list.append(return_obj)

    return response_200("success", list)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vote_field(request):
    field_name = request.data.get("field_name")

    try:
        field_obj = Field.objects.get(name=field_name)
    except ObjectDoesNotExist as e:
        return response_400("this field doesn't exist")

    try:
        vote_obj = VotedField.objects.get(category=field_obj.category)
        if vote_obj.is_voted:
            if datetime.timestamp(datetime.now()) - datetime.timestamp(vote_obj.voted_time) < 86400:
                return response_400("you can't vote")

        vote_obj.voted_time = datetime.now()
        vote_obj.is_voted = True
        vote_obj.save()
        field_obj.total_vote = field_obj.total_vote + 1
        field_obj.save()

    except ObjectDoesNotExist as e:
        vote_obj = VotedField.objects.create(category=field_obj.category,
                                             user=request.user,
                                             voted_time=datetime.now(),
                                             is_voted=True)
        field_obj.total_vote = field_obj.total_vote + 1
        field_obj.save()

    return response_200("success", None)
