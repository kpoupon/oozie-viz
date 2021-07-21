# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC


class AbstractVisitor(ABC):
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

    def create_node_fork(self, oozie_fork):
        pass

    def connect_node_fork(self, oozie_fork):
        pass

    def create_node_join(self, oozie_join):
        pass

    def connect_node_join(self, oozie_join):
        pass

    def create_node_email(self, oozie_email):
        pass

    def connect_node_email(self, oozie_email):
        pass

    def create_node_decision(self, oozie_decision):
        pass

    def connect_node_decision(self, oozie_decision):
        pass
