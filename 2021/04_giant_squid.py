from typing import Dict, List, Set
from util import get_input


class Board:
    """
    Representation of a bingo board.

    Numbers are removed from the board when they are "marked".
    """

    def __init__(self, board: List[List[int]]) -> None:
        # rows in the bingo board, indexed by number
        self._rows: Dict[int, List[int]] = self._index_list_by_values(board)
        # columns in the bingo board, indexed by number
        self._cols: Dict[int, List[int]] = self._index_list_by_values(self._get_cols(board))
        # True if the board has achieved bingo
        self.bingo: bool = False

    def mark_number(self, num: int) -> None:
        """
        Update the internal state of the board by removing the provided
        number. If bingo is achieved, self.bingo will be True
        """

        def remove_num_from_index(index: Dict[int, List[int]]) -> None:
            """
            Delete num from the index's backing list,
            and remove the index entry.

            self.bingo will be updated here if bingo is achieved
            """
            if num in index:
                index[num].remove(num)
                nums_left = len(index[num])
                del index[num]
                if not nums_left:
                    self.bingo = True

        remove_num_from_index(self._rows)
        remove_num_from_index(self._cols)

    def get_unmarked_numbers(self) -> Set[int]:
        """
        Return all the remaining numbers in the board
        that haven't been marked yet.
        """
        return self._rows.keys()

    def _get_cols(self, rows: List[List[int]]) -> List[List[int]]:
        """
        Rotate a list of rows into a list of columns
        """
        return list(map(list, zip(*rows)))

    def _index_list_by_values(self, board: List[List[int]]) -> Dict[int, List[int]]:
        """
        For each number in the board, create a mapping to its corresponding row or column.
        The input may be a list of columns or a list of rows.

        This function assumes all numbers in the board are unique.
        """
        return {number: numbers for numbers in board for number in numbers}



def get_score_for_winning_board(random_numbers: List[int], boards: List[Board], place: int = 1) -> int:
    """
    Given a sequence of random numbers, and a list of bingo boards, 
    get the score for the board that achieves bingo.

    By default, the first place board score is returned, but modifying the place parameter
    can yield results for the subsequent winners.
    """
    curr_place = 1
    for drawn_number in random_numbers:
        for board in boards:
            board.mark_number(drawn_number)
            if board.bingo:
                if curr_place == place:
                    return sum(board.get_unmarked_numbers()) * drawn_number
                curr_place += 1
                # since we achieved bingo, remove the board from consideration
                boards = [board for board in boards if not board.bingo]
    raise RuntimeError('No bingo!')


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=4)
    random_numbers: List[int] = [int(n) for n in raw_input[0].split(',')]
    boards: List[Board] = []
    for i in range(2, len(raw_input) - 2, 6):
        boards.append(Board([[int(n) for n in line.split()] for line in raw_input[i:i+5]]))

    print(f'Part 1 answer: {get_score_for_winning_board(random_numbers, boards, place=1)}')
    print(f'Part 2 answer: {get_score_for_winning_board(random_numbers, boards, place=len(boards))}')
