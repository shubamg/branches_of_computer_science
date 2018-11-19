class Node:

    def __init__(self, __id, label, parent):
        self.__id = __id
        self.label = label
        self.parent = parent
        self.description = []
        self.children = []

    def append_description(self, text_to_append):
        self.description.append(text_to_append)

    def get_id(self):
        return self.__id

    def append_child(self, child_node):
        self.children.append(child_node)

    def get_children(self):
        return self.children

    def get_label(self):
        return self.label

    def __str__(self):
        parent_id = ''
        ids_of_children = [child_node.get_id() for child_node in self.children]
        if self.parent:
            parent_id = self.parent.get_id()
        return '{{Id:{0}\nlabel:{1}\nparent:{2}\nchildren:{3}\ndescription:[{4}]}}'.format(
            self.get_id(), self.label, parent_id, ids_of_children, '\n'.join(self.description)
        )
