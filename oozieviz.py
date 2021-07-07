# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from abc import ABC
from os.path import basename
from xml.etree import ElementTree
# from graphviz import Digraph


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workflow_path", help="Path of the Oozie workflow to visualize", required=True)
    arguments = parser.parse_args()
    return arguments


class OozieVisitor(ABC):
    def visit_start(self, oozie_start):
        pass

    def visit_end(self, oozie_end):
        pass

    def visit_kill(self, oozie_kill):
        pass

    def visit_shell(self, oozie_shell):
        pass

    def visit_hive(self, oozie_hive):
        pass

    def visit_subwf(self, oozie_subwf):
        pass

    def visit_email(self, oozie_email):
        pass

    def visit_decision(self, oozie_decision):
        pass


class OozieGraphViz01(OozieVisitor):
    def visit_start(self, oozie_start):
        print("=== start")

    def visit_end(self, oozie_end):
        print("=== end")

    def visit_kill(self, oozie_kill):
        print("=== kill")

    def visit_shell(self, oozie_shell):
        print("=== shell")

    def visit_hive(self, oozie_hive):
        print("=== hive")

    def visit_subwf(self, oozie_subwf):
        print("=== subwf")

    def visit_email(self, oozie_email):
        print("=== email")

    def visit_decision(self, oozie_decision):
        print("=== decision")


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
                actions.append(OozieStart())
            elif tag == "end":
                actions.append(OozieEnd())
            elif tag == "kill":
                actions.append(OozieKill())
            elif tag == "action":
                action_type = markup[0].tag.split("}", 1)[1]

                if action_type == "shell":
                    # TODO : passer la markup au constructeur de l'action, afin que l'action puisse en extraire des infos spécifiques
                    # actions.append(OozieShell(markup))
                    actions.append(OozieShell())
                elif action_type == "hive":
                    actions.append(OozieHive())
                elif action_type == "sub-workflow":
                    actions.append(OozieSubWf())
                elif action_type == "email":
                    actions.append(OozieEmail())
            elif tag == "decision":
                actions.append(OozieDecision())

        return actions

    def accept(self, visitor: OozieVisitor):
        for action in self.actions:
            action.accept(visitor)


class OozieAction(ABC):
    def accept(self, visitor: OozieVisitor):
        pass


class OozieStart(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_start(self)


class OozieEnd(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_end(self)


class OozieKill(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_kill(self)


class OozieShell(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_shell(self)


class OozieHive(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_hive(self)


class OozieSubWf(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_subwf(self)


class OozieEmail(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_email(self)


class OozieDecision(OozieAction):
    def accept(self, visitor: OozieVisitor):
        visitor.visit_decision(self)


# Script entry point
if __name__ == "__main__":
    args = parse_args()

    visitor = OozieGraphViz01()
    workflow = OozieWorkflow(args.workflow_path)

    workflow.accept(visitor)
