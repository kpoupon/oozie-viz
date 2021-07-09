# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from abc import ABC
from os.path import basename
from xml.etree import ElementTree
from graphviz import Digraph


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workflow_path", help="Path of the Oozie workflow to visualize", required=True)
    arguments = parser.parse_args()
    return arguments


class OozieVisitor(ABC):
    def visit(self, oozie_workflow):
        pass

    def create_node_start(self, oozie_start):
        pass

    def connect_node_start(self, oozie_start):
        pass

    def create_node_end(self, oozie_end):
        pass

    def connect_node_end(self, oozie_end):
        pass

    def create_node_kill(self, oozie_kill):
        pass

    def connect_node_kill(self, oozie_kill):
        pass

    def create_node_shell(self, oozie_shell):
        pass

    def connect_node_shell(self, oozie_shell):
        pass

    def create_node_hive(self, oozie_hive):
        pass

    def connect_node_hive(self, oozie_hive):
        pass

    def create_node_subwf(self, oozie_subwf):
        pass

    def connect_node_subwf(self, oozie_subwf):
        pass

    def create_node_email(self, oozie_email):
        pass

    def connect_node_email(self, oozie_email):
        pass

    def create_node_decision(self, oozie_decision):
        pass

    def connect_node_decision(self, oozie_decision):
        pass


class OozieGraphViz01(OozieVisitor):
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
            action.accept_creation(visitor)

        for action in oozie_workflow.actions:
            action.accept_connection(visitor)

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


class OozieWorkflow:
    def __init__(self, workflow_path):
        self.wf_path = workflow_path
        self.wf_name = basename(workflow_path)
        self.root = ElementTree.parse(workflow_path).getroot()
        self.actions = self.list_actions()

    def list_actions(self):
        actions = list()

        for markup in self.root:
            tag = markup.tag.split("}", 1)[1]

            if tag == "start":
                actions.append(OozieStart(markup))
            elif tag == "end":
                actions.append(OozieEnd(markup))
            elif tag == "kill":
                actions.append(OozieKill(markup))
            elif tag == "action":
                action_type = markup[0].tag.split("}", 1)[1]

                if action_type == "shell":
                    actions.append(OozieShell(markup))
                elif action_type == "hive":
                    actions.append(OozieHive(markup))
                elif action_type == "sub-workflow":
                    actions.append(OozieSubWf(markup))
                elif action_type == "email":
                    actions.append(OozieEmail(markup))
            elif tag == "decision":
                actions.append(OozieDecision(markup))

        return actions


class OozieAction(ABC):
    def accept_creation(self, visitor: OozieVisitor):
        pass

    def accept_connection(self, visitor: OozieVisitor):
        pass


class OozieStart(OozieAction):
    def __init__(self, markup):
        self.action_type = 'start'
        self.action_name = 'start'
        self.to = markup.attrib['to']

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_start(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_start(self)


class OozieEnd(OozieAction):
    def __init__(self, markup):
        self.action_type = 'end'
        self.action_name = markup.attrib['name']

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_end(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_end(self)


class OozieKill(OozieAction):
    def __init__(self, markup):
        self.action_type = 'kill'
        self.action_name = markup.attrib['name']

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_kill(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_kill(self)


class OozieShell(OozieAction):
    def __init__(self, markup):
        self.action_type = 'shell'
        self.action_name = markup.attrib['name']
        self.job_tracker = None
        self.name_node = None
        self.exec = None
        self.arguments = None
        self.files = None
        self.ok = markup[1].attrib['to']
        self.error = markup[2].attrib['to']

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_shell(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_shell(self)


class OozieHive(OozieAction):
    def __init__(self, markup):
        self.action_type = 'hive'
        self.action_name = markup.attrib['name']
        self.job_tracker = None
        self.name_node = None
        self.script = None
        self.ok = markup[1].attrib['to']
        self.error = markup[2].attrib['to']

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_hive(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_hive(self)


class OozieSubWf(OozieAction):
    def __init__(self, markup):
        self.action_type = 'sub-workflow'
        self.action_name = markup.attrib['name']
        self.ok = markup[1].attrib['to']
        self.error = markup[2].attrib['to']

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_subwf(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_subwf(self)


class OozieEmail(OozieAction):
    def __init__(self, markup):
        self.action_type = 'email'
        self.action_name = markup.attrib['name']
        self.ok = markup[1].attrib['to']
        self.error = markup[2].attrib['to']

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_email(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_email(self)


class OozieDecision(OozieAction):
    def __init__(self, markup):
        self.action_type = 'decision'
        self.action_name = markup.attrib['name']
        self.cases = []

        for m in markup[0]:
            self.cases.append(m.attrib['to'])

    def accept_creation(self, visitor: OozieVisitor):
        visitor.create_node_decision(self)

    def accept_connection(self, visitor: OozieVisitor):
        visitor.connect_node_decision(self)


# Script entry point
if __name__ == "__main__":
    args = parse_args()

    # Oozie workflow modeling as a collection of OozieAction
    workflow = OozieWorkflow(args.workflow_path)

    # GraphViz visitor instantiation
    visitor = OozieGraphViz01(workflow.wf_name)
    visitor.visit(workflow)
