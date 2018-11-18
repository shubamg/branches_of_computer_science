class Node:

    def __init__(self, __id, label, parent, line_of_description=None):
        self.__id = __id
        self.label = label
        self.parent = parent
        self.description = []
        if line_of_description:
            self.description.append(line_of_description)

    def append_description(self, text_to_append):
        self.description.append(text_to_append)

    def get_id(self):
        return self.__id

    def __str__(self):
        parent_id = ''
        if self.parent:
            parent_id = self.parent.get_id()
        return '{{Id:{0}\nlabel:{1}\nparent:{2}\ndescription:[{3}]}}'.format(
            self.get_id(), self.label, parent_id, '\n'.join(self.description)
        )