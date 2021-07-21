# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from visitor.abstract_visitor import AbstractVisitor


class OozieAction(ABC):
    def accept_creation(self, visitor: AbstractVisitor):
        pass

    def accept_connection(self, visitor: AbstractVisitor):
        pass


class OozieStart(OozieAction):
    def __init__(self, markup):
        self.action_type = 'start'
        self.action_name = 'start'
        self.to = markup.attrib['to']

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_start(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_start(self)


class OozieEnd(OozieAction):
    def __init__(self, markup):
        self.action_type = 'end'
        self.action_name = markup.attrib['name']

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_end(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_end(self)


class OozieKill(OozieAction):
    def __init__(self, markup):
        self.action_type = 'kill'
        self.action_name = markup.attrib['name']

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_kill(self)

    def accept_connection(self, visitor: AbstractVisitor):
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

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_shell(self)

    def accept_connection(self, visitor: AbstractVisitor):
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

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_hive(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_hive(self)


class OozieSubWf(OozieAction):
    def __init__(self, markup):
        self.action_type = 'sub-workflow'
        self.action_name = markup.attrib['name']
        self.ok = markup[1].attrib['to']
        self.error = markup[2].attrib['to']

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_subwf(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_subwf(self)


class OozieFork(OozieAction):
    def __init__(self, markup):
        self.action_type = 'fork'
        self.action_name = markup.attrib['name']
        self.paths = []

        for m in markup:
            self.paths.append(m.attrib['start'])

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_fork(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_fork(self)


class OozieJoin(OozieAction):
    def __init__(self, markup):
        self.action_type = 'join'
        self.action_name = markup.attrib['name']
        self.to = markup.attrib['to']

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_join(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_join(self)


class OozieEmail(OozieAction):
    def __init__(self, markup):
        self.action_type = 'email'
        self.action_name = markup.attrib['name']
        self.ok = markup[1].attrib['to']
        self.error = markup[2].attrib['to']

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_email(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_email(self)


class OozieDecision(OozieAction):
    def __init__(self, markup):
        self.action_type = 'decision'
        self.action_name = markup.attrib['name']
        self.cases = []

        for m in markup[0]:
            self.cases.append(m.attrib['to'])

    def accept_creation(self, visitor: AbstractVisitor):
        visitor.create_node_decision(self)

    def accept_connection(self, visitor: AbstractVisitor):
        visitor.connect_node_decision(self)
