class Tag:
    def __init__(self):
        self.attributes = {}

    def __str__(self):
        if not self.attributes:
            return '[]'
        var = []
        for k, v in self.attributes.items():
            var.append(k + ':' + str(v))
        return '[' + ','.join(var) + ']'

    def load(self, arg):
        for i in arg:
            strings = i.split(':')
            if len(strings) > 1:
                if strings[1][0].isdigit() or strings[1][0] == '-':
                    self.attributes[strings[0]] = int(strings[1])
                else:
                    self.attributes[strings[0]] = strings[1]

    def remove(self, param, default=None):
        if param in self.attributes:
            r = self.attributes[param]
            del self.attributes[param]
            return r
        return default

    def get(self, param, default=None):
        if param in self.attributes:
            return self.attributes[param]
        return default

    def set(self, param, arg, add=False):
        if param in self.attributes or add:
            self.attributes[param] = arg
            return True

    def increment(self, param, arg, add=False, remove=False):
        if param in self.attributes:
            self.attributes[param] += arg
            if remove:
                if self.attributes[param] == 0:
                    del self.attributes[param]
            return True
        elif add:
            self.attributes[param] = arg
            return True
