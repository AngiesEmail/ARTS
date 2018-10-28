class ListNode(Onject):
    def __init__(self,x):
        self.val = x
        self.next = None

def mergeLists(l1,l2):
    dummy = result = ListNode(l1.val)
    node1 = l1.next
    node2 = l2
    while node1 != None and node2 != None:
        if node1.val <= node2.val:
            result.next = node1
            node1 = node1.next
            result = result.next
        else:
            if result.val <= node2.val:
                result.next = node2
                node2 = node2.next
                result = result.next
            else:
                curNode = result
                result.val = node2.val
                result.next = curNode
                node2 = node2.next
                result = result.next
    return dummy