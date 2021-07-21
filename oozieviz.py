# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import configparser

from oozie.oozie_workflow import OozieWorkflow
from visitor.graphviz_visitor import GraphVizVisitor01


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workflow_path", help="Path of the Oozie workflow to visualize", required=True)
    arguments = parser.parse_args()
    return arguments


# Script entry point
if __name__ == "__main__":
    args = parse_args()

    # Property file parsing
    config = configparser.ConfigParser()
    config.read('graphviz_conf.ini')

    # Oozie workflow modeling as a collection of OozieAction
    workflow = OozieWorkflow(args.workflow_path)

    # GraphViz visitor instantiation
    visitor = GraphVizVisitor01(workflow.wf_name, config)
    visitor.visit(workflow)
