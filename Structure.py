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


# redundant function
def word_num(target):
    temp_dict = dict()
    for i in range(len(target)):
        if target[i] in temp_dict:
            temp_dict[target[i]] += 1
        else:
            temp_dict[target[i]] = 1
    return temp_dict


def sorted_dict(container, keys, reverse=False):
    """返回 keys 的列表,根据container中对应的值排序"""
    aux = [(container[k], k) for k in keys]
    aux.sort()
    if reverse:
        aux.reverse()
    return [k for v, k in aux]

