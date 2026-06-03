import copy
from collections import deque
from typing import Optional

# Тип для состояния (хешируемый кортеж кортежей)
State = tuple[tuple[int, ...], ...]

# Тип для одной операции (from_stack, to_stack), нумерация с 1
Operation = tuple[int, int]

# Тип для списка стопок
Stacks = list[list[int]]

BFS_LIMIT: int = 20  # при ≤ 20 контейнерах используем BFS, иначе — жадный

# Вспомогательные функции

def is_sorted(stacks: Stacks) -> bool:
    for i, stack in enumerate(stacks):
        if any(c != i + 1 for c in stack):
            return False
    return True

def to_state(stacks: Stacks) -> State:
    return tuple(tuple(s) for s in stacks)

def from_state(state: State) -> Stacks:
    return [list(s) for s in state]

def total_containers(stacks: Stacks) -> int:
    return sum(len(s) for s in stacks)

#BFS-решатель

def solve_bfs(stacks_input: Stacks) -> Optional[list[Operation]]:

    n: int = len(stacks_input)

    if is_sorted(stacks_input):
        return []

    start: State = to_state(stacks_input)

    # parent[state] хранит (предыдущее_состояние, из_стопки, в_стопку)
    parent: dict[State, Optional[tuple[State, int, int]]] = {start: None}
    queue: deque[State] = deque([start])

    while queue:
        cur_state: State = queue.popleft()
        cur: Stacks = from_state(cur_state)

        for src in range(n):
            if not cur[src]:
                continue

            top: int = cur[src][-1]

            for dst in range(n):
                if dst == src:
                    continue

                # Выполняем ход: берём верхний из src, кладём в dst
                next_stacks: Stacks = from_state(cur_state)
                next_stacks[src].pop()
                next_stacks[dst].append(top)
                ns: State = to_state(next_stacks)

                if ns in parent:
                    continue

                parent[ns] = (cur_state, src + 1, dst + 1)

                if is_sorted(next_stacks):
                    # Восстанавливаем путь от финального состояния к начальному
                    ops: list[Operation] = []
                    state: State = ns
                    while parent[state] is not None:
                        prev_state, f, t = parent[state]  # type: ignore[misc]
                        ops.append((f, t))
                        state = prev_state
                    ops.reverse()
                    return ops

                queue.append(ns)

    return None  # решения нет

#Жадный решатель для больших данных

def solve_greedy(stacks_input: Stacks) -> Optional[list[Operation]]:
    stacks: Stacks = copy.deepcopy(stacks_input)
    n: int = len(stacks)
    operations: list[Operation] = []
    max_ops: int = n * 500 * (n + 1) * 20 + 1

    while not is_sorted(stacks):
        moved: bool = False

        # Приоритет 1: прямой ход в целевую стопку
        for src in range(n):
            if not stacks[src]:
                continue
            top: int = stacks[src][-1]
            dst: int = top - 1  # индекс целевой стопки (0-based)
            if dst == src:
                continue
            if all(c == top for c in stacks[dst]):
                stacks[src].pop()
                stacks[dst].append(top)
                operations.append((src + 1, dst + 1))
                moved = True
                if len(operations) > max_ops:
                    return None
                break

        if moved:
            continue

        # Приоритет 2: буферный ход — верхний «чужой» в любую пустую стопку
        for src in range(n):
            if not stacks[src]:
                continue
            top = stacks[src][-1]
            # Пропускаем контейнеры, которые уже на правильном месте
            if src == top - 1 and all(c == top for c in stacks[src]):
                continue

            for buf in range(n):
                if buf == src or stacks[buf]:
                    continue
                stacks[src].pop()
                stacks[buf].append(top)
                operations.append((src + 1, buf + 1))
                moved = True
                if len(operations) > max_ops:
                    return None
                break
            if moved:
                break

        if not moved:
            return None  # тупик — задача не имеет решения

    return operations

#Главная функция

def solve(stacks_input: Stacks) -> Optional[list[Operation]]:
    total: int = total_containers(stacks_input)
    if total <= BFS_LIMIT:
        return solve_bfs(stacks_input)
    return solve_greedy(stacks_input)