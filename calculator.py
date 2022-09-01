
# check if input is correct
# parse input into a list
# input into Odwrotna Notacja Polska (Reverse Polish Notation)
# calculate


class Calculator:

    error_detected = False
    log = False

    def __init__(self, log=False, test=False):
        self.log = log
        while not test:
            expression = input("Enter a numerical expression (* / - +):")
            # self.check_brackets_validity(self.check_operator_duplication(self.check_character_validity(expression)))
            self.run_all(expression)
        if test:
            self.test_run()

    def run_all(self, expression):
        if self.any_numbers(expression):
            expression = self.check_characters(expression)
            expression = self.check_fractions(expression)
            expression = self.check_operators(expression)
            expression = self.check_brackets_closure(expression)
            expression = self.check_operators_near_brackets(expression)
            expression = self.parse_input_into_onp(expression)
            self.do_the_math(expression)

    def test_run(self):
        tests = ["dsghbgsdgjsdij",
                 "dsgh3--+2.h523+bgsd3.+.55---352=++++&***gjsdij",
                 ".2+2.+.....++..-.-...",
                 "2.(2+.2)+.2.",
                 "12.4+2*(3.3*4+10/5)",
                 "2+2*2",
                 "(-2+-2*8)/2-2",
                 "+*-+*-+--2+-+-+-dsggsdgsd+-*-",
                 "(2+2)*2",
                 "2*2/2*2/2*2+5*2***2"
                 ]
        for i in tests:
            print("\nRunning test expression:", i)
            self.run_all(i)

    def any_numbers(self, string):
        for i in string:
            if i.isnumeric():
                if self.log:
                    print("any numbers", True)
                return True
        if self.log:
            print("any numbers", False)
        return False

    def check_characters(self, string):
        string = string.replace(" ", "")
        string = string.replace(",", ".")
        result = ""
        for i in string:
            if i in [".", "+", "-", "*", "/", "(", ")"] or i.isnumeric():
                result += i
            else:
                self.error_detected = True
        if self.log:
            print("check character validity", result)
        return result

    def check_fractions(self, string):
        result = ""
        # remove duplicate .
        for i in string:
            if i == "." and len(result) > 0 and result[-1] == ".":
                continue
            else:
                result += i
        if self.log:
            print("check fraction duplicates", result)
        # remove . not neighbouring any number
        string = result
        result = ""
        for i in range(len(string)):
            if string[i] == ".":
                if i == 0 and not string[i+1].isnumeric():
                    continue
                elif i == len(string)-1 and not string[i-1].isnumeric():
                    continue
                elif i != 0 and i != len(string)-1 and not (string[i-1].isnumeric() or string[i+1].isnumeric()):
                    continue
                else:
                    result += string[i]
            else:
                result += string[i]
        if self.log:
            print("check . neighbouring numbers", result)
        # .1 into 0.1 and 1. into 1
        string = result
        result = ""
        for i in range(len(string)):
            if string[i] == ".":
                # .1 at start
                if i == 0 and string[i+1].isnumeric():
                    result += "0"
                # .1 anywhere else
                elif i != 0 and not string[i-1].isnumeric() and i != len(string)-1 and string[i+1].isnumeric():
                    result += "0"
                # 1. at the end
                if i == len(string)-1 and string[i-1].isnumeric():
                    continue
                # 1. anywhere else
                elif i != 0 and string[i-1].isnumeric() and i < len(string)-1 and not string[i+1].isnumeric():
                    continue
                result += string[i]
            else:
                result += string[i]
        if self.log:
            print("check fraction position", result)
        return result

    def check_operators(self, string):
        result = ""
        # duplication
        for i in range(len(string)):
            if i != 0 and string[i] in [".", "+", "-", "*", "/"] and string[i-1] in [".", "+", "-", "*", "/"]:
                if string[i] == "-" and string[i+1].isnumeric():
                    result += string[i]
                self.error_detected = True
            else:
                result += string[i]
        if self.log:
            print("check operator duplication", result)

        # loose operators at the end
        for i in reversed(result):
            if i in [".", "+", "-", "*", "/"]:
                result = result[:-1]
            else:
                break
        if self.log:
            print("check operator loose at the end", result)

        # loose operators at the beginning
        for i in range(len(result)):
            if result[0] in ["+", "*", "/", "."]:
                result = result[1:]
            elif i < len(result)-1 and result[0] == "-" and result[1].isnumeric():
                break
            else:
                break
        if self.log:
            print("check operator loose at the beginning", result)
        return result

    def check_brackets_closure(self, string):
        result = ""
        brackets = ""
        for i in range(len(string)):
            if string[i] == "(":
                brackets += ")"
                if i != 0 and string[i-1].isnumeric():  # interpret 1( as 1*(
                    result += "*"
            elif string[i] == ")":
                if len(brackets) == 0:  # missing opening bracket
                    result = "(" + result
                else:  # close leftover brackets
                    brackets = brackets[:-1]
            result += string[i]
            if string[i] == ")" and i < len(string) - 1 and string[i + 1].isnumeric():  # interpret )1 as )*1
                result += "*"
        result += brackets
        if self.log:
            print("check brackets validity", result)
        return result

    def check_operators_near_brackets(self, string):
        result = string[0]
        for i in range(1, len(string)-1):
            if string[i] == "(" and string[i-1].isnumeric():  # 1( -> 1*(
                result += "*"
            if string[i] in [".", "+", "*", "/"] and string[i-1] == "(":
                continue
            elif string[i] in [".", "+", "-", "*", "/"] and string[i+1] == ")":
                continue
            result += string[i]
            if string[i] == ")" and string[i+1].isnumeric():  # )1 -> )*1 2+(*2+2*)+2
                result += "*"
        result += string[-1]
        if self.log:
            print("check operators near brackets", result)
        return result

    def parse_number(self, index, number, string):
        index = index + 1
        if index < len(string) and string[index].isnumeric():
            return self.parse_number(index, number + string[index], string)
        elif index < len(string) and string[index] == ".":
            if "." in number:
                self.error_detected = True
                return self.parse_number(index, number, string)
            else:
                return self.parse_number(index, number + string[index], string)
        return index, number

    def parse_input_into_onp(self, string):
        # split input elements into a list
        prepared_input = []
        i = 0
        while i < len(string):
            if string[i].isnumeric() or (string[i] == "-" and i < len(string)-1 and string[i+1].isnumeric() and (string[i-1] in [".", "+", "-", "*", "/", "("] or i == 0)):
                index, tmp = self.parse_number(i, string[i], string)
                i = index
                if "." in tmp:
                    tmp = float(tmp)
                else:
                    tmp = int(tmp)
                prepared_input.append(tmp)
            else:
                prepared_input.append(string[i])
                i += 1

        if self.log:
            print("parse input into a list", prepared_input)

        if self.error_detected:
            tmp = ""
            for j in prepared_input:
                tmp += str(j) + " "
            print("Errors in input detected, interpreted as:\n", tmp)

        # turn list into Reverse Polish Notation
        result = []
        stack = []
        index = 0
        for i in range(len(prepared_input)):
            index += 1
            if isinstance(prepared_input[i], (float, int)):
                result.append(prepared_input[i])
            elif prepared_input[i] == "(":
                stack.append(prepared_input[i])
            elif prepared_input[i] == ")":
                while True:
                    tmp = stack.pop()
                    if tmp == "(":
                        break
                    else:
                        result.append(tmp)
            else:
                while len(stack) != 0 and not((prepared_input[i] == "*" or prepared_input[i] == "/") and (stack[-1] == "+" or stack[-1] == "-")):
                    if stack[-1] in ["+", "-", "*", "/"]:
                        result.append(stack.pop())
                    else:
                        break
                stack.append(prepared_input[i])
            if i == len(prepared_input)-1:
                for j in range(len(stack)):
                    result.append(stack.pop())
        if self.log:
            print("RPN", result)
        return result

    def do_the_math(self, onp):
        if not len(onp) == 1:
            stack = []
            for i in range(len(onp)):
                if isinstance(onp[i], (float, int)):
                    # stack.append(int(onp[i]))
                    stack.append(onp[i])
                else:
                    if onp[i] == "+":
                        stack.append(stack.pop() + stack.pop())
                    elif onp[i] == "*":
                        stack.append(stack.pop() * stack.pop())
                    elif onp[i] == "-":
                        tmp = stack.pop()
                        stack.append(stack.pop()-tmp)
                    else:  # / dzielenie przez zero?
                        tmp = stack.pop()
                        if tmp == 0:
                            print("pamietaj cholero nie dziel przez zero")
                            return False
                        else:
                            stack.append(stack.pop()/tmp)
            if stack[0] % 1 == 0:
                stack[0] = int(stack[0])
            print("Result:", stack[0])
        else:
            print("Result:", onp[0])
        # return True


# constructor (if_output_logs, if_run_auto_test_instead)
# c = Calculator(True, True)
c = Calculator()

# przykladowe dzialania
# (-2+-2*8)/2-2 = -11
# 12.4+2×(3.3×4+10/5) = 42.8
# 2+2*2 = 6
# (2+2)*2 = 8
# 8/2(2+2) = 16
# -4*(-1/12)-74 = -73.6666666667
