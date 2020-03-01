from game.Tile import Tile


class Task:
    def __init__(self, host):
        self.host = host

    def perform(self):
        pass

    def update(self):
        pass


class Path(Task):  # path finding A*
    chase = 3

    @staticmethod
    def get_routes(pos):
        options = []
        left = pos.get_neighbor(-1, 0)
        right = pos.get_neighbor(1, 0)
        down = pos.get_neighbor(0, 1)
        up = pos.get_neighbor(0, -1)
        if up and not up.is_land(Tile.CHECK_FIRM):
            options.append((0, -1))
        if right and not right.is_land(Tile.CHECK_FIRM):
            options.append((1, 0))
        if left and not left.is_land(Tile.CHECK_FIRM):
            options.append((-1, 0))
        if down and not down.is_land(Tile.CHECK_FIRM):
            options.append((0, 1))
        return options

    class Node:
        def __init__(self, parent, node):
            self.parent = parent
            self.node = node
            self.g = 0
            self.h = 0
            self.f = self.g + self.h

        def set_h(self, destination):
            self.h = (self.node - destination).distance()

        def __str__(self):
            return self.node.__str__()+'/'+str(self.f)

    def __init__(self, pilot):
        super().__init__(pilot)
        self.target = self.host.pos
        self.open = None
        self.closed = []
        self.closest = None
        self.result = []
        self.next_reset = 0
        self.heuristic_threshold = 0
        self.out_of_reach = False

    def iterate(self, node):
        index = 0
        for k, v in enumerate(self.open):
            if v.f < node.f:
                index = k
                node = v
        self.open.pop(index)
        self.closed.append(node)
        achieved = (node.node - self.target).difference()
        if achieved <= 1:
            return node
        if achieved < (self.closest.node - self.target).difference():
            self.closest = node
        options = Path.get_routes(node.node)
        for i in options:
            pos = node.node.get_neighbor(i[0], i[1])
            if self.check_loop(self.closed, pos):
                continue
            conflict = self.check_loop(self.open, pos)
            if conflict:
                if node.g + 1 <= conflict.g:
                    conflict.parent = node
                    conflict.g = node.g + 1 + node.node.type
                    conflict.set_h(self.target)
                    conflict.f = conflict.h + conflict.g
                continue
            new = Path.Node(node, pos)
            new.g = node.g + 1 + node.node.type
            new.set_h(self.target)
            new.f = new.h + new.g
            if new.h < self.heuristic_threshold:
                self.open.append(new)

    @staticmethod
    def check_loop(loop, pos):
        for i in loop:
            if i.node == pos:
                return i

    def perform(self):
        if self.result:
            self.host.face_toward(self.result[0])
            self.host.input('walk')
            self.result = []
        if (self.host.pos - self.target).difference() <= 1:
            return True

    def update(self):
        super().update()
        if not self.result and (self.host.pos - self.target).difference() > 1:
            done = None
            if self.next_reset == 0:
                self.reset()
                self.next_reset = 1
            else:
                self.next_reset += 1
            for times in range(16):
                if self.open:
                    done = self.iterate(self.open[0])
                    if done:
                        break
                else:
                    break
            # self.debug_trace()
            if not done and self.next_reset > Path.chase:
                self.out_of_reach = True
                done = self.closest
            if done:
                self.next_reset = 0
                self.result = [done.node]
                while done.parent:
                    done = done.parent
                    if done.node == self.host.pos:
                        break
                    self.result.insert(0, done.node)

    def reset(self):
        self.heuristic_threshold = (self.host.pos - self.target).distance() * 2 + 4
        self.open = [Path.Node(None, self.host.pos)]
        self.closed = []
        self.closest = self.open[0]


class Attack(Task):
    def __init__(self, pilot):
        super().__init__(pilot)
        self.move = Path(pilot)
        self.target = None

    def update(self):
        super().update()
        if self.target and self.target.removed == 0:
            self.move.target = self.target.pos
            self.move.update()

    def perform(self):
        if self.target:
            dist = self.target.pos - self.host.pos
            if dist.difference() == 1:
                self.host.face_toward(self.target.pos)
                self.host.input('walk')
            elif self.move.out_of_reach:
                self.move.target = self.target.pos
                self.move.perform()
            else:
                self.move.target = self.target.pos
                self.move.perform()
