#!/usr/bin/env python3

import datetime
import os
import orgparse

class AgendaItem:

    def __init__(self, heading, status, tags=None, properties=None, parent=None):
        self.heading = heading
        self.status = status
        self.tags = tags or {}
        self.properties = properties or {}
        self.parent = parent
        # caching:
        self._timestamp = None

    def __str__(self):
        return f"{self.status} {self.heading}"

    def last_state_change(self):
        if not self._timestamp:
            if 'last-state-change' in self.properties:
                iso = self.properties['last-state-change']
                self._timestamp = datetime.datetime.fromisoformat(iso[1:11] + "T" + iso[16:21])
        return self._timestamp

    def longname(self):
        return self.heading + (""
                               if self.parent is None
                               else (" (in " + self.parent + ")"))

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
            results.append(AgendaItem(entry.get_heading(),
                                      status=entry.todo,
                                      tags=entry.tags,
                                      properties=entry.properties,
                                      parent=(None
                                              if isinstance(entry.get_parent(), orgparse.node.OrgRootNode)
                                              else entry.get_parent().get_heading())))
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
    print("Ordered item:", item, item.last_state_change())

for item in load_agenda_file("$ORG/learning.org",
                             require_todo="OPEN",
                             n_results=6,
                             ):
    print("Learning:", item)
