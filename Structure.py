from queue import Queue
import math

class StackUnderflow(ValueError):   # 栈下溢(空栈访问)
    pass


class SStack:
    def __init__(self):
        self._elems = []    # store element using list

    def is_empty(self):
        return self._elems == []

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        # return and delete
        if self._elems == []:
            raise StackUnderflow("in SStack.pop()")
        return self._elems.pop()

    def top(self):
        # return the last element
        if self._elems == []:
            raise StackUnderflow("in SStack.top()")
        return self._elems[-1]


class MinHeap(object):
    currentSize = 0
    maxSize = 0
    heapArray = None

    def __init__(self, n):
        if n <= 0:
            return
        else:
            self.maxSize = n

    def build_heap(self):
        i = self.currentSize // 2 - 1
        while i >= 0:
            self.siftdown(i)
            i -= 1

    def siftdown(self, pos):
        i = pos
        j = 2 * i + 1
        temp = self.heapArray[i]
        while j < self.currentSize:
            if j < self.currentSize-1 and self.heapArray[j] > self.heapArray[j+1]:
                j += 1
            if temp > self.heapArray[j]:
                self.heapArray[i] = self.heapArray[j]
                i = j
                j = 2 * j + 1
            else:
                break
        self.heapArray[i] = temp

    def siftup(self, pos):
        temp_pos = pos
        temp = self.heapArray[temp_pos]
        while temp_pos > 0 and self.heapArray[self.parent(temp_pos)] > temp:
            self.heapArray[temp_pos] = self.heapArray[self.parent(temp_pos)]
            temp_pos = self.parent(temp_pos)
        self.heapArray[temp_pos] = temp

    def insert(self, newNode):
        if self.currentSize == self.maxSize:
            return False
        self.heapArray.insert(self.currentSize, newNode)
        #self.heapArray.append(newNode)
        self.siftup(self.currentSize)
        self.currentSize += 1
        return True

    def remove_min(self):
        if self.currentSize == 0:
            print("Can't Delete")
            exit(1)
        else:
            self.currentSize -= 1
            temp = self.heapArray[0]
            self.heapArray[0] = self.heapArray[self.currentSize]
            self.heapArray[self.currentSize] = temp
            if self.currentSize > 1:
                self.siftdown(0)
            return self.heapArray.pop()

    def is_left(self, pos):
        return self.currentSize // 2 <= pos < self.currentSize

    def left_child(self, pos):
        return pos * 2 + 1

    def right_child(self, pos):
        return pos * 2 + 2

    def parent(self, pos):
        return (pos - 1) // 2


class HuffmanTreeNode(object):
    value = None
    code = ""   # HuffmanTree Code
    name = None
    left = None
    right = None
    parent = None

    def __init__(self, value=None, left=None, right=None, parent=None, name=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.name = name
        return

    def __lt__(self, other):
        if self.value < other.value:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        else:
            return False

    def encode(self):
        if self.left is not None:
            self.left.code = self.code + '1'
            self.left.encode()
        if self.right is not None:
            self.right.code = self.code + '0'
            self.right.encode()

    def is_leaf(self):
        return (self.left is None) and (self.right is None)

    def __del__(self):
        return


class HuffmanTree(object):
    root = None

    def __init__(self, weight, n):
        heap = MinHeap(n)
        node_list = list()
        for k in weight.keys():
            temp_node = HuffmanTreeNode(value=weight[k], name=k)
            node_list.append(temp_node)
        heap.heapArray = node_list
        heap.currentSize = len(node_list)
        heap.build_heap()
        for i in range(n-1):
            parent = HuffmanTreeNode()
            first_child = heap.remove_min()
            second_child = heap.remove_min()
            self.merge_tree(first_child, second_child, parent)
            heap.insert(parent)
            self.root = parent
        self.root.encode()

    def merge_tree(self, left, right, parent):
        parent.value = left.value + right.value
        parent.left = left
        parent.right = right
        left.parent = parent
        right.parent = parent
        return

    def delete_tree(self, root):
        if root is None:
            return
        else:
            self.delete_tree(root.left)
            self.delete_tree(root.right)
            root.__del__(root)
        return

    def pre_oder(self, root):
        if root is not None:
            print(root.value, " ", root.code, " ", root.name, root.is_leaf())
            self.pre_oder(root.left)
            self.pre_oder(root.right)

    def to_dict(self, root, dict_a):
        if root is not None:
            if root.is_leaf():
                dict_a[root.name] = root.code
            self.to_dict(root.left, dict_a)
            self.to_dict(root.right, dict_a)


def find_next(pattern):
    i = 0
    k = -1
    m = len(pattern)
    assert m > 0
    p_next = [0] * len(pattern)
    p_next[0] = -1
    while i < m:
        while k >= 0 and pattern[i] != pattern[k]:
            k = p_next[k]
        i += 1
        k += 1
        if i == m:
            break
        if pattern[i] == pattern[k]:
            p_next[i] = p_next[k]
        else:
            p_next[i] = k
    return p_next


def kmp_matching(target, pattern):
    i = 0
    j = 0
    p_len = len(pattern)
    t_len = len(target)
    pos = list()
    n = find_next(pattern)
    if t_len < p_len:
        print("target shorter than pattern")
        return -1   #target shorter than pattern, can't match
    while j < t_len:
        if i == -1 or target[j] == pattern[i]:
            i += 1
            j += 1
        else:
            i = n[i]
        if i >= p_len:
            i = 0
            pos.append(j - p_len)
    if len(pos) == 0:
        return -1
    else:
        return pos
#

def kmp_replace(target, old_str, new_str):
    text_pos = kmp_matching(target, old_str)
    if text_pos != -1:
        # print("text_pos:", text_pos)
        for i in range(0, len(text_pos)):
            pos = len(text_pos) - 1 - i
            # print(pos, text_pos[pos])
            # print(target[text_pos[pos]:])
            temp_str = target[text_pos[pos]:]
            target = target[0:text_pos[pos]]
            # print(target)
            temp_str = temp_str[len(old_str):]
            # print(temp_str)
            target += new_str
            target += temp_str
            # print(target)
    return target


def count_element(source, dict_a):
    for i in range(len(source)):
        if source[i] in dict_a:
            dict_a[source[i]] += 1
        else:
            dict_a[source[i]] = 1


def tf_idf_cal(passage_len, passage_count, file_path, index_word):
    # passage_len: the length of the passage
    # passage_count: total count of article
    # index_word: value of the word in inverted_index
    # {'path':[pos1, pos2]}
    word_count = len(index_word[file_path])  # how many time have this word appeared in this passage
    tf_value = word_count / passage_len
    idf_value = abs(math.log2(passage_count / (len(index_word) + 1)))
    print("tf:", tf_value, "idf:", idf_value)
    return tf_value * idf_value


def sorted_dict(container, keys, reverse=False):
    """返回 keys 的列表,根据container中对应的值排序"""
    aux = [(container[k], k) for k in keys]
    print(1)
    aux.sort()
    print(2)
    if reverse:
        print(3)
        aux.reverse()
        print(4)
    return [k for v, k in aux]


def takeFirst(elem):
    return elem[0]


def infix_to_postfix(str_pattern):
    priority = {'|': 1, '&': 2, '(': 3}
    str_pattern = str_pattern.replace(' ', '')  # remove all the space in the string
    queue_a = Queue()
    stack_a = SStack()
    if str_pattern != "":

        while str_pattern != "":
            item = []
            str_pattern = get_next_item(str_pattern, item)
            item = item[0]  # item = "string"

            print("str_a:", str_pattern)
            print("item:", item[0], len(item[0]))

            if item[0] == '~':
                # when item is a word with '~'
                # processing multiple '~'
                for i in range(len(item)):
                    if item[i] != '~':
                        if i % 2:
                            item = '~' + item[i:]
                            break
                        else:
                            item = item[i:]
                            break
                if item == '~':
                    print("invalid equation")
                    break
                else:
                    queue_a.put(item)
            elif item[0] != '(' and item[0] != ')' and item[0] != '&' and item[0] != '|':
                # when item is a word
                queue_a.put(item)
            elif stack_a.is_empty():
                # when item is a sign and the stack in empty
                stack_a.push(item)
            elif item == ')':
                while stack_a.top() != '(':
                    queue_a.put(stack_a.pop())
                stack_a.pop()   # pop '('
                continue
            elif stack_a.top() == '(' or priority[stack_a.top()] < priority[item]:
                stack_a.push(item)
            elif stack_a.top() != '(' and priority[stack_a.top()] >= priority[item]:
                queue_a.put(stack_a.pop())
                while (not stack_a.is_empty()) and stack_a.top() != '(' and priority[stack_a.top()] >= priority[item]:
                    queue_a.put(stack_a.pop())
                stack_a.push(item)
        while not stack_a.is_empty():
            queue_a.put(stack_a.pop())
        return queue_a
    else:
        print("Invalid input")


def get_next_item(str_a, item):
    # next element or sign
    # return new_str, item
    i = 0
    if str_a[i] == '(' or str_a[i] == ')' or str_a[i] == '&' or str_a[i] == '|':
        item.append(str_a[i])
        return str_a[1:]
    else:
        for i in range(len(str_a)):
            if str_a[i] == '(' or str_a[i] == ')' or str_a[i] == '&' or str_a[i] == '|':
                item.append(str_a[:i])
                return str_a[i:]
        item.append(str_a[:i+1])
        return ""


def get_file_name(path):
    for i in range(1, len(path)+1):
        if path[-i] == '/':
            break
    return path[-i+1:]


def pos_to_sentence_no(pos_index, sentence_index):
    print("inside func pos_to_sentence_no")
    sen_no_index = pos_index.copy()
    for key in pos_index.keys():
        for path in pos_index[key].keys():
            temp_list = pos_index[key][path]
            sen_no_index[key][path] = []
            for pos in temp_list:
                for i in sentence_index[path].keys():
                    if sentence_index[path][i][0] <= pos <= sentence_index[path][i][1]:
                        if len(sen_no_index[key][path]) > 0:
                            if sen_no_index[key][path][-1] != i:
                                sen_no_index[key][path].append(i)
                        else:
                            sen_no_index[key][path].append(i)
                        break
    return sen_no_index


def expression_calculation(index1, index2, sign):
    # index1\2 are indexed by sentence No.
    print("inside func expression_cal")
    print("sign:", sign)
    if sign == '|':
        print("cal |")
        result = index1.copy()
        for key in index2.keys():
            if key not in result:
                result[key] = index2[key].copy()
            else:
                result[key].extend(index2[key])
                temp_list = list(set(result[key]))
                print(temp_list)
                temp_list.sort()
                result[key] = temp_list
    elif sign == '&':
        if index1 == {} or index2 == {}:
            return {}
        result = index1.copy()
        # for key in index2.keys():
        for key in result.keys():
            # if key not in result:
            if key not in index2:
                print("not in:", key, result[key])
                # result[key] = []
                del result[key]
                # continue
            else:
                # temp_list = list(set(result[key]).intersection(set(index2[key])))
                temp_list = list(set(result[key]) & set(index2[key]))
                print(key, temp_list)
                result[key] = temp_list
        print("for finished")
    else:
        print("sign wrong")
    return result


def locate_sentence(list_a):
    print("inside func locate_sentence")
    # list_a: [path, word pos]
    file_a = open(list_a[0], mode='r')
    str_a = file_a.read()
    w_pos = list_a[1]
    s_pos = 0   # start pos
    e_pos = 0   # end pos
    for i in range(w_pos, len(str_a)):
        if str_a[i] == '.' or str_a[i] == '!' or str_a[i] == '?' or str_a[i] == '>' or str_a[i] == '<':
            e_pos = i
            break
    s_pos = w_pos
    while s_pos >= 0:
        if str_a[s_pos] == '.' or str_a[s_pos] == '!' or str_a[s_pos] == '?' or str_a[s_pos] == '>' \
                or str_a[s_pos] == '<':
            # print(s_pos, str_a[s_pos])
            break
        s_pos -= 1
    s_pos += 1
    return [list_a[0], s_pos, e_pos]


def invert_select(word, u_set, sentence):
    print("inside func invert_select")
    # processing '~'
    # u_set: universal set contains all sentence num of each passage
    # sentence: inverted_index with sentence no
    word = word[1:]
    if word in sentence:
        original = sentence[word]
        print('original:', original)
        result = original.copy()
        for path in u_set.keys():
            count = len(u_set[path])
            result[path] = []
            for i in range(count):
                exist = False
                for j in original[path]:
                    if j == i+1:
                        exist = True
                if not exist:
                    result[path].append(i+1)
        return result
    else:
        result = {}
        for path in u_set.keys():
            count = len(u_set[path])
            result[path] = []
            for i in range(count):
                result[path].append(i+1)
        return result
