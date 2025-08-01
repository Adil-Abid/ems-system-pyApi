from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from emsmodel import models
from emsmodel import serializers
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError, OperationalError, ProgrammingError

# from django.db import transaction
# import psycopg2
# from config import load_config

class DummyAPI(APIView):
    def get(self, request):
        queryset = models.dummy.objects.all()
        serializer = serializers.dummySerializer(queryset, many=True)
        return Response({
            "status": "0",
            "message": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = serializers.dummySerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "0",
            "message": "data saved",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def put(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": 'id is required',
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            dummy = models.dummy.objects.get(id=data.get('id'))
        except models.dummy.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.dummySerializer(dummy, data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
          
    def delete(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "status": "2",
                "message": "data not deleted",
                "error": 'id is required',
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            dummy = models.dummy.objects.get(id=data.get('id'))
            dummy.delete()
        except models.dummy.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        }, status=status.HTTP_200_OK)

class CompanyAPI(APIView):
    def get(self, requests):
        queryset = models.Company.objects.all()
        serializer = serializers.CompanySerializer(queryset, many = True)
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        }, status = status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = serializers.CompanySerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        company = models.Company.objects.get(vid = data.get('vid'))
        serializer = serializers.CompanySerializer(company, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        }, status = status.HTTP_200_OK)
    
    # def patch(self, request):
    #     data = request.data

    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         }, status = status.HTTP_400_BAD_REQUEST)

    #     company = models.Company.objects.get(VID = data.get('VID'))
    #     serializer = serializers.CompanySerializer(
    #         company, data=data, partial=True)

    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": serializer.errors,
    #         }, status = status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data save",
    #         "data": serializer.data
    #     }, status = status.HTTP_200_OK)        

class DepartmentAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Department.objects.get(vid = data.get('vid'))
            serializer = serializers.DepartmentSerializer(queryset)
        else :
            queryset = models.Department.objects.all()
            serializer = serializers.DepartmentSerializer(queryset, many = True)   
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        }, status= status.HTTP_200_OK)    

    def post(self, request):
        data = request.data

        if models.Department.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Department.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Department.objects.filter(vnameurdu=data.get("vnameurdu")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Urdu Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer = serializers.DepartmentSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        }, status = status.HTTP_200_OK)
    
    # def patch(self, request):
    #     data = request.data

    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not updated",
    #             "error": 'id is required',
    #         }, status = status.HTTP_400_BAD_REQUEST)

    #     department = models.Department.objects.get(VID = data.get('VID'))
    #     serializer = serializers.DepartmentSerializer(
    #         department, data=data, partial=True)

    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not updated",
    #             "error": serializer.errors,
    #         }, status = status.HTTP_400_BAD_REQUEST)

    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data updated",
    #         "data": serializer.data
    #     }, status = status.HTTP_200_OK) 

    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)
        
        # Check if the record exists
        try:
            department = models.Department.objects.get(pk=data.get('vid'))
        except models.Department.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check for duplicate VCode (excluding the current record)
        if models.Department.objects.filter(vcode=data.get("vcode")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VCode not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for duplicate VName (excluding the current record)
        if models.Department.objects.filter(vname=data.get("vname")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VName not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for duplicate VNameUrdu (excluding the current record)
        if models.Department.objects.filter(vnameurdu=data.get("vnameurdu")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate Urdu Name not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)


        # if data.get('VID') == 0:
        #     if models.Department.objects.filter(VCode = data.get("VCode")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Code not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Department.objects.filter(VName=data.get("VName")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Department.objects.filter(VNameUrdu=data.get("VNameUrdu")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Urdu Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)        

        department = models.Department.objects.get(vid = data.get('vid'))
        serializer = serializers.DepartmentSerializer(department, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        }, status = status.HTTP_200_OK)

    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        department = models.Department.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        }, status = status.HTTP_200_OK) 

class DepartmentGroupAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.DepartmentGroup.objects.get(vid = data.get('vid'))
            serializer = serializers.DepartmentGroupSerializer(queryset)
        else :
            queryset = models.DepartmentGroup.objects.all()
            serializer = serializers.DepartmentGroupSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        }, status = status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if models.DepartmentGroup.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.DepartmentGroup.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.DepartmentGroup.objects.filter(vnameurdu=data.get("vnameurdu")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Urdu Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer = serializers.DepartmentGroupSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        # Check if the record exists
        try:
            departmentGroup = models.DepartmentGroup.objects.get(pk=data.get('vid'))
        except models.DepartmentGroup.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)

        # Check for duplicate vcode (excluding the current record)
        if models.DepartmentGroup.objects.filter(vcode=data.get("vcode")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VCode not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vname (excluding the current record)
        if models.DepartmentGroup.objects.filter(vname=data.get("vname")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VName not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for duplicate vnameurdu (excluding the current record)
        if models.DepartmentGroup.objects.filter(vnameurdu=data.get("vnameurdu")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate Urdu Name not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # if data.get('VID') == 0:
        #     if models.DepartmentGroup.objects.filter(VCode = data.get("VCode")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Code not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.DepartmentGroup.objects.filter(VName=data.get("VName")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.DepartmentGroup.objects.filter(VNameUrdu=data.get("VNameUrdu")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Urdu Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)    

        departmentGroup = models.DepartmentGroup.objects.get(vid = data.get('vid'))
        serializer = serializers.DepartmentGroupSerializer(departmentGroup, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })

    def patch(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        departmentGroup = models.DepartmentGroup.objects.get(vid = data.get('vid'))
        serializer = serializers.DepartmentGroupSerializer(
            departmentGroup, data=data, partial=True)

        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })

    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        departmentGroup = models.DepartmentGroup.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class LocationAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Location.objects.get(vid = data.get('vid'))
            serializer = serializers.LocationSerializer(queryset)
        else :
            queryset = models.Location.objects.all()
            serializer = serializers.LocationSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Location.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Location.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Location.objects.filter(vnameurdu=data.get("vnameurdu")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Urdu Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer = serializers.LocationSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        # Check if the record exists
        try:
            location = models.Location.objects.get(pk=data.get('vid'))
        except models.Location.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)

        # Check for duplicate vcode (excluding the current record)
        if models.Location.objects.filter(vcode=data.get("vcode")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate vcode not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vname (excluding the current record)
        if models.Location.objects.filter(vname=data.get("vname")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate vname not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vnameurdu (excluding the current record)
        if models.Location.objects.filter(vnameurdu=data.get("vnameurdu")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate Urdu Name not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # if data.get('VID') == 0:
        #     if models.Location.objects.filter(VCode = data.get("VCode")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Code not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Location.objects.filter(VName=data.get("VName")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Location.objects.filter(VNameUrdu=data.get("VNameUrdu")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Urdu Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)

        location = models.Location.objects.get(vid = data.get('vid'))
        serializer = serializers.LocationSerializer(location, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)
        location_id = data.get('vid')

        # Check if location is used in the Department model
        if models.Department.objects.filter(locationid=location_id).exists():
            return Response({
                "status": "1",
                "message": "data not deleted",
                "error": "Location is in use and cannot be deleted",
            }, status=status.HTTP_400_BAD_REQUEST)

        location = models.Location.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
    def getLocationLogo(self, obj):
        request = self.context.get('request')
        if obj.Logo:
            return request.build_absolute_uri(obj.Logo.url)
        return None

class DesignationAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Designation.objects.get(vid = data.get('vid'))
            serializer = serializers.DesignationSerializer(queryset)
        else :
            queryset = models.Designation.objects.all().order_by('-vid')
            serializer = serializers.DesignationSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Designation.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Designation.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Designation.objects.filter(vnameurdu=data.get("vnameurdu")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Urdu Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer = serializers.DesignationSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)
        
        # Check if the record exists
        try:
            designation = models.Designation.objects.get(pk=data.get('vid'))
        except models.Designation.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)

        # Check for duplicate vcode (excluding the current record)
        if models.Designation.objects.filter(vcode=data.get("vcode")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate vcode not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vname (excluding the current record)
        if models.Designation.objects.filter(vname=data.get("vname")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate vname not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vnameurdu (excluding the current record)
        if models.Designation.objects.filter(vnameurdu=data.get("vnameurdu")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate Urdu Name not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # if data.get('vid') == 0:
        #     if models.Designation.objects.filter(vcode = data.get("vcode")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Code not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
    
        #     if models.Designation.objects.filter(VName=data.get("VName")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Designation.objects.filter(VNameUrdu=data.get("VNameUrdu")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Urdu Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)

        designation = models.Designation.objects.get(vid = data.get('vid'))
        serializer = serializers.DesignationSerializer(designation, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
  
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "Data not saved",
                "error": "vid is required",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            designation = models.Designation.objects.get(vid=data.get('vid'))
            designation.delete()
            return Response({
                "status": "0",
                "message": "Data deleted",
                "data": {}
            }, status=status.HTTP_200_OK)

        except models.Designation.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Designation not found",
                "error": f"No record found with vid {data.get('vid')}",
            }, status=status.HTTP_404_NOT_FOUND)

        except IntegrityError:
            return Response({
                "status": "3",
                "message": "Cannot delete this record because it is linked to other data.",
            }, status=status.HTTP_400_BAD_REQUEST)

        except OperationalError:
                return Response({
                    "status": "3",
                    "message": "Database connection issue. Please try again later.",
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ProgrammingError:
                return Response({
                    "status": "3",
                    "message": "There was an internal error. Our team has been notified.",
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except DatabaseError:
                return Response({
                    "status": "3",
                    "message": "A database error occurred while processing your request.",
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # def delete(self, request):
    #     data = request.data

    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         }, status = status.HTTP_400_BAD_REQUEST)

    #     designation = models.Designation.objects.get(VID = data.get('VID')).delete()
    #     return Response({
    #         "status": "0",
    #         "message": "data deleted",
    #         "data": {}
    #     })
    
class GradeAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Grade.objects.get(vid=data.get('vid'))
            serializer = serializers.GradeSerializer(queryset)
        else :
            queryset = models.Grade.objects.all()
            serializer = serializers.GradeSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Grade.objects.filter(vcode=data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Grade.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Grade.objects.filter(vnameurdu=data.get("vnameurdu")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Urdu Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer = serializers.GradeSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)
        
        # Check if the record exists
        try:
            grade = models.Grade.objects.get(pk=data.get('vid'))
        except models.Grade.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)
        # Check for duplicate vcode (excluding the current record)
        if models.Grade.objects.filter(vcode=data.get("vcode")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VCode not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vname (excluding the current record)
        if models.Grade.objects.filter(vname=data.get("vname")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VName not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate vnameurdu (excluding the current record)
        if models.Grade.objects.filter(vnameurdu=data.get("vnameurdu")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate Urdu Name not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)


        # if data.get('VID') == 0:
        #     if models.Grade.objects.filter(VCode = data.get("VCode")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Code not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Grade.objects.filter(VName=data.get("VName")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Grade.objects.filter(VNameUrdu=data.get("VNameUrdu")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Urdu Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)

        grade = models.Grade.objects.get(vid = data.get('vid'))
        serializer = serializers.GradeSerializer(grade, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        grade = models.Grade.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class BankAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Bank.objects.get(vid = data.get('vid'))
            serializer = serializers.BankSerializer(queryset)
        else :
            queryset = models.Bank.objects.all()
            serializer = serializers.BankSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Bank.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Bank.objects.filter(branchname = data.get("branchname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Branch Name not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        if models.Bank.objects.filter(accountnumber = data.get("accountnumber")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Account Number not allowed",
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer = serializers.BankSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)
        
        # Check if the record exists
        try:
            bank = models.Bank.objects.get(pk=data.get('vid'))
        except models.Bank.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)

        # Check for duplicate vcode (excluding the current record)
        if models.Bank.objects.filter(vcode=data.get("vcode")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate vcode not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate branchname (excluding the current record)
        if models.Bank.objects.filter(branchname=data.get("branchname")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate branchname not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate accountnumber (excluding the current record)
        if models.Bank.objects.filter(accountnumber=data.get("accountnumber")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate Urdu Name not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)

        # if data.get('VID') == 0:
        #     if models.Bank.objects.filter(VCode = data.get("VCode")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Code not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Bank.objects.filter(BranchName = data.get("BranchName")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Branch Name not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)
            
        #     if models.Bank.objects.filter(AccountNumber = data.get("AccountNumber")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Account Number not allowed",
        #         }, status = status.HTTP_400_BAD_REQUEST)

        bank = models.Bank.objects.get(vid = data.get('vid'))
        serializer = serializers.BankSerializer(bank, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        bank = models.Bank.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class AllowDedCatAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AllowDedCat.objects.get(vid = data.get('vid'))
            serializer = serializers.AllowDedCatSerializer(queryset)
        else :
            queryset = models.AllowDedCat.objects.all()
            serializer = serializers.AllowDedCatSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    # def post(self, request):
    #     data = request.data
    #     serializer = AllowDedCatSerializer(data = data)
    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": serializer.errors,
    #         })
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data save",
    #         "data": serializer.data
    #     })
    
    # def put (self, request):
    #     data = request.data
        
    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         })
    #     allDedCat = AllowDedCat.objects.get(VID = data.get('VID'))
    #     serializer = AllowDedCatSerializer(allDedCat, data=request.data)
        
    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not updated",
    #             "error": serializer.errors,
    #         })
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data updated",
    #         "data": serializer.data
    #     })
    
    # def delete(self, request):
    #     data = request.data

    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         })

    #     allowDedCat = AllowDedCat.objects.get(VID = data.get('VID')).delete()
    #     return Response({
    #         "status": "0",
    #         "message": "data deleted",
    #         "data": {}
    #     })
    
class AllowDedAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('VID'):
            queryset = models.AllowDed.objects.get(VID = data.get('VID'))
            serializer = serializers.AllowDedSerializer(queryset)
        else :
            queryset = models.AllowDed.objects.all()
            serializer = serializers.AllowDedSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.AllowDedSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        allowDed = models.AllowDed.objects.get(vid = data.get('vid'))
        serializer = serializers.AllowDedSerializer(allowDed, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        allowDed = models.AllowDed.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
        
class AllowanceDedCatByNameAPI(APIView):
    def get(self, request):

        parm_VType = request.query_params.get('vtype')

        if parm_VType:
            queryset = models.AllowDedCat.objects.filter(vtype = parm_VType)
            serializer = serializers.AllowDedCatSerializer(queryset, many = True)
        else:
            serializer = None
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data if serializer else []
        })

class AllowanceDedByCatAPI(APIView):
    def get(self, request):
        parm_Vtype = request.query_params.get('vtype')
        parm_GroupID = request.query_params.get('groupid')
        if parm_Vtype and parm_GroupID:
            queryset = models.AllowDed.objects.filter(vtype = parm_Vtype, groupid = parm_GroupID)
            serializer = serializers.AllowDedSerializer(queryset, many = True)
        else:
            serializer = None
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data if serializer else []
        })

class AllowDedGroupAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AllowDedGroup.objects.get(vid = data.get('vid'))
            serializer = serializers.AllowDedGroupSerializer(queryset)
        else :
            queryset = models.AllowDedGroup.objects.all()
            serializer = serializers.AllowDedGroupSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    # def post(self, request):
    #     data = request.data
    #     serializer = AllowDedGroupSerializer(data = data)
    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": serializer.errors,
    #         })
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data save",
    #         "data": serializer.data
    #     })
    
    # def put (self, request):
    #     data = request.data
        
    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         })
    #     allowDedGroup = AllowDedGroup.objects.get(VID = data.get('VID'))
    #     serializer = AllowDedGroupSerializer(allowDedGroup, data=request.data)
        
    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not updated",
    #             "error": serializer.errors,
    #         })
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data updated",
    #         "data": serializer.data
    #     })
    
    # def delete(self, request):
    #     data = request.data

    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         })

    #     allowDedGroup = AllowDedGroup.objects.get(VID = data.get('VID')).delete()
    #     return Response({
    #         "status": "0",
    #         "message": "data deleted",
    #         "data": {}
    #     })
    
class AttCodeAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttCode.objects.get(vid = data.get('vid'))
            serializer = serializers.AttCodeSerializer(queryset)
        else :
            queryset = models.AttCode.objects.all()
            serializer = serializers.AttCodeSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.AttCode.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            })

        if models.AttCode.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.AttCodeSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        # Check if the record exists
        try:
            attCode = models.AttCode.objects.get(pk=data.get('vid'))
        except models.AttCode.DoesNotExist:
            return Response({
                "status": "1",
                "message": "Record not found",
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check for duplicate VCode (excluding the current record)
        if models.AttCode.objects.filter(vcode=data.get("vcode")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VCode not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for duplicate VName (excluding the current record)
        if models.AttCode.objects.filter(vname=data.get("vname")).exclude(pk=data.get('vid')).exists():
            return Response({
                "status": "1",
                "message": "Data not updated",
                "error": "Duplicate VName not allowed",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # if data.get('VID') == 0:
        #     if models.AttCode.objects.filter(VCode = data.get("VCode")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Code not allowed",
        #         })
            
        #     if models.AttCode.objects.filter(VName=data.get("VName")).exists():
        #         return Response({
        #             "status": "1",
        #             "message": "data not saved",
        #             "error": "Duplicate Name not allowed",
        #         })

        attCode = models.AttCode.objects.get(vid = data.get('vid'))
        serializer = serializers.AttCodeSerializer(attCode, data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attCode = models.AttCode.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class AttGroupAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttGroup.objects.get(vid = data.get('vid'))
            serializer = serializers.AttGroupSerializer(queryset)
        else :
            queryset = models.AttGroup.objects.all()
            serializer = serializers.AttGroupSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    # def post(self, request):
    #     data = request.data
    #     serializer = AttGroupSerializer(data = data)
    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": serializer.errors,
    #         })
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data save",
    #         "data": serializer.data
    #     })
    
    # def put (self, request):
    #     data = request.data
        
    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         })
    #     attGroup = AttGroup.objects.get(VID = data.get('VID'))
    #     serializer = AttGroupSerializer(attGroup, data=request.data)
        
    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not updated",
    #             "error": serializer.errors,
    #         })
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data updated",
    #         "data": serializer.data
    #     })
    
    # def delete(self, request):
    #     data = request.data

    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         })

    #     attGroup = AttGroup.objects.get(VID = data.get('VID')).delete()
    #     return Response({
    #         "status": "0",
    #         "message": "data deleted",
    #         "data": {}
    #     })

class AttLeaveTypeAPI(APIView):
    def get(self, request):
        data = request.data

        queryset = models.AttGroup.objects.filter(forleave = 1)
        serializer = serializers.AttGroupSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })
    
class RamazanAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Ramazan.objects.get(vid = data.get('vid'))
            serializer = serializers.RamazanSerializer(queryset)
        else :
            queryset = models.Ramazan.objects.all()
            serializer = serializers.RamazanSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.RamazanSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        ramazan = models.Ramazan.objects.get(vid = data.get('vid'))
        serializer = serializers.RamazanSerializer(ramazan, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        ramazan = models.Ramazan.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class HolidayAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Holiday.objects.get(vid = data.get('vid'))
            serializer = serializers.HolidaySerializer(queryset)
        else :
            queryset = models.Holiday.objects.all().order_by('-vid')
            serializer = serializers.HolidaySerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Holiday.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.HolidaySerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        if data.get('vid') == 0:
            if models.Holiday.objects.filter(vname=data.get("vname")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Name not allowed",
                })

        holiday = models.Holiday.objects.get(vid = data.get('vid'))
        serializer = serializers.HolidaySerializer(holiday, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        holiday = models.Holiday.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class LeaveBalanceAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.LeaveBalance.objects.get(vid = data.get('vid'))
            serializer = serializers.LeaveBalanceSerializer(queryset)
        else :
            queryset = models.LeaveBalance.objects.all()
            serializer = serializers.LeaveBalanceSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.LeaveBalanceSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        leaveBalance = models.LeaveBalance.objects.get(vid = data.get('vid'))
        serializer = serializers.LeaveBalanceSerializer(leaveBalance, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        leaveBalance = models.LeaveBalance.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class LeaveTypeAPI(APIView):
    def get(self, request):
        queryset = models.AttGroup.objects.filter(isoff=True)
        serializer = serializers.LeaveTypeSerializer(queryset, many=True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })
    
class ShiftAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Shift.objects.get(vid = data.get('vid'))
            serializer = serializers.ShiftSerializer(queryset)
        else :
            queryset = models.Shift.objects.all()
            serializer = serializers.ShiftSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Shift.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            })

        if models.Shift.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.ShiftSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        if data.get('vid') == 0:
            if models.Shift.objects.filter(vcode = data.get("vcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Code not allowed",
                })

        if models.Shift.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        shift = models.Shift.objects.get(vid = data.get('vid'))
        serializer = serializers.ShiftSerializer(shift, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        shift = models.Shift.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SalaryIncrementAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryIncrement.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryIncrementSerializer(queryset)
        else :
            queryset = models.SalaryIncrement.objects.all()
            serializer = serializers.SalaryIncrementSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.SalaryIncrementSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        salaryIncrement = models.SalaryIncrement.objects.get(vid = data.get('vid'))
        serializer = serializers.SalaryIncrementSerializer(salaryIncrement, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        salaryIncrement = models.SalaryIncrement.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SalaryAllowDedAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryAllowDed.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryAllowDedSerializer(queryset)
        else :
            queryset = models.SalaryAllowDed.objects.all()
            serializer = serializers.SalaryAllowDedSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.SalaryAllowDedSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        salaryAllowDed = models.SalaryAllowDed.objects.get(vid = data.get('vid'))
        serializer = serializers.SalaryAllowDedSerializer(salaryAllowDed, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        salaryAllowDed = models.SalaryAllowDed.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SalaryAdvanceAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryAllowDed.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryAllowDedSerializer(queryset)
        else :
            queryset = models.SalaryAllowDed.objects.filter(AllowDedID=6)
            serializer = serializers.SalaryAllowDedSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

class LocalSaleAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryAllowDed.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryAllowDedSerializer(queryset)
        else :
            queryset = models.SalaryAllowDed.objects.filter(AllowDedID=16)
            serializer = serializers.SalaryAllowDedSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

class SalaryLoanAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryLoan.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryLoanSerializer(queryset)
        else :
            queryset = models.SalaryLoan.objects.all()
            serializer = serializers.SalaryLoanSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.SalaryLoanSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        salaryLoan = models.SalaryLoan.objects.get(vid = data.get('vid'))
        serializer = serializers.SalaryLoanSerializer(salaryLoan, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        salaryLoan = models.SalaryLoan.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SalaryLoanDeductionAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryLoanDeduction.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryLoanDeductionSerializer(queryset)
        else :
            queryset = models.SalaryLoanDeduction.objects.all()
            serializer = serializers.SalaryLoanDeductionSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.SalaryLoanDeductionSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        salaryLoanDeduction = models.SalaryLoanDeduction.objects.get(vid = data.get('vid'))
        serializer = serializers.SalaryLoanDeductionSerializer(salaryLoanDeduction, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        salaryLoanDeduction = models.SalaryLoanDeduction.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttMainAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttMain.objects.get(vid = data.get('vid'))
            serializer = serializers.AttMainSerializer(queryset)
        else :
            queryset = models.AttMain.objects.all()
            serializer = serializers.AttMainSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.AttMainSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        attMain = models.AttMain.objects.get(vid = data.get('vid'))
        serializer = serializers.AttMainSerializer(attMain, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attMain = models.AttMain.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class EmployeeLast10AttRecordsAPI(APIView):
    def get(self, request):
        empid = request.query_params.get('empid')

        queryset = models.AttMain.objects.filter(empid = empid).order_by('-vdate')[:10]
        serializer = serializers.AttMainSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })
    
class AttClosingDayAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttClosingDay.objects.get(vid = data.get('vid'))
            serializer = serializers.AttClosingDaySerializer(queryset)
        else :
            queryset = models.AttClosingDay.objects.all()
            serializer = serializers.AttClosingDaySerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.AttClosingDaySerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        attClosingDay = models.AttClosingDay.objects.get(vid = data.get('vid'))
        serializer = serializers.AttClosingDaySerializer(attClosingDay, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attClosingDay = models.AttClosingDay.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttLeaveAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttLeave.objects.get(vid = data.get('vid'))
            serializer = serializers.AttLeaveSerializer(queryset)
        else :
            queryset = models.AttLeave.objects.all()
            serializer = serializers.AttLeaveSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.AttLeaveSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        attLeave = models.AttLeave.objects.get(vid = data.get('vid'))
        serializer = serializers.AttLeaveSerializer(attLeave, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attLeave = models.AttLeave.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttLeaveSpecialAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttLeaveSpecial.objects.get(vid = data.get('vid'))
            serializer = serializers.AttLeaveSpecialSerializer(queryset)
        else :
            queryset = models.AttLeaveSpecial.objects.all()
            serializer = serializers.AttLeaveSpecialSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.AttLeaveSpecialSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    # def put (self, request):
    #     data = request.data
        
    #     if not data.get('VID'):
    #         return Response({
    #             "status": "2",
    #             "message": "data not saved",
    #             "error": 'id is required',
    #         })
    #     attLeaveSpecial = models.AttLeaveSpecial.objects.get(VID = data.get('VID'))
    #     serializer = serializers.AttLeaveSpecialSerializer(attLeaveSpecial, data=request.data)
        
    #     if not serializer.is_valid():
    #         return Response({
    #             "status": "2",
    #             "message": "data not updated",
    #             "error": serializer.errors,
    #         })
    #     serializer.save()
    #     return Response({
    #         "status": "0",
    #         "message": "data updated",
    #         "data": serializer.data
    #     })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attLeaveSpecial = models.AttLeaveSpecial.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttOTAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttOT.objects.get(vid = data.get('vid'))
            serializer = serializers.AttOTSerializer(queryset)
        else :
            queryset = models.AttOT.objects.all()
            serializer = serializers.AttOTSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.AttOTSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        attOT = models.AttOT.objects.get(vid = data.get('vid'))
        serializer = serializers.AttOTSerializer(attOT, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attOT = models.AttOT.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttOTMonthAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.AttOTMonth.objects.get(vid = data.get('vid'))
            serializer = serializers.AttOTMonthSerializer(queryset)
        else :
            queryset = models.AttOTMonth.objects.all()
            serializer = serializers.AttOTMonthSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.AttOTMonthSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        attOTMonth = models.AttOTMonth.objects.get(vid = data.get('vid'))
        serializer = serializers.AttOTMonthSerializer(attOTMonth, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attOTMonth = models.AttOTMonth.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SalaryTypeAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryType.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryTypeSerializer(queryset)
        else :
            queryset = models.SalaryType.objects.all()
            serializer = serializers.SalaryTypeSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.SalaryType.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            })

        if models.SalaryType.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.SalaryTypeSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        if data.get('vid') == 0:
            if models.SalaryType.objects.filter(vcode = data.get("vcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Code not allowed",
                })

        if models.SalaryType.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        salaryType = models.SalaryType.objects.get(vid = data.get('vid'))
        serializer = serializers.SalaryTypeSerializer(salaryType, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        salaryType = models.SalaryType.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class EmployeeTypeAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.EmployeeType.objects.get(vid = data.get('vid'))
            serializer = serializers.EmployeeTypeSerializer(queryset)
        else :
            queryset = models.EmployeeType.objects.all()
            serializer = serializers.EmployeeTypeSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.EmployeeType.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            })

        if models.EmployeeType.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.EmployeeTypeSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        if data.get('vid') == 0:
            if models.EmployeeType.objects.filter(vcode = data.get("vcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Code not allowed",
                })
        
        employeeType = models.EmployeeType.objects.get(vid = data.get('vid'))
        serializer = serializers.EmployeeTypeSerializer(employeeType, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        employeeType = models.EmployeeType.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class GenderAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Gender.objects.get(vid = data.get('vid'))
            serializer = serializers.GenderSerializer(queryset)
        else :
            queryset = models.Gender.objects.all()
            serializer = serializers.GenderSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Gender.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            })

        if models.Gender.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.GenderSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:
            if models.Gender.objects.filter(vcode = data.get("vcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Code not allowed",
                })

            if models.Gender.objects.filter(vname=data.get("vname")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Name not allowed",
                })

        gender = models.Gender.objects.get(vid = data.get('vid'))
        serializer = serializers.GenderSerializer(gender, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        gender = models.Gender.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class ReligionAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Religion.objects.get(vid = data.get('vid'))
            serializer = serializers.ReligionSerializer(queryset)
        else :
            queryset = models.Religion.objects.all()
            serializer = serializers.ReligionSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Religion.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            })

        if models.Religion.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.ReligionSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        if data.get('vid') == 0:
            if models.Religion.objects.filter(vcode = data.get("vcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Code not allowed",
                })

            if models.Religion.objects.filter(vname=data.get("vname")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Name not allowed",
                })

        religion = models.Religion.objects.get(vid = data.get('vid'))
        serializer = serializers.ReligionSerializer(religion, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        religion = models.Religion.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class StatusAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Status.objects.get(vid = data.get('vid'))
            serializer = serializers.StatusSerializer(queryset)
        else :
            queryset = models.Status.objects.all()
            serializer = serializers.StatusSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Status.objects.filter(vcode = data.get("vcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Code not allowed",
            })

        if models.Status.objects.filter(vname=data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })
        
        serializer = serializers.StatusSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:
            if models.Status.objects.filter(vcode = data.get("vcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Code not allowed",
                })

            if models.Status.objects.filter(vname=data.get("vname")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Name not allowed",
                })

        status = models.Status.objects.get(vid = data.get('vid'))
        serializer = serializers.StatusSerializer(status, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        status = models.Status.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class EmpLocationTransferAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.EmpLocationTransfer.objects.get(vid = data.get('vid'))
            serializer = serializers.EmpLocationTransferSerializer(queryset)
        else :
            queryset = models.EmpLocationTransfer.objects.all()
            serializer = serializers.EmpLocationTransferSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        # if models.EmpLocationTransfer.objects.filter(VNo = data.get("VNo")).exists():
        #     return Response({
        #         "status": "1",
        #         "message": "data not saved",
        #         "error": "Duplicate Voucher No not allowed",
        #     })

        serializer = serializers.EmpLocationTransferSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:
            if models.EmpLocationTransfer.objects.filter(vno = data.get("vno")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Voucher No not allowed",
                })

        empLocationTransfer = models.EmpLocationTransfer.objects.get(vid = data.get('vid'))
        serializer = serializers.EmpLocationTransferSerializer(empLocationTransfer, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        empLocationTransfer = models.EmpLocationTransfer.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class EmployeeAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.Employee.objects.get(vid = data.get('vid'))
            serializer = serializers.EmployeeSerializer(queryset)
        else :
            queryset = models.Employee.objects.all()
            serializer = serializers.EmployeeSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.Employee.objects.filter(empcode = data.get("empcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Employee Code not allowed",
            })

        if models.Employee.objects.filter(ename=data.get("ename")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Employee Name not allowed",
            })

        serializer = serializers.EmployeeSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('empid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:
            if models.Employee.objects.filter(empcode = data.get("empcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Employee Code not allowed",
                })

            if models.Employee.objects.filter(ename=data.get("ename")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Employee Name not allowed",
                })
        
        employee = models.Employee.objects.get(empid = data.get('empid'))
        serializer = serializers.EmployeeSerializer(employee, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('empid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        empLocationTransfer = models.Employee.objects.get(empid = data.get('empid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecUserAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('userid'):
            queryset = models.SecUser.objects.get(vid = data.get('userid'))
            serializer = serializers.SecUserSerializer(queryset)
        else :
            queryset = models.SecUser.objects.all()
            serializer = serializers.SecUserSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.SecUser.objects.filter(userlogin = data.get("userlogin")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Userlogin not allowed",
            })

        if models.SecUser.objects.filter(userfullname=data.get("userfullname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Userfullname not allowed",
            })

        serializer = serializers.SecUserSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('userid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        if data.get('userid') == 0:
            if models.SecUser.objects.filter(userlogin = data.get("userlogin")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Userlogin not allowed",
                })

            if models.SecUser.objects.filter(userfullname=data.get("userfullname")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Userfullname not allowed",
                })
        
        secUser = models.SecUser.objects.get(userid = data.get('userid'))
        serializer = serializers.SecUserSerializer(secUser, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('userid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secUser = models.SecUser.objects.get(userid = data.get('userid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecRoleAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SecRole.objects.get(vid = data.get('vid'))
            serializer = serializers.SecRoleSerializer(queryset)
        else :
            queryset = models.SecRole.objects.all()
            serializer = serializers.SecRoleSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.SecRole.objects.filter(vname = data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.SecRoleSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        # if data.get('VID') == 0:
            # if models.SecRole.objects.filter(VID = data.get("VID")).exists():
            #     return Response({
            #         "status": "1",
            #         "message": "data not saved",
            #         "error": "Duplicate Userlogin not allowed",
            #     })
            
            # if models.SecRole.objects.filter(Userfullname=data.get("Userfullname")).exists():
            #     return Response({
            #         "status": "1",
            #         "message": "data not saved",
            #         "error": "Duplicate Userfullname not allowed",
            #     })

        secRole = models.SecRole.objects.get(vid = data.get('vid'))
        serializer = serializers.SecRoleSerializer(secRole, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secRole = models.SecRole.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecPageAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SecPage.objects.get(vid = data.get('vid'))
            serializer = serializers.SecPageSerializer(queryset)
        else :
            queryset = models.SecPage.objects.all()
            serializer = serializers.SecPageSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.SecPage.objects.filter(vname = data.get("vname")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Name not allowed",
            })

        serializer = serializers.SecPageSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:
            # if models.SecPage.objects.filter(VID = data.get("VID")).exists():
            #     return Response({
            #         "status": "1",
            #         "message": "data not saved",
            #         "error": "Duplicate Userlogin not allowed",
            #     })
            
            # if models.SecPage.objects.filter(Userfullname=data.get("Userfullname")).exists():
            #     return Response({
            #         "status": "1",
            #         "message": "data not saved",
            #         "error": "Duplicate Userfullname not allowed",
            #     })

            secPage = models.SecPage.objects.get(vid = data.get('vid'))
            serializer = serializers.SecPageSerializer(secPage, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secPage = models.SecPage.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecRolePageAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SecRolePage.objects.get(vid = data.get('vid'))
            serializer = serializers.SecRolePageSerializer(queryset)
        else :
            queryset = models.SecRolePage.objects.all()
            serializer = serializers.SecRolePageSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.SecRolePageSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        if data.get('vid') > 0:

            secRolePage = models.SecRolePage.objects.get(vid = data.get('vid'))
            serializer = serializers.SecRolePageSerializer(secRolePage, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secRolePage = models.SecRolePage.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecUserCompanyAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SecUserCompany.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserCompanySerializer(queryset)
        else :
            queryset = models.SecUserCompany.objects.all()
            serializer = serializers.SecUserCompanySerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.SecUserCompanySerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        if data.get('vid') == 0:

            secUserCompany = models.SecUserCompany.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserCompanySerializer(secUserCompany, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secUserCompany = models.SecUserCompany.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecUserLocationAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SecUserLocation.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserLocationSerializer(queryset)
        else :
            queryset = models.SecUserLocation.objects.all()
            serializer = serializers.SecUserLocationSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.SecUserLocationSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        if data.get('vid') == 0:

            secUserLocation = models.SecUserLocation.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserLocationSerializer(secUserLocation, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secUserLocation = models.SecUserLocation.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecUserRoleAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SecUserRole.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserRoleSerializer(queryset)
        else :
            queryset = models.SecUserRole.objects.all()
            serializer = serializers.SecUserRoleSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.SecUserRoleSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:

            secUserRole = models.SecUserRole.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserRoleSerializer(secUserRole, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secUserRole = models.SecUserRole.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class SecUserPageAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SecUserPage.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserPageSerializer(queryset)
        else :
            queryset = models.SecUserPage.objects.all()
            serializer = serializers.SecUserPageSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.SecUserPageSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:

            secUserPage = models.SecUserPage.objects.get(vid = data.get('vid'))
            serializer = serializers.SecUserPageSerializer(secUserPage, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        secUserPage = models.SecUserPage.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttEntryAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('orgini')
        vdate = request.query_params.get('vdate')
        datefrom = request.query_params.get('datefrom')
        dateto = request.query_params.get('dateto')
        deptids = request.query_params.get('deptids')
        employeeidlist = request.query_params.get('employeeidlist')
        companyid = request.query_params.get('companyid')
        locationid = request.query_params.get('locationid')
        etypeid = request.query_params.get('etypeid')
        empid = request.query_params.get('empid')
        isau = request.query_params.get('isau')
        onlyot = request.query_params.get('onlyot')
        isexport = request.query_params.get('isexport')
        uid = request.query_params.get('uid')
        inflage = request.query_params.get('inflage')

        # print(orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage)

        try:
            rows = []
            with connection.cursor() as cursor:                 

                cursor.execute("""  CALL spentryfillregister(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
                    orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage
                ])

                if inflage == '0':
                    cursor.execute(""" SELECT * FROM tblOneTime """)
                    results = cursor.fetchall()

                if inflage == '1':
                    cursor.execute(""" SELECT * FROM multitime """)
                    results = cursor.fetchall()

                if inflage == '2':
                    cursor.execute(""" SELECT * FROM multitime1 """)
                    results = cursor.fetchall()

                # if results and cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                # print(rows)
                # else:
                #     print("No data returned or invalid query.")
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

    def post(self, request):
        data = request.data

        empid = data.get('empid')
        vdate = data.get('vdate')
        vid1 = data.get('vid1')
        vid2 = data.get('vid2')
        shiftid = data.get('shiftid')
        datein1 = data.get('datein1')
        dateout1 = data.get('dateout1')
        datein2 = data.get('datein2')
        dateout2 = data.get('dateout2')
        remarks = data.get('remarks')
        uid = data.get('uid')
        computername = data.get('computername')

        print(empid, vdate, vid1, vid2, shiftid, datein1, dateout1, datein2, dateout2, remarks, uid, computername)

        # with connection.cursor() as cursor:
        #     cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName])
            # print(cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName]))
        with connection.cursor() as cursor:
            cursor.execute(""" CALL spsavetblattmain(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
                empid, vdate, vid1, vid2, shiftid,
                datein1, dateout1, datein2, dateout2,
                remarks, uid, computername
                ])
            cursor.execute("""  SELECT * FROM attmainentrystatus """)
            # rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        
            return Response(rows)

class AttChangeAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('orgini')
        vdate = request.query_params.get('vdate')
        datefrom = request.query_params.get('datefrom')
        dateto = request.query_params.get('dateto')
        deptids = request.query_params.get('deptids')
        employeeidlist = request.query_params.get('employeeidlist')
        companyid = request.query_params.get('companyid')
        locationid = request.query_params.get('locationid')
        etypeid = request.query_params.get('etypeid')
        empid = request.query_params.get('empid')
        isau = request.query_params.get('isau')
        onlyot = request.query_params.get('onlyot')
        isexport = request.query_params.get('isexport')
        uid = request.query_params.get('uid')
        inflage = request.query_params.get('inflage')

        # print(orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage)

        try:
            rows = []
            # with transaction.atomic():
            with connection.cursor() as cursor:                 

                cursor.execute("""  CALL spentryfillregisterchange(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
                    orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage
                ])

                cursor.execute(""" SELECT * FROM MultiTimeChangeFinal """)
                # cursor.execute(""" SELECT * FROM MultiTimeChange """)
                results = cursor.fetchall()

                # if results and cursor.description:

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                print(columns)
                print(rows)
                # else:
                #     print("No data returned or invalid query.")
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
    
    def post(self, request):
        data = request.data

        vid = data.get('vid')
        empid = data.get('empid')
        vdate = data.get('vdate')
        vid1 = data.get('vid1')
        vid2 = data.get('vid2')
        shiftid = data.get('shiftid')
        datein1 = data.get('datein1')
        dateout1 = data.get('dateout1')
        datein2 = data.get('datein2')
        dateout2 = data.get('dateout2')
        remarks = data.get('remarks')
        uid = data.get('uid')
        computername = data.get('computername')

        print(empid, vdate, vid1, vid2, shiftid, datein1, dateout1, datein2, dateout2, remarks, uid, computername)

        # with connection.cursor() as cursor:
        #     cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName])
            # print(cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName]))
        with connection.cursor() as cursor:
            cursor.execute(""" CALL spsavetblclosingday(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
                vid, empid, vdate, vid1, vid2, shiftid,
                datein1, dateout1, datein2, dateout2,
                remarks, uid, computername
                ])
            cursor.execute("""  SELECT * FROM attclosingdaystatus """)
            # rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        
            return Response(rows)

class AttSingleAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('orgini')
        vdate = request.query_params.get('vdate')
        datefrom = request.query_params.get('datefrom')
        dateto = request.query_params.get('dateto')
        deptids = request.query_params.get('deptids')
        employeeidlist = request.query_params.get('employeeidlist')
        companyid = request.query_params.get('companyid')
        locationid = request.query_params.get('locationid')
        etypeid = request.query_params.get('etypeid')
        empid = request.query_params.get('empid')
        isau = request.query_params.get('isau')
        onlyot = request.query_params.get('onlyot')
        isexport = request.query_params.get('isexport')
        uid = request.query_params.get('uid')
        inflage = request.query_params.get('inflage')

        # print(orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage)

        try:
            rows = []
            # with transaction.atomic():
            with connection.cursor() as cursor:                 

                cursor.execute("""  CALL spentryfillregistersingle(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
                    orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage
                ])

                cursor.execute(""" SELECT * FROM attRegisterSingle """)
                results = cursor.fetchall()

                # if results and cursor.description:

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                print(columns)
                print(rows)
                # else:
                #     print("No data returned or invalid query.")
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
    
    def post(self, request):
        data = request.data
        
        vid = data.get('vid')
        empid = data.get('empid')
        vdate = data.get('vdate')
        vid1 = data.get('vid1')
        vid2 = data.get('vid2')
        shiftid = data.get('shiftid')
        datein1 = data.get('datein1')
        dateout1 = data.get('dateout1')
        datein2 = data.get('datein2')
        dateout2 = data.get('dateout2')
        remarks = data.get('remarks')
        uid = data.get('uid')
        computername = data.get('computername')

        print(empid, vdate, vid1, vid2, shiftid, datein1, dateout1, datein2, dateout2, remarks, uid, computername)

        # with connection.cursor() as cursor:
        #     cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName])
            # print(cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName]))
        with connection.cursor() as cursor:
            cursor.execute(""" CALL spsavetblattclosingdaysingle(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
                vid, empid, vdate, vid1, vid2, shiftid,
                datein1, dateout1, datein2, dateout2,
                remarks, uid, computername
                ])
            cursor.execute("""  SELECT * FROM attclosingdaysinglestatus """)
            # rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        
            return Response(rows)

    # def post(self, request):
    #     data = request.data
        
    #     EmpID = data.get('empid')
    #     VDate = data.get('vdate')
    #     VID1 = data.get('vid1')
    #     VID2 = data.get('vid2')
    #     ShiftID = data.get('shiftID')        
    #     DateIn1 = data.get('dateIn1')
    #     DateOut1 = data.get('dateOut1')
    #     DateIn2 = data.get('dateIn2')
    #     DateOut2 = data.get('dateOut2')
    #     Remarks = data.get('remarks')
    #     UID = data.get('uID')
    #     ComputerName = data.get('computerName')

    #     print(EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName)

    #     # with connection.cursor() as cursor:
    #     #     cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName])
    #         # print(cursor.callproc("spsavetblattmain", [EmpID, VDate, VID1, VID2, ShiftID, DateIn1, DateOut1, DateIn2, DateOut2, Remarks, UID, ComputerName]))
    #     with connection.cursor() as cursor:
    #         cursor.execute(""" CALL spsavetblattmain(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
    #             EmpID, VDate, VID1, VID2, ShiftID,
    #             DateIn1, DateOut1, DateIn2, DateOut2,
    #             Remarks, UID, ComputerName
    #             ])
    #         cursor.execute("""  SELECT * FROM attmainentrystatus """)
    #         # rows = cursor.fetchall()
    #         columns = [col[0] for col in cursor.description]
    #         rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        
    #         return Response(rows)
        
class EmployeeSearchAPI(APIView):
    def get(self, request):
        string = request.query_params.get('string')
        cWhere = request.query_params.get('cWhere')
        # etypeID = request.query_params.get('etypeID')
        # ename = request.query_params.get('ename')
        # fname = request.query_params.get('fname')
        # deptID = request.query_params.get('deptID')
        # desgID = request.query_params.get('desgID')
        # hodID = request.query_params.get('hodID')
        # nic = request.query_params.get('nic')
        # locationID = request.query_params.get('locationID')
        # shiftID = request.query_params.get('shiftID')
        # regionID = request.query_params.get('regionID')
        # gradeID = request.query_params.get('gradeID')
        # leftStatus = request.query_params.get('leftStatus')
        # bloodGroup = request.query_params.get('bloodGroup')
        # salaryFrom = request.query_params.get('salaryFrom')
        # salaryTo = request.query_params.get('salaryTo')
        # joinDateFrom = request.query_params.get('joinDateFrom')
        # joinDateTo = request.query_params.get('joinDateTo')
        # resignDateFrom = request.query_params.get('resignDateFrom')
        # resignDateTo = request.query_params.get('resignDateTo')

        # print(string, etypeID, ename, fname, deptID, desgID, hodID, nic, locationID, shiftID, regionID, gradeID, leftStatus, bloodGroup, salaryFrom, 
        #                         salaryTo, joinDateFrom, joinDateTo, resignDateFrom, resignDateTo)

        try:
            rows = []
            with connection.cursor() as cursor:
                
                cursor.execute(""" SELECT * FROM fnSearchEmployee(%s, %s); """, [string, cWhere])
                results = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RemoveExtraAttendanceAPI(APIView):
    def get(self, request):
        deptid = request.query_params.get('deptid')
        empid = request.query_params.get('empid')        
        datefrom = request.query_params.get('datefrom')
        dateto = request.query_params.get('dateto')

        print(deptid, empid, datefrom, dateto)

        try:
            rows = []
            with connection.cursor() as cursor:                
                cursor.execute(""" SELECT * FROM fnremoveextraattendance(%s, %s, %s, %s); """, [deptid, empid, datefrom, dateto])                
                results = cursor.fetchall()                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class GetTypeByAllowDedIdAPI(APIView):
    def get(self, request):
        allowdedid = request.query_params.get('allowdedid')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM FnGetTypeByAllowDedID(%s); """, [allowdedid])

                results = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
    
class SalaryGratuityAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.SalaryGratuity.objects.get(vid = data.get('vid'))
            serializer = serializers.SalaryGratuitySerializer(queryset)
        else :
            queryset = models.SalaryGratuity.objects.all()
            serializer = serializers.SalaryGratuitySerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = serializers.SalaryGratuitySerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        salaryGratuity = models.SalaryGratuity.objects.get(vid = data.get('vid'))
        serializer = serializers.SalaryGratuitySerializer(salaryGratuity, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        salaryGratuity = models.SalaryGratuity.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })
    
class EmployeeTrialAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('vid'):
            queryset = models.EmployeeTrial.objects.get(vid = data.get('vid'))
            serializer = serializers.EmployeeTrialSerializer(queryset)
        else :
            queryset = models.EmployeeTrial.objects.all()
            serializer = serializers.EmployeeTrialSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        if models.EmployeeTrial.objects.filter(empcode = data.get("empcode")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Employee Code not allowed",
            })

        if models.EmployeeTrial.objects.filter(ename=data.get("ename")).exists():
            return Response({
                "status": "1",
                "message": "data not saved",
                "error": "Duplicate Employee Name not allowed",
            })

        serializer = serializers.EmployeeTrialSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        if data.get('vid') == 0:
            if models.EmployeeTrial.objects.filter(empcode = data.get("empcode")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Employee Code not allowed",
                })

            if models.EmployeeTrial.objects.filter(ename=data.get("ename")).exists():
                return Response({
                    "status": "1",
                    "message": "data not saved",
                    "error": "Duplicate Employee Name not allowed",
                })
        
        employeeTrial = models.EmployeeTrial.objects.get(vid = data.get('vid'))
        serializer = serializers.EmployeeTrialSerializer(employeeTrial, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('vid'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        employeeTrial = models.EmployeeTrial.objects.get(vid = data.get('vid')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })    
    
class EmployeeLeaveBalanceAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        cwhere = request.query_params.get('cWhere')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        vdate = request.query_params.get('VDate')        
        isau = request.query_params.get('IsAu')
        empid = request.query_params.get('EmpID')
        isexport = request.query_params.get('IsExport')
        cwherelimit = request.query_params.get('cWhereLimit')        

        print(orgini, cwhere, datefrom, dateto, vdate, isau, empid, isexport, cwherelimit)

        try:
            rows = []
            with connection.cursor() as cursor:                 

                cursor.execute("""  CALL spentryfillleavebalance(%s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ orgini, cwhere, datefrom, dateto, vdate, isau, empid, isexport, cwherelimit ])

                cursor.execute(""" SELECT * FROM tblEmpLeaveBalanceFinal """)
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                print(rows)
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
    
class AttOTFillGridAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        onlyot = request.query_params.get('OnlyOT')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        inflage = request.query_params.get('InFlage')

        try:
            rows = []
            with connection.cursor() as cursor:
                
                cursor.execute(""" SELECT * FROM ftentryfillotday(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage])
                results = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class AttOTMonthFillGridAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        onlyot = request.query_params.get('OnlyOT')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        inflage = request.query_params.get('InFlage')

        try:
            rows = []
            with connection.cursor() as cursor:
                
                cursor.execute(""" SELECT * FROM ftentryfillotmonth(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage])
                results = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class GetEmployeeGratuityDetailAPI(APIView):
    def get(self, request):
        Orgini = request.query_params.get('Orgini')
        EmpID = request.query_params.get('EmpID')
        VDate = request.query_params.get('VDate')
        UID = request.query_params.get('UID')
        IsAu = request.query_params.get('IsAu')
        IgnoreOld = request.query_params.get('IgnoreOld')
        BasicSalary = request.query_params.get('BasicSalary')

        try:
            rows = []
            with connection.cursor() as cursor:
                
                cursor.execute(""" SELECT * FROM fngratuitystatus(%s, %s, %s, %s, %s, %s, %s); """, [ Orgini, EmpID, VDate, UID, IsAu, IgnoreOld, BasicSalary ])
                
                results = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class EmployeeReportsAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        cwhere = request.query_params.get('cWhere')
        vdate = request.query_params.get('VDate')        
        isau = request.query_params.get('IsAu')
        empid = request.query_params.get('EmpID')
        isexport = request.query_params.get('IsExport')
        compcode = request.query_params.get('Compcode')        
        uid = request.query_params.get('UID')        
        reporttype = request.query_params.get('ReportType')        

        print(orgini, cwhere, vdate, isau, empid, isexport, compcode, uid, reporttype)

        try:
            rows = []
            with connection.cursor() as cursor:                 

                cursor.execute("""  CALL sprptemployee(%s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ orgini, cwhere, vdate, isau, empid, isexport, compcode, uid, reporttype  ])

                if  reporttype == 'EmpList' or reporttype == 'EmpCard' or reporttype == '' :
                    cursor.execute(""" SELECT * FROM tblemployeelist """)
                    results = cursor.fetchall()
                
                elif reporttype == 'EmpOnDate':                    
                    cursor.execute(""" SELECT * FROM tblemployeeondate """)
                    results = cursor.fetchall()
                
                elif reporttype == 'EmpListExport':
                    cursor.execute(""" SELECT * FROM tblemployeelistexport """)
                    results = cursor.fetchall()
                
                elif reporttype == 'EmpStrength':
                    cursor.execute(""" SELECT * FROM tblemployeestrength """)
                    results = cursor.fetchall()
                
                elif reporttype == 'EmpStrengthOnDate':
                    cursor.execute(""" SELECT * FROM tblemployeeondatestrength """)
                    results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                # print(rows)
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
    
class AttLeaveDepartmentAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('VID'):
            queryset = models.AttLeaveDepartment.objects.get(VID = data.get('VID'))
            serializer = serializers.AttLeaveDepartmentSerializer(queryset)
        else :
            queryset = models.AttLeaveDepartment.objects.all()
            serializer = serializers.AttLeaveDepartmentSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        VID = data.get('VID')
        VName = data.get('VName')
        DeptID = data.get('DeptID')
        DateFrom = data.get('DateFrom')
        DateTo = data.get('DateTo')
        LeaveTypeID = data.get('LeaveTypeID')        
        UID = data.get('UID')        
        LocationID = data.get('LocationID')
        CompanyID = data.get('CompanyID')

        action = 'Insert'

        serializer = serializers.AttLeaveDepartmentSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        with connection.cursor() as cursor:
            cursor.execute("""  CALL spentryattleavedepartment(%s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ VName, DeptID, DateFrom, DateTo, LeaveTypeID, UID, LocationID, CompanyID, action ])
        
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        attLeaveDepartment = models.AttLeaveDepartment.objects.get(VID = data.get('VID'))
        serializer = serializers.AttLeaveDepartmentSerializer(attLeaveDepartment, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        VID = data.get('VID')
        VName = data.get('VName')
        DeptID = data.get('DeptID')
        DateFrom = data.get('DateFrom')
        DateTo = data.get('DateTo')
        LeaveTypeID = data.get('LeaveTypeID')        
        UID = data.get('UID')        
        LocationID = data.get('LocationID')
        CompanyID = data.get('CompanyID')

        action = 'Delete'

        print (VID, VName, DeptID, DateFrom, DateTo, LeaveTypeID, UID, LocationID, CompanyID)

        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attLeaveDepartment = models.AttLeaveDepartment.objects.get(VID = data.get('VID')).delete()
        with connection.cursor() as cursor:
            cursor.execute("""  CALL spentryattleavedepartment(%s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ VName, DeptID, DateFrom, DateTo, LeaveTypeID, UID, LocationID, CompanyID, action ])
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttExemptLateAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('VID'):
            queryset = models.AttExemptLate.objects.get(VID = data.get('VID'))
            serializer = serializers.AttExemptLateSerializer(queryset)
        else :
            queryset = models.AttExemptLate.objects.all()
            serializer = serializers.AttExemptLateSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.AttExemptLateSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        attExemptLate = models.AttExemptLate.objects.get(VID = data.get('VID'))
        serializer = serializers.AttExemptLateSerializer(attExemptLate, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attExemptLate = models.AttExemptLate.objects.get(VID = data.get('VID')).delete()
        
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class RptATTDailyUnpostedAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')              

        print(orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid)

        try:
            rows = []
            with connection.cursor() as cursor:                 

                cursor.execute("""  SELECT * FROM ftrptattdailyunposted(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid  ])
                
                # cursor.execute(""" SELECT * FROM tblrptdailyunposted """)
                results = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                # print(rows)
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptATTDailyPostedAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')              

        print(orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid)

        try:
            rows = []
            with connection.cursor() as cursor:                 

                cursor.execute("""  SELECT * FROM ftrptattdailyposted (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid  ])
                
                # cursor.execute(""" SELECT * FROM ftrptattdailyposted (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """)
                results = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                # print(rows)
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptATTDailyLateAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')              

        print(orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid)

        try:
            rows = []
            with connection.cursor() as cursor:                 

                cursor.execute("""  SELECT * FROM ftrptattdailylate(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid  ])
                
                # cursor.execute(""" SELECT * FROM tblrptattdailylate """)
                results = cursor.fetchall()
                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
                # print(rows)
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptATTDailyABAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        print(orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid)

        try:
            rows = []
            with connection.cursor() as cursor:                 

                cursor.execute("""  SELECT * FROM ftrptattdailyab(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                               [ orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                # cursor.execute("""  SELECT * FROM ftrptattdailyab(%s, %s::date, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, 
                #                [ orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                # results = cursor.fetchall()

                def format_sql(query, params):
                    from psycopg2.extensions import adapt
                    return query % tuple(adapt(p).getquoted().decode('utf-8') for p in params)


                raw_sql = """SELECT * FROM ftrptattdailyab(%s, %s::date, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                params = [orgini, vdate, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid]

                # Print the interpolated query (FOR DEBUGGING ONLY)
                print("===== RAW SQL TO EXECUTE =====")
                print(format_sql(raw_sql, params))
                
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]

        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
        
class RptATTMonthStatusAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        # print(orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage)

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptattmonthstatus(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptATTMonthSummaryAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        # print(orgini, vdate, datefrom, dateto, deptids, employeeidlist, companyid, locationid, etypeid, empid, isau, onlyot, isexport, uid, inflage)

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptattmonthsummary(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptATTMonthAttendanceAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptattmonthattendance(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptATTMonthABAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptattmonthablist(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptATTMonthLeaveAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptattmonthleave(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class GetRosterDepartmentAPI(APIView):
    def get(self, request):
        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM fngetrosterdepartments(); """,  [ ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
    
class AttRosterAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('VID'):
            queryset = models.AttRoster.objects.get(VID = data.get('VID'))
            serializer = serializers.AttRosterSerializer(queryset)
        else :
            queryset = models.AttRoster.objects.all()
            serializer = serializers.AttRosterSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.AttRosterSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": 'id is required',
            }, status = status.HTTP_400_BAD_REQUEST)

        attRoster = models.AttRoster.objects.get(VID = data.get('VID'))
        serializer = serializers.AttRosterSerializer(attRoster, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attRoster = models.AttRoster.objects.get(VID = data.get('VID')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class AttEntryRosterMonthAPI(APIView):
    def get(self, request):
        data = request.data

        if data.get('VID'):
            queryset = models.AttEntryRosterMonth.objects.get(VID = data.get('VID'))
            serializer = serializers.AttEntryRosterMonthSerializer(queryset)
        else :
            queryset = models.AttEntryRosterMonth.objects.all()
            serializer = serializers.AttEntryRosterMonthSerializer(queryset, many = True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

    def post(self, request):
        data = request.data

        serializer = serializers.AttEntryRosterMonthSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data save",
            "data": serializer.data
        })
    
    def put (self, request):
        data = request.data
        
        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attEntryRosterMonth = models.AttEntryRosterMonth.objects.get(VID = data.get('VID'))
        serializer = serializers.AttEntryRosterMonthSerializer(attEntryRosterMonth, data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "2",
                "message": "data not updated",
                "error": serializer.errors,
            })
        serializer.save()
        return Response({
            "status": "0",
            "message": "data updated",
            "data": serializer.data
        })
    
    def delete(self, request):
        data = request.data

        if not data.get('VID'):
            return Response({
                "status": "2",
                "message": "data not saved",
                "error": 'id is required',
            })

        attEntryRosterMonth = models.AttEntryRosterMonth.objects.get(VID = data.get('EmpID')).delete()
        return Response({
            "status": "0",
            "message": "data deleted",
            "data": {}
        })

class GetRosterShiftAPI(APIView):
    def get(self, request):
        queryset = models.Shift.objects.filter(IsRoster=True)
        serializer = serializers.ShiftSerializer(queryset, many=True)
        
        return Response ({
            "status": "0",
            "message": "success",
            "data" : serializer.data
        })

class RptOverTimeSheetAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthsalarysheet(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptOverTimeSheetSummaryAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthotsheetsum(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptFinalSettlementAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthfinalsettlement(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptMonthSalarySheetAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthotsheet(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptSalaryEmployeeAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthsalaryemployee(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptMonthSalarySummaryAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthsalarysum(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class PaymentPlanFillGridAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        employeeidlist = request.query_params.get('EmployeeIDList')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftEntryFillLoanDed(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, vdate, employeeidlist, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

# class SavePaymentPlanAPI(APIView):
    
#     def post(self, request):
#         data = request.data
        
        
#         VID = data.get('VID')
#         VName = data.get('VName')
#         VNo = data.get('VNo')
#         VDate  = data.get('VDate')
#         EmpID  = data.get('EmpID')
#         LoanID = data.get('LoanID')
#         Amount = data.get('Amount')
#         IsApproved = data.get('IsApproved')
#         ApprovedBy = data.get('ApprovedBy')
#         ApprovedDate = data.get('ApprovedDate')
#         IsPosted = data.get('IsPosted')
#         PostedBy = data.get('PostedBy')
#         PostedDate = data.get('PostedDate')
#         IsActive = data.get('IsActive')
#         UID = data.get('UID')
#         CompanyID = data.get('CompanyID')

        

#          with connection.cursor() as cursor:
#             cursor.execute(""" CALL spsavetblsalaryloandeduction(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, [
#                 VID,VName,VNo,VDate,EmpID,LoanID,Amount,IsApproved
#                 ,ApprovedBy,ApprovedDate,IsPosted,PostedBy
#                 ,PostedDate,IsActive,UID,CompanyID     
#                 ])
                
#              return Response ({
#                 "status": "0",
#                 "message": "success",
#                 "data" : ""
#                 })        


class RptMonthSalaryDeductionAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthsalaryallowded(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class RptMonthSalaryDeductionSumAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        datefrom = request.query_params.get('DateFrom')
        dateto = request.query_params.get('DateTo')
        deptids = request.query_params.get('DeptIDs')
        employeeidlist = request.query_params.get('EmployeeIDList')
        cwhere = request.query_params.get('cWhere')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')
        showPer = request.query_params.get('ShowPer')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftrptmonthsalaryallowdedsum(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, datefrom, dateto, deptids, employeeidlist, cwhere, companyid, locationid, etypeid, empid, isau, isexport, uid, showPer ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class PaymentPlanFillGridAPI(APIView):
    def get(self, request):
        orgini = request.query_params.get('Orgini')
        vdate = request.query_params.get('VDate')
        employeeidlist = request.query_params.get('EmployeeIDList')
        companyid = request.query_params.get('CompanyID')
        locationid = request.query_params.get('LocationID')
        etypeid = request.query_params.get('ETypeID')
        empid = request.query_params.get('EmpID')
        isau = request.query_params.get('IsAu')
        isexport = request.query_params.get('IsExport')
        uid = request.query_params.get('UID')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftEntryFillLoanDed(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, 
                               [ orgini, vdate, employeeidlist, companyid, locationid, etypeid, empid, isau, isexport, uid ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)

class GetddlLocationAPI(APIView):
    def get(self, request):
        p_userlogin = request.query_params.get('p_userlogin')
        p_appname = request.query_params.get('p_appname')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftloginuserlocation(%s, %s); """, 
                               [ p_userlogin, p_appname ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
class LoginAPI(APIView):
    def get(self, request):
        p_userlogin = request.query_params.get('p_userlogin')
        p_userpswd = request.query_params.get('p_userpswd')
        p_locationid = request.query_params.get('p_locationid')
        p_logintype = request.query_params.get('p_logintype')
        p_appname = request.query_params.get('p_appname')

        try:
            rows = []
            with connection.cursor() as cursor:

                cursor.execute(""" SELECT * FROM ftloginuser(%s, %s,%s, %s,%s); """, 
                               [ p_userlogin, p_userpswd, p_locationid, p_logintype, p_appname ])
                results = cursor.fetchall()

                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("DB Error occurred:", str(e))
            return Response({"error": str(e)}, status=500)
        finally:
            cursor.close()
        return Response(rows)
