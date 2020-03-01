class Turn:
    all = [[], []]
    current = []
    turn_team = 1

    @staticmethod
    def update():
        queue = []
        while Turn.current:
            r = Turn.current.pop()
            if not r():
                queue.append(r)
        if queue:
            Turn.current = queue
        else:
            Turn.turn_team += 1
            if Turn.turn_team >= len(Turn.all):
                Turn.turn_team = 0
            Turn.current = Turn.all[Turn.turn_team].copy()

    @staticmethod
    def add(index, arg):
        Turn.all[index].append(arg)

    @staticmethod
    def remove(arg):
        for i in Turn.all:
            if arg in i:
                i.remove(arg)
