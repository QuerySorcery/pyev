from pyev import Visualizer
import json


def visualize():
    with open("query_plan_full.json") as json_file:
        explains = json.load(json_file)
        for explain in explains:
            v = Visualizer(110)
            v.load(explain)
            v.print()


visualize()
