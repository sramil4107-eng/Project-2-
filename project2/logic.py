class Stack:

    def __init__(self, items: list[int] | None = None) -> None:
        #Внутреннее хранилище — список; items[0] — дно, items[-1] — верх
        self._data: list[int] = list(items) if items else []

    def push(self, item: int) -> None:
        self._data.append(item)

    def pop(self) -> int:
        return self._data.pop()

    def peek(self) -> int:
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def to_tuple(self) -> tuple[int, ...]:
        return tuple(self._data)

    def copy(self) -> "Stack":
        return Stack(list(self._data))

    def is_sorted(self, target_type: int) -> bool:
        return all(c == target_type for c in self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"

# Класс Queue — очередь для BFS


class Queue:
    def __init__(self) -> None:
        self._data: list = []
        self._head: int = 0  # индекс первого непрочитанного элемента

    def enqueue(self, item) -> None:
        self._data.append(item)

    def dequeue(self):
        item = self._data[self._head]
        self._head += 1
        # Периодически чистим обработанную часть, чтобы не росла память
        if self._head > 1000:
            self._data = self._data[self._head:]
            self._head = 0
        return item

    def is_empty(self) -> bool:
        return self._head >= len(self._data)



# Класс Solver — решатель задачи


# Тип псевдонимов
State     = tuple[tuple[int, ...], ...]
Operation = tuple[int, int]

BFS_LIMIT: int = 20  # при ≤ 20 контейнерах — BFS, иначе жадный


class Solver:
    def __init__(self, stacks: list[Stack]) -> None:
        self._n: int = len(stacks)
        self._stacks: list[Stack] = stacks

    #Вспомогательные методы

    def _total(self) -> int:
        return sum(s.size() for s in self._stacks)

    @staticmethod
    def _is_state_sorted(state: State) -> bool:
        for i, tup in enumerate(state):
            if any(c != i + 1 for c in tup):
                return False
        return True

    @staticmethod
    def _stacks_from_state(state: State) -> list[Stack]:
        return [Stack(list(tup)) for tup in state]

    @staticmethod
    def _state_from_stacks(stacks: list[Stack]) -> State:
        return tuple(s.to_tuple() for s in stacks)

    def _is_sorted(self, stacks: list[Stack]) -> bool:
        for i, stack in enumerate(stacks):
            if not stack.is_sorted(i + 1):
                return False
        return True

    #BFS

    def _solve_bfs(self) -> list[Operation] | None:

        start: State = self._state_from_stacks(self._stacks)

        if self._is_state_sorted(start):
            return []

        # parent[state] = (предыдущее_состояние, из_стопки, в_стопку)
        parent: dict[State, tuple[State, int, int] | None] = {start: None}
        queue: Queue = Queue()
        queue.enqueue(start)

        while not queue.is_empty():
            cur_state: State = queue.dequeue()
            cur: list[Stack] = self._stacks_from_state(cur_state)

            for src in range(self._n):
                if cur[src].is_empty():
                    continue

                top: int = cur[src].peek()

                for dst in range(self._n):
                    if dst == src:
                        continue

                    # Выполняем ход
                    next_stacks: list[Stack] = self._stacks_from_state(cur_state)
                    next_stacks[src].pop()
                    next_stacks[dst].push(top)
                    ns: State = self._state_from_stacks(next_stacks)

                    if ns in parent:
                        continue

                    parent[ns] = (cur_state, src + 1, dst + 1)

                    if self._is_state_sorted(ns):
                        # Восстанавливаем путь
                        ops: list[Operation] = []
                        state: State = ns
                        while parent[state] is not None:
                            prev, f, t = parent[state]
                            ops.append((f, t))
                            state = prev
                        ops.reverse()
                        return ops

                    queue.enqueue(ns)

        return None  # решения нет

    #Жадный алгоритм

    def _solve_greedy(self) -> list[Operation] | None:
        # Работаем на копиях, чтобы не менять исходные данные
        stacks: list[Stack] = [s.copy() for s in self._stacks]
        operations: list[Operation] = []
        max_ops: int = self._n * 500 * (self._n + 1) * 20 + 1

        while not self._is_sorted(stacks):
            moved: bool = False

            # Приоритет 1: прямой ход
            for src in range(self._n):
                if stacks[src].is_empty():
                    continue
                top: int = stacks[src].peek()
                dst: int = top - 1  # индекс целевой стопки (0-based)
                if dst == src:
                    continue
                if stacks[dst].is_sorted(top):  # пустая или только такой вид
                    stacks[src].pop()
                    stacks[dst].push(top)
                    operations.append((src + 1, dst + 1))
                    moved = True
                    if len(operations) > max_ops:
                        return None
                    break

            if moved:
                continue

            # Приоритет 2: буферный ход в пустую стопку
            for src in range(self._n):
                if stacks[src].is_empty():
                    continue
                top = stacks[src].peek()
                # Пропускаем контейнеры, которые уже на месте
                if src == top - 1 and stacks[src].is_sorted(top):
                    continue

                for buf in range(self._n):
                    if buf == src or not stacks[buf].is_empty():
                        continue
                    stacks[src].pop()
                    stacks[buf].push(top)
                    operations.append((src + 1, buf + 1))
                    moved = True
                    if len(operations) > max_ops:
                        return None
                    break
                if moved:
                    break

            if not moved:
                return None  # тупик

        return operations

#Главный метод

    def solve(self) -> list[Operation] | None:
        if self._total() <= BFS_LIMIT:
            return self._solve_bfs()
        return self._solve_greedy()