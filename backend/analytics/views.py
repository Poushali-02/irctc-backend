
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT=MongoClient(os.getenv("MONGO_URI"))
DATABASE=CLIENT[os.getenv("MONGO_DB_NAME")]


@extend_schema(tags=['Analytics'])
class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            if DATABASE is None:
                return Response(
                    {
                        "error": "Mongodb not connected"
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            pipeline = [
                {
                    "$match": {
                        "endpoint": {"$regex" : "/trains/search"} # filtering out search queries only
                    }
                },
                {
                    "$project": { # extract source and dest
                        "source" : "$query_params.source",
                        "destination": "$query_params.destination"
                    }
                },
                {
                    "$match":{ # if both are missing
                        "source": {"$ne": None, "$exists": True},
                        "destination": {"$ne": None, "$exists": True}
                    }
                },
                {
                    "$group": { # group by source and dest
                        "_id": {
                            "source": "$source",
                            "destination": "$destination"
                        }, 
                        "search_count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {"search_count": -1} # descending order
                },
                {
                    "$limit": 5 # top 5 most searched
                },
                {
                    "$project":{
                        "_id": 0,
                        "source": {"$arrayElemAt": ["$_id.source", 0]},
                        "destination": {"$arrayElemAt": ["$_id.destination", 0]},
                        "search_count": 1
                    }
                }
            ]
            
            collection = DATABASE['api_logs']
            results = list(collection.aggregate(pipeline))
            
            return Response(
                results,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch analytics: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )