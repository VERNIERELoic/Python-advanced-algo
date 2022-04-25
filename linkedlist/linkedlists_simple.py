class LC:
    class Cell:
        def __init__(self, val):
            self.val = val
            self.next = None
            self.previous = None


    def __init__(self):
        self.head = None
        self.max = None
        self.min = None

    def add_last(self, val):
        if self.head == None:
            cell = LC.Cell(val)
            self.head = cell
            return
        
        cell = self.head
        while(cell.next != None):
            cell = cell.next
    
        c = LC.Cell(val)
        cell.next = c

    def add_begin(self, val):
        cell = self.head
        c = LC.Cell(val)
        self.head = c
        self.head.next = cell

    def delete_last(self):
        cell = self.head
        while(cell.next.next != None):
            cell = cell.next
        cell.next = None
    
    def test_is_none(self):
        if self.head == None:
            return True
        else:
            return False
    
    def get_minmax(self):
        cell = self.head
        self.max = cell.val
        self.min = cell.val
        while cell.next != None:
            cell = cell.next
            if cell.val > self.max:
                self.max = cell.val
            if cell.val < self.min:
                self.min = cell.val

        return self.max, self.min
    
    def 
      
    def print(self):
        cell = self.head
        while(cell != None):
            print(cell.val)
            cell = cell.next


L = LC()
L.add_last(3)
L.add_last(4)
L.add_last(7)
L.add_last(9)
L.delete_last()
L.add_begin(1)
L.print()
print(L.get_minmax())
L.test_is_none()

