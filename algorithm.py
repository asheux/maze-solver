from time import sleep


class Node:
    def __init__(self, root, action, state):
        self.state = state
        self.root = root
        self.action = action


class DFS:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        """
        check if the stack is empty
        """
        return len(self.stack) == 0

    def add(self, node):
        """
        Add a new item to to end of a stack
        """
        self.stack.append(node)

    def remove(self):
        """
        Remove from the end of a stack, using the
        Last in first out(LIFO)
        """
        node = self.stack[-1]  # remove the last node from the stack
        self.stack = self.stack[:-1]  # update the stack

        return node

    def contains(self, state, iterable):
        """
        Check if an item exists in a listjg
        """
        for item in iterable:
            if item.state == state:
                return True
        return False

    def algorithm(self, start, goal, callback):
        """
        This algorithm go through all the possible nodes
        that can be explored in a graph and returns the optimum
        path used to reach the goal
        """
        explored = list()  # maintain all the nodes that have been visitted
        count = 0
        begin = start

        start_node = Node(root=None, action=None, state=begin)
        self.add(start_node)  # add start node to the our stack

        while not self.is_empty():
            node = self.remove()
            count += 1  # keep a count of the number of visited nodes

            if node and node.state == goal:  # go here if the current node is our goal
                explored = []

                # backtracking to find the path used to get to the goal
                # an optimum path
                while node.root:
                    explored.append(node.state)
                    node = node.root
                break

            n = callback(node.state)

            # use the current that's being exployed and expand it to get
            # it's neighbouring nodes for exploring
            for a, new_state in n:
                if not self.contains(new_state,
                                     self.stack) and not self.contains(
                                         new_state, explored):
                    child_node = Node(root=node, action=a, state=new_state)
                    self.add(child_node)
            explored.append(node)
        return count, list(reversed(explored))


class BFS(DFS):
    def remove(self):
        node = self.stack[0]
        self.stack = self.stack[1:]

        return node
