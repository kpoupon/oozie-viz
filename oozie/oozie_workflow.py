# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import basename
from xml.etree import ElementTree
from oozie.oozie_actions import *


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
            elif tag == "fork":
                actions.append(OozieFork(markup))
            elif tag == "join":
                actions.append(OozieJoin(markup))
            elif tag == "decision":
                actions.append(OozieDecision(markup))
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

        return actions
