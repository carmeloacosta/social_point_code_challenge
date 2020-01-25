#!/bin/python3

"""
    Client module. Contains all information regarding with a client
"""

from functools import total_ordering


@total_ordering
class Client():
    """
        Client
    """
    def __init__(self, id):
        self.id = id
        self.score = 0

    def __repr__(self):
        return "(id: {}, score: {})".format(self.id, self.score)

    def to_json(self):
        return {"user": self.id, "total": self.score}

    def total(self, score):
        """
            Modifies the client total score

        :param score: (int) New total score.
        :return: (bool) True if the modification was successfully applied. False otherwise.
        """
        result = True

        try:
            self.score = int(score)

        except ValueError:
            result = False

        return result

    def relative(self, modification):
        """
            Relative modification of the client total score

        :param modification: (str) Relative client score, following the format:

                        <operator><value>

                where:

                        <operator>: (str) Operator to be applied. Valid values are '+' and '-'. If a no valid operator
                                is used the score modification is not applied.

                        <value> : (str) Decimal value to be modified the score with. If does not represent a valid
                            base 10 value the score modification is not applied.

        :return: (bool) True if the modification was successfully applied. False otherwise.
        """
        result = True
        try:
            operator = modification[0]
            value = int(modification[1:])

            if operator == '+':
                # INCREASE
                self.score += value

            elif operator == '-':
                # DECREASE
                self.score -= value
            else:
                # UNKNOWN OPERATION
                result = False

        except (IndexError, ValueError):
            # Invalid modification
            result = False

        return result

    def _is_valid_operand(self, other):
        """
            Tells if the specified object is valid for comparison

        :param other:
        :return: (bool)
        """
        return hasattr(other, "score")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.score == other.score

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.score < other.score
