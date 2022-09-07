from collections import defaultdict


class Node:
  def __init__(self, index=None, stripe=None, val=float('inf'), left=None, right=None):
    self.index = index
    self.stripe = [] if stripe is None else stripe
    self.val = val
    self.left = left
    self.right = right
  
  def __lt__(self, other):
    return self.val < other.val

  def __le__(self, other):
    return self.val <= other.val
  
  def put(self, offset: int):
    self.stripe.append(offset)
    self.val = len(self.stripe)
  
  def consume_n(self, n: int):
    ret = self.stripe[:n]
    self.stripe = self.stripe[n:]
    self.val = len(self.stripe)
    return ret



class PriorityManager:
  def __init__(self):
    self.mapping = defaultdict(Node)
    self.dumbNode = Node()
    self.tailNode = self.dumbNode


  # Naive way (bubble). ToDo: Change to insertion if we update by batch
  def swap_left_(self, node: Node):
    tem = node.left
    node.left = tem.left
    node.left.right = node
    tem.right = node.right
    tem.right.left = tem
    tem.left = node
    node.right = tem


  # Provide to Receiver
  def recv_packet(self, index: int, offset: int):
    if index in self.mapping:
      cur = self.mapping[index]
      cur.put(offset)
    else:
      cur = self.mapping[index]
      cur.index = index
      cur.put(offset)
      cur.left = self.tailNode
      self.tailNode.right = cur
    
    while cur.left < cur:
      self.swap_left_(cur)
    
    if self.tailNode.right:
      self.tailNode = self.tailNode.right


  # Provide to CommandGenerator
  def fetch_max(self):
    if not self.dumbNode.right:
      return None
    
    ret = self.dumbNode.right
    self.dumbNode.right = ret.right
    if ret.right:
      ret.right.left = self.dumbNode
    # Isolate the returning node from linked list, 
    # no matter if it marks more than 9 packects or not
    ret.left, ret.right = None, None
    return ret


  # Provide to CommandGenerator
  def consume(self, cur: Node, expectation: int):
    ret = 0
    if cur.val <= expectation:
      usage = cur.stripe
      # Action here ^^
      self.mapping.pop(cur.index)
      ret = expectation - cur.val
    else:
      usage = cur.consume_n(expectation)
      # Action here ^^
      self.tailNode.right = cur
      cur.left = self.tailNode
      while cur.left < cur:
        self.swap_left_(cur)
      
      if self.tailNode.right:
        self.tailNode = self.tailNode.right
      
    return ret



def main():
  pm = PriorityManager()
  pass


if __name__ == '__main__':
  main()