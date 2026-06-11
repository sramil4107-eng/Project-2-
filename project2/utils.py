from logic import Stack, Operation
from typing import Optional

class InputHandler:

    @staticmethod
    def read_int(prompt: str,
                 min_val: Optional[int] = None,
                 max_val: Optional[int] = None) -> int:

        while True:
            raw: str = input(prompt).strip()
            is_negative: bool = raw.startswith('-') and raw[1:].isdigit()

            if not raw.isdigit() and not is_negative:
                print("Ошибка: введите целое число.")
                continue

            value: int = int(raw)

            if min_val is not None and value < min_val:
                print(f"Ошибка: значение должно быть не менее {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Ошибка: значение должно быть не более {max_val}.")
                continue

            return value

    @staticmethod
    def read_stacks(n: int) -> list[Stack]:
        stacks: list[Stack] = []

        print(f"\nВведите описание {n} стопок.")
        print("Для каждой: количество контейнеров, затем их виды (снизу вверх).")
        print("0 — пустая стопка.\n")

        for i in range(n):
            print(f"  Стопка {i + 1}:")
            k: int = InputHandler.read_int(
                "    Количество контейнеров: ", min_val=0, max_val=500
            )

            if k == 0:
                stacks.append(Stack())
                continue

            while True:
                raw: str = input(
                    f"    Виды контейнеров (снизу вверх, {k} чисел): "
                ).strip()
                parts: list[str] = raw.split()

                if len(parts) != k:
                    print(f"Ошибка: нужно ровно {k} чисел.")
                    continue

                valid: bool = True
                types: list[int] = []

                for part in parts:
                    if not part.isdigit() or int(part) < 1 or int(part) > n:
                        print(f"Ошибка: вид контейнера должен быть от 1 до {n}.")
                        valid = False
                        break
                    types.append(int(part))

                if valid:
                    stacks.append(Stack(types))
                    break

        return stacks

class OutputHandler:

    @staticmethod
    def print_result(operations: Optional[list[Operation]]) -> None:

        print()
        if operations is None:
            print("  Результат: 0  (задача не имеет решения)")
        elif len(operations) == 0:
            print("  Контейнеры уже расставлены правильно. Операций не требуется.")
        else:
            print(f"  Последовательность операций ({len(operations)} шт.):")
            from_stack: int
            to_stack: int
            for from_stack, to_stack in operations:
                print(f"    {from_stack} {to_stack}")
        print()