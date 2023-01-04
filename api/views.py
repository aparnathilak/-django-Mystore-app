from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Products, Carts, Reviews
from api.serializers import ProductSerializer, ProductModelSerializer, UserSerializer, CartSerializer, ReviewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication, permissions


class ProductsView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Products.objects.all()
        serializer = ProductSerializer(qs, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class ProductDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        qs = Products.objects.get(id=id)
        serializer = ProductSerializer(qs, many=False)
        return Response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        Products.objects.filter(id=id).update(**request.data)
        qs = Products.objects.get(id=id)
        serializer = ProductSerializer(qs, many=False)
        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        Products.objects.filter(id=id).delete()
        return Response(data="Product deleted")


# class ProductViewSetView(viewsets.ViewSet):
#    def list(self, request, *args, **kwargs):
#        qs = Products.objects.all()
#        serializer = ProductModelSerializer(qs, many=True)
#        return Response(data=serializer.data)


#   def create(self, request, *args, **kwargs):
#      serializer = ProductModelSerializer(data=request.data)
#       if serializer.is_valid():
#            serializer.save()
#            return Response(data=serializer.data)
#       else:
#           return Response(data=serializer.errors)

#   def retrieve(self, request, *args, **kwargs):
#       id = kwargs.get("pk")
#        qs = Products.objects.get(id=id)
#       serializer = ProductModelSerializer(qs, many=False)
#       return Response(data=serializer.data)

#   def destroy(self, *args, **kwargs):
#       id = kwargs.get("pk")
#       Products.objects.filter(id=id).delete()
#  return Response(data=" item deleted")

#  def update(self, request, *args, **kwargs):
#      id = kwargs.get("pk")
#     obj = Products.objects.get(id=id)
#    serializer = ProductModelSerializer(data=request.data, instance=obj)
#    if serializer.is_valid():
#        serializer.save()
#        return Response(data=serializer.data)
#   else:
#       return Response(data=serializer.errors)

# custom methods in viewset can be defined
#  @action(methods=["GET"], detail=False)
#   def categories(self, request, *args, **kwargs):
#      res = Products.objects.values_list("category", flat=True).distinct()
#     return Response(data=res)


# serialization not required as the result is already in a python native type

# class UsersView(viewsets.ViewSet):
#    def create(self, request, *args, **kwargs):
#        serializer = UserSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(data=serializer.data)
#        else:
#           return Response(data=serializer.errors)

class ProductViewSetView(viewsets.ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Products.objects.all()
    # authentication_classes = [authentication.BasicAuthentication] for basic authentication
    authentication_classes = [authentication.TokenAuthentication]  # for token authentication
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def categories(self, request, *args, **kwargs):
        res = Products.objects.values_list("category", flat=True).distinct()
        return Response(data=res)

    @action(methods=["POST"], detail=True)
    def add_to_cart(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        item = Products.objects.get(id=id)
        user = request.user
        user.carts_set.create(product=item)
        return Response(data="Item added to cart")

    @action(methods=["POST"], detail=True)
    def add_review(self, request, *args, **kwargs):
        usr = request.user
        id = kwargs.get("pk")
        item = Products.objects.get(id=id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=item, user=usr)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"], detail=True)
    def get_review(self, request, *args, **kwargs):
        item = self.get_object()
        qs = item.reviews_set.all()
        serializer = ReviewSerializer(qs, many=True)
        return Response(data=serializer.data)


class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # overriding list method to take list of cart item of users who sends the credential

    def list(self, request, *args, **kwargs):
        qs = request.user.carts_set.all()
        serializer = CartSerializer(qs, many=True)
        return Response(data=serializer.data)


class ReviewDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        item = Reviews.objects.get(id=id).delete()
        return Response(data="Review deleted")


class UsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

# Or to change only query set just override get_queryset method
#     def get_queryset(self):
#         return self.request.user.carts_set.all()
