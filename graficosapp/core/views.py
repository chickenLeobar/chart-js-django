from os import error
from chartjs.views import HighChartsView
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
import requests

from django.views.generic import TemplateView
from chartjs.views.pie import HighChartDonutView
from chartjs.views.lines import BaseLineChartView
from chartjs.colors import next_color
from colour import Color

import json


def get_countries(scope):
    data = requests.get("https://api.covid19api.com/summary")
    data_dump = data.json()
    if scope == 'countries':
        return data_dump['Countries']
    else:
        is_general = scope == "general"
        if is_general:
            return data_dump['Global']
        else:
            countries = data_dump['Countries']

            def selec_countrie(countrie):
                return countrie['ID'] == scope
            result = list(filter(selec_countrie, countries))

            return result[0] if len(result) > 0 else None


class PieChart(BaseLineChartView):

    def get_dataset_options(self, index, color, generator: iter):

        default_opt = {
            "backgroundColor": "rgba(%d, %d, %d, 0.5)" % color,
            "borderColor": "rgba(%d, %d, %d, 1)" % color,
            "pointBackgroundColor": "rgba(%d, %d, %d, 1)" % color,
            "pointBorderColor": "#fff",
        }
        return default_opt

    def get_colors(self):
        return ["red", "blue"]

    def get_datasets(self):
        datasets = []
        color_generator = self.get_colors()
        data = self.get_data()
        providers = self.get_providers()
        num = len(providers)
        for i, entry in enumerate(data):
            color = tuple(next(color_generator))
            dataset = {"data": entry}
            temporal_generator = self.get_colors()
            entry_size = len(entry)
            colors = list()
            print(entry_size)
            for i in range(entry_size):
                colors.append("rgba(%d, %d, %d, 0.8)" %
                              next(temporal_generator))
            default_opt = {
                "backgroundColor": colors,
                "borderColor": "rgba(%d, %d, %d, 1)" % color,
                "pointBackgroundColor": "rgba(%d, %d, %d, 1)" % color,
                "pointBorderColor": "#fff",
            }
            dataset.update(default_opt)
            # dataset.update(self.get_dataset_options(i, color , temporal_generator))
            if i < num:
                dataset["label"] = providers[i]  # series labels for Chart.js
                dataset["name"] = providers[i]  # HighCharts may need this
            datasets.append(dataset)
        return datasets


class JSONPieChart(PieChart):
    scope = "general"

    def is_general(self):
        return self.scope == "general"

    def get_labels(self):

        return ["Confirmados", "Muertos", "Recuperados"]

    def get_colors(self):
        colors = [(250, 212, 1), (253, 83, 7), (61, 1, 164)]
        return iter(colors)

    def get_data(self):
        print("data has been called")
        print("scope", self.scope)
        result = get_countries(self.scope)
        print("result", result)
        if result == None:
            return []
        else:
            return [[result['TotalConfirmed'], result['TotalDeaths'], result['TotalRecovered']]]

    def get_context_data(self, **kwargs):
        self.scope = kwargs['id']
        context = super().get_context_data(**kwargs)
        return context


class Principal(View):
    def get(self, request, *args, **kwargs):
        try:
            countries = get_countries('countries')
            return render(request, "graf.html", {
                'countries': countries
            })
        except error:

            return render(request, "graf.html", {
                'countries': []
            })
