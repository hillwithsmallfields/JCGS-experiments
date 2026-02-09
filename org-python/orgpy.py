#!/usr/bin/env python3

import os
import orgparse

def load_agenda_file(filename,
                     n_results=None,
                     require_todo=None,
                     require_tag=None):
    base_node = orgparse.load(os.path.expandvars(filename))
    todo_keys = base_node.env.todo_keys
    results = []

    def add_entry_conditionally(entry):
        if ((entry.todo == require_todo
             if require_todo
             else entry.todo in todo_keys)
            and (require_tag is None
                 or require_tag in entry.tags)):
            results.append((entry.get_heading() + (""
                                                   if isinstance(entry.get_parent(), orgparse.node.OrgRootNode)
                                                   else (" (in " + entry.get_parent().get_heading() + ")")),
                            entry.todo,
                            entry.tags))

    for top_entry in base_node.children:
        if top_entry.children:
            for sub_entry in top_entry.children:
                add_entry_conditionally(sub_entry)
                if n_results and len(results) == n_results:
                    break
        else:
            add_entry_conditionally(top_entry)
            if n_results and len(results) == n_results:
                break
    return results

for entry in load_agenda_file("$ORG/projects.org",
                              n_results=12,
                              require_tag="@Makespace"):
    print(entry)

for item in load_agenda_file("$ORG/shopping.org",
                             require_todo="ORDERED"):
    print("Ordered item:", item)
