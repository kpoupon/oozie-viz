# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from visitor.abstract_visitor import AbstractVisitor
from graphviz import Digraph


class GraphVizVisitor01(AbstractVisitor):
    def __init__(self, wf_name):
        self.wf_name = wf_name
        self.graph = Digraph(wf_name, filename=f'renderings/{wf_name}.gv', format='svg')

        self.graph.attr('node', {
            'fontname': 'consolas'
        })
        self.graph.attr('edge', {
            'fontname': 'consolas'
        })

    def visit(self, oozie_workflow):
        for action in oozie_workflow.actions:
            action.accept_creation(self)

        for action in oozie_workflow.actions:
            action.accept_connection(self)

        self.graph.view()

    def create_node_start(self, oozie_start):
        self.graph.attr('node', {
            'shape': 'doublecircle',
            'color': 'green'
        })
        self.graph.node(oozie_start.action_name, oozie_start.action_name)

    def connect_node_start(self, oozie_start):
        self.graph.edge(oozie_start.action_name, oozie_start.to)

    def create_node_end(self, oozie_end):
        self.graph.attr('node', {
            'shape': 'doublecircle',
            'color': 'green'
        })
        self.graph.node(oozie_end.action_name, oozie_end.action_name)

    def create_node_kill(self, oozie_kill):
        self.graph.attr('node', {
            'shape': 'doublecircle',
            'color': 'red'
        })
        self.graph.node(oozie_kill.action_name, oozie_kill.action_name)

    def create_node_shell(self, oozie_shell):
        self.graph.attr('node', {
            'shape': 'box',
            'color': 'grey'
        })
        self.graph.node(oozie_shell.action_name, oozie_shell.action_name)

    def connect_node_shell(self, oozie_shell):
        self.graph.edge(oozie_shell.action_name, oozie_shell.ok, label='ok', color='green', fontcolor='green')
        self.graph.edge(oozie_shell.action_name, oozie_shell.error, label='error', color='red', fontcolor='red')

    def create_node_hive(self, oozie_hive):
        self.graph.attr('node', {
            'shape': 'box',
            'color': 'grey'
        })
        self.graph.node(oozie_hive.action_name, oozie_hive.action_name)

    def connect_node_hive(self, oozie_hive):
        self.graph.edge(oozie_hive.action_name, oozie_hive.ok, label='ok', color='green', fontcolor='green')
        self.graph.edge(oozie_hive.action_name, oozie_hive.error, label='error', color='red', fontcolor='red')

    def create_node_subwf(self, oozie_subwf):
        self.graph.attr('node', {
            'shape': 'box3d',
            'color': 'grey'
        })
        self.graph.node(oozie_subwf.action_name, oozie_subwf.action_name)

    def connect_node_subwf(self, oozie_subwf):
        self.graph.edge(oozie_subwf.action_name, oozie_subwf.ok, label='ok', color='green', fontcolor='green')
        self.graph.edge(oozie_subwf.action_name, oozie_subwf.error, label='error', color='red', fontcolor='red')

    def create_node_email(self, oozie_email):
        self.graph.attr('node', {
            'shape': 'box',
            'color': 'grey'
        })
        self.graph.node(oozie_email.action_name, oozie_email.action_name)

    def connect_node_email(self, oozie_email):
        self.graph.edge(oozie_email.action_name, oozie_email.ok, label='ok', color='green', fontcolor='green')
        self.graph.edge(oozie_email.action_name, oozie_email.error, label='error', color='red', fontcolor='red')

    def create_node_decision(self, oozie_decision):
        self.graph.attr('node', {
            'shape': 'hexagon',
            'color': 'goldenrod2'
        })
        self.graph.node(oozie_decision.action_name, oozie_decision.action_name)

    def connect_node_decision(self, oozie_decision):
        for case in oozie_decision.cases:
            self.graph.edge(oozie_decision.action_name, case)
