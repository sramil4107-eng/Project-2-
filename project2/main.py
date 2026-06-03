from logic import solve
from utils import input_stacks, input_int, print_result
from typing import Optional

Operation = tuple[int, int]

SEPARATOR: str = "─" * 50

def print_menu() -> None:
    print(SEPARATOR)
    print("     КОНТЕЙНЕРЫ — Автопогрузчик")
    print(SEPARATOR)
    print("  1. Решить задачу (ввод с клавиатуры)")
    print("  0. Выход")
    print(SEPARATOR)

def run_solver() -> None:
    print()
    n: int = input_int("Введите число видов контейнеров N (1–500): ",
                       min_val=1, max_val=500)

    stacks: list[list[int]] = input_stacks(n)

    print("\n  Решаю задачу...")
    operations: Optional[list[Operation]] = solve(stacks)
    print_result(operations)

def main() -> None:
    print()
    print("Добро пожаловать в программу «Контейнеры»!")
    print()

    while True:
        print_menu()
        choice: str = input("Выберите пункт меню: ").strip()

        if choice == "1":
            run_solver()
        elif choice == "0":
            print()
            print("До свидания!")
            print()
            break
        else:
            print()
            print("Неверный пункт меню. Введите 1 или 0.")
            print()

if __name__ == "__main__":
    main()