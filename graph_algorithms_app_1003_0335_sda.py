# 代码生成时间: 2025-10-03 03:35:21
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import networkx as nx

"""
Graph Algorithms Django App

This app is responsible for implementing various graph theory algorithms using NetworkX library.
"""

class GraphAlgorithmView(View):
    """
    View class for handling graph algorithm requests.

    Provides endpoints to compute and return results for different graph algorithms.
    """
    def get(self, request):
        """
        Handles GET requests to compute graph algorithms.
        """
        graph_type = request.GET.get('graph_type')
        if not graph_type:
            return JsonResponse({'error': 'Missing graph type parameter.'}, status=400)

        try:
            # Initialize graph based on the type provided
            if graph_type == 'directed':
                G = nx.DiGraph()
            elif graph_type == 'undirected':
                G = nx.Graph()
            else:
                return JsonResponse({'error': 'Unsupported graph type.'}, status=400)

            # Add edges to the graph based on the request parameters
            edges = request.GET.get('edges', '')
            if edges:
                for edge in edges.split(','):
                    nodes = edge.split('-')
                    G.add_edge(nodes[0], nodes[1])

            # Compute the requested graph algorithm
            if request.GET.get('algorithm') == 'shortest_path':
                start = request.GET.get('start')
                end = request.GET.get('end')
                if start and end:
                    path = nx.shortest_path(G, source=start, target=end)
                    return JsonResponse({'path': path})
                else:
                    return JsonResponse({'error': 'Start and end nodes are required for shortest path.'}, status=400)
            else:
                return JsonResponse({'error': 'Unsupported algorithm.'}, status=400)

        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# URLs for the graph algorithms app
from django.urls import path

urlpatterns = [
    path('graph_algorithm/', GraphAlgorithmView.as_view(), name='graph_algorithm'),
]
