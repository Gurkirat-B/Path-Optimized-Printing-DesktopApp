class HamiltonianSTL:
    def __init__(self, width: int, height: int, use_zigzag=True):
        self.width = width
        self.height = height
        self.H = [[False for _ in range(width - 1)] for _ in range(height)]
        self.V = [[False for _ in range(width)] for _ in range(height - 1)]

        if use_zigzag:
            self.zigzag()

    def zigzag(self):
        for y in range(self.height):
            if y % 2 == 0:
                for x in range(self.width - 1):
                    self.H[y][x] = True
                if y < self.height - 1:
                    self.V[y][self.width - 1] = True
            else:
                for x in range(self.width - 1):
                    self.H[y][x] = True
                if y < self.height - 1:
                    self.V[y][0] = True

    def set_edge(self, p1, p2, value=True):
        if not p1 or not p2:
            return
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and abs(y1 - y2) == 1:
            self.V[min(y1, y2)][x1] = value
        elif y1 == y2 and abs(x1 - x2) == 1:
            self.H[y1][min(x1, x2)] = value

    def has_edge(self, p1, p2):
        if not p1 or not p2:
            return False
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and abs(y1 - y2) == 1:
            return self.V[min(y1, y2)][x1]
        elif y1 == y2 and abs(x1 - x2) == 1:
            return self.H[y1][min(x1, x2)]
        return False

    def get_subgrid_by_corners(self, corner1, corner2):
        x1, y1 = corner1
        x2, y2 = corner2
        x_start, x_end = sorted([x1, x2])
        y_start, y_end = sorted([y1, y2])

        subgrid = []
        for y in range(y_start, y_end + 1):
            row = []
            for x in range(x_start, x_end + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    row.append((x, y))
                else:
                    row.append(None)
            subgrid.append(row)
        return subgrid

    def transpose_subgrid(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(a, d)
        self.set_edge(b, c)
        self.set_edge(b, e)
        self.set_edge(c, f)
        self.set_edge(e, h)
        self.set_edge(g, h)
        self.set_edge(f, i)

        return subgrid, "transposed"

    def print_ascii_edges(self, highlight_subgrid=None):
        grid_height = self.height * 2 - 1
        grid_width = self.width * 2 - 1
        grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

        highlight_set = set()
        if highlight_subgrid:
            for row in highlight_subgrid:
                for point in row:
                    if point:
                        highlight_set.add(point)

        for y in range(self.height):
            for x in range(self.width):
                gx, gy = x * 2, y * 2
                grid[gy][gx] = 'X' if (x, y) in highlight_set else 'O'

        for y in range(self.height):
            for x in range(self.width - 1):
                if self.H[y][x]:
                    grid[y * 2][x * 2 + 1] = '-'

        for y in range(self.height - 1):
            for x in range(self.width):
                if self.V[y][x]:
                    grid[y * 2 + 1][x * 2] = '|'

        for row in grid:
            print(' '.join(row))

    def validate_full_path(self):
        visited = set()
        start = (0, 0)
        stack = [start]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            x, y = current
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.has_edge(current, (nx, ny)):
                        neighbors.append((nx, ny))
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)

        return len(visited) == self.width * self.height

    # West-Above
    def transpose_subgrid_wa(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(a, d)
        self.set_edge(d, g)
        self.set_edge(g, h)
        self.set_edge(h, e)
        self.set_edge(e, b)
        self.set_edge(b, c)
        self.set_edge(f, i)

        return subgrid, "transposed_wa"


    # Right-Left
    def transpose_subgrid_rl(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(g, d)
        self.set_edge(d, a)
        self.set_edge(g, h)
        self.set_edge(b, e)
        self.set_edge(e, h)
        self.set_edge(b, c)
        self.set_edge(i, f)

        return subgrid, "transposed_rl"
    
    # South-Right
    def transpose_subgrid_sr(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(a, d)
        self.set_edge(b, c)
        self.set_edge(b, e)
        self.set_edge(c, f)
        self.set_edge(e, h)
        self.set_edge(f, i)

        return subgrid, "transposed_sr"
    
    # West-Below
    def transpose_subgrid_wb(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(a, b)
        self.set_edge(d, e)
        self.set_edge(e, f)
        self.set_edge(g, h)
        self.set_edge(h, i)
        self.set_edge(f, i)

        return subgrid, "transposed_wb"

    # East-Above
    def transpose_subgrid_ea(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(a, b)
        self.set_edge(b, c)
        self.set_edge(a, d)
        self.set_edge(d, e)
        self.set_edge(e, f)
        self.set_edge(g, h)

        return subgrid, "transposed_ea"
    
    # South-Left
    def transpose_subgrid_sl(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(a, b)
        self.set_edge(a, d)
        self.set_edge(b, e)
        self.set_edge(c, f)
        self.set_edge(d, g)
        self.set_edge(e, h)

        return subgrid, "transposed_sl"
    
    # North-Right
    def transpose_subgrid_nr(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(b, e)
        self.set_edge(c, f)
        self.set_edge(d, g)
        self.set_edge(e, h)
        self.set_edge(f, i)
        self.set_edge(h, i)

        return subgrid, "transposed_nr"
    
    # East-Below
    def transpose_subgrid_eb(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not transposable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        self.set_edge(a, b)
        self.set_edge(d, e)
        self.set_edge(e, f)
        self.set_edge(d, g)
        self.set_edge(g, h)
        self.set_edge(h, i)

        return subgrid, "transposed_eb"
    


    # Flip Operation
    def flip_subgrid(self, subgrid):
        flat = [pt for row in subgrid for pt in row if pt is not None]
        if len(flat) != 6:
            return subgrid, "invalid size"

        if len(subgrid) == 3 and len(subgrid[0]) == 2:
            width, height = 2, 3 
        elif len(subgrid) == 2 and len(subgrid[0]) == 3:
            width, height = 3, 2 
        else:
            return subgrid, "not 3x2 or 2x3"

        points = [pt for row in subgrid for pt in row if pt is not None]

        for pt in points:
            x, y = pt
            neighbor_found = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in points and self.has_edge(pt, (nx, ny)):
                    neighbor_found = True
            if not neighbor_found:
                return subgrid, "not flippable"

        for pt in points:
            x, y = pt
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        if width == 2:
            a, b = subgrid[0]
            c, d = subgrid[1]
            e, f = subgrid[2]
            self.set_edge(a, b)
            self.set_edge(a, c)
            self.set_edge(b, d)
            self.set_edge(e, f)
        else:
            a, b, c = subgrid[0]
            d, e, f = subgrid[1]
            self.set_edge(a, d)
            self.set_edge(b, c)
            self.set_edge(b, e)
            self.set_edge(e, f)

        return subgrid, "flipped"

    # West
    def flip_subgrid_w_3x3(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        points = [a, b, c, d, e, f, g, h, i]
        for pt in points:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (pt[0] + dx, pt[1] + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        self.set_edge(g, h)
        self.set_edge(a, d)
        self.set_edge(a, b)
        self.set_edge(e, h)
        self.set_edge(d, e) 
        self.set_edge(i, f)

        return subgrid, "flipped"

    # East
    def flip_subgrid_e_3x3(self, subgrid):
        if len(subgrid) != 3 or len(subgrid[0]) != 3:
            return subgrid, "not 3x3"

        a, b, c = subgrid[0]
        d, e, f = subgrid[1]
        g, h, i = subgrid[2]

        points = [a, b, c, d, e, f, g, h, i]
        for pt in points:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (pt[0] + dx, pt[1] + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        self.set_edge(a, b)
        self.set_edge(d, e) 
        self.set_edge(g, h)
        self.set_edge(a, d)
        self.set_edge(e, h)
        self.set_edge(b, c)
        self.set_edge(f, i)

        return subgrid, "flipped"
    
    # North
    def flip_subgrid_n_2x3(self, subgrid):
        if len(subgrid) != 2 or len(subgrid[0]) != 3:
            return subgrid, "not 2x3"

        a, b = subgrid[0]
        c, d = subgrid[1]
        e, f = subgrid[2]


        points = [a, b, c, d, e, f]
        for pt in points:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (pt[0] + dx, pt[1] + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        self.set_edge(a, c)
        self.set_edge(b, d) 
        self.set_edge(c, d)
        self.set_edge(e, f)

        return subgrid, "flipped"
    
    # South
    def flip_subgrid_s_2x3(self, subgrid):
        if len(subgrid) != 2 or len(subgrid[0]) != 3:
            return subgrid, "not 2x3"

        a, b = subgrid[0]
        c, d = subgrid[1]
        e, f = subgrid[2]

        points = [a, b, c, d, e, f]
        for pt in points:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (pt[0] + dx, pt[1] + dy)
                if neighbor in points:
                    self.set_edge(pt, neighbor, False)

        self.set_edge(a, b)
        self.set_edge(c, d) 
        self.set_edge(c, e)
        self.set_edge(d, f)

        return subgrid, "flipped"
    
if __name__ == '__main__':
    hamiltonian = HamiltonianSTL(10, 10)

    print("Original Grid:")
    hamiltonian.print_ascii_edges()


    #bottom right transpose
    subgrid = hamiltonian.get_subgrid_by_corners((7, 6), (9, 8))
    print("\nSelected 3x3 Subgrid for Transpose:")
    for row in subgrid:
        print(row)

    transposed, result = hamiltonian.transpose_subgrid(subgrid)
    print(f"\nTranspose: {result}")

    print("\nGrid After Transpose:")
    hamiltonian.print_ascii_edges(highlight_subgrid=transposed)


    #top right transpose
    top_right_subgrid = hamiltonian.get_subgrid_by_corners((7, 0), (9, 2))
    print("\nSelected 3x3 Subgrid for Top-Right Transpose:")
    for row in top_right_subgrid:
        print(row)

    transposed_top_right, result_top_right = hamiltonian.transpose_subgrid(top_right_subgrid)
    print(f"\nTop-Right Transpose: {result_top_right}")

    print("\nGrid After Top-Right Transpose:")
    hamiltonian.print_ascii_edges(highlight_subgrid=transposed_top_right)


    #top left transpose
    top_left_subgrid = hamiltonian.get_subgrid_by_corners((0, 0), (2, 2))
    print("\nSelected 3x3 Subgrid for Top-Left WA Transpose:")
    for row in top_left_subgrid:
        print(row)

    transposed_top_left, result_top_left = hamiltonian.transpose_subgrid_wa(top_left_subgrid)
    print(f"\nTop-Left Transpose (WA): {result_top_left}")

    print("\nGrid After Top-Left Transpose (WA):")
    hamiltonian.print_ascii_edges(highlight_subgrid=transposed_top_left)


    #bottom left transpose
    bottom_left_subgrid = hamiltonian.get_subgrid_by_corners((0, 6), (2, 8))
    print("\nSelected 3x3 Subgrid for Bottom-Left RL Transpose:")
    for row in bottom_left_subgrid:
        print(row)

    transposed_bottom_left, result_bottom_left = hamiltonian.transpose_subgrid_rl(bottom_left_subgrid)
    print(f"\nBottom-Left Transpose (RL): {result_bottom_left}")

    print("\nGrid After Bottom-Left Transpose (RL):")
    hamiltonian.print_ascii_edges(highlight_subgrid=transposed_bottom_left)


    #bottom right flip
    subgrid_s = hamiltonian.get_subgrid_by_corners((6, 6), (8, 7))
    print("\nSelected 3x2 Subgrid for Bottom-Right (S) Flip:")
    for row in subgrid_s:
        print(row)

    flipped_s, result_s = hamiltonian.flip_subgrid(subgrid_s)
    print(f"\nFlip S: {result_s}")
    hamiltonian.print_ascii_edges(highlight_subgrid=flipped_s)


    #top right flip
    subgrid_n = hamiltonian.get_subgrid_by_corners((6, 0), (8, 1))
    print("\nSelected 3x2 Subgrid for Top-Right (N) Flip:")
    for row in subgrid_n:
        print(row)

    flipped_n, result_n = hamiltonian.flip_subgrid(subgrid_n)
    print(f"\nFlip N: {result_n}")
    hamiltonian.print_ascii_edges(highlight_subgrid=flipped_n)


    #top left flip
    subgrid_w = hamiltonian.get_subgrid_by_corners((1, 0), (3, 2))
    print("\nSelected 3x3 Subgrid for Top-Left (W) 3x3 Flip:")
    for row in subgrid_w:
        print(row)

    flipped_w, result_w = hamiltonian.flip_subgrid_w_3x3(subgrid_w)
    print(f"\nFlip W: {result_w}")
    hamiltonian.print_ascii_edges(highlight_subgrid=flipped_w)


    #bottom left flip
    subgrid_e = hamiltonian.get_subgrid_by_corners((1, 6), (3, 8))
    print("\nSelected 3x2 Subgrid for Bottom-Left (E) Flip:")
    for row in subgrid_e:
        print(row)

    flipped_e, result_e = hamiltonian.flip_subgrid_e_3x3(subgrid_e)
    print(f"\nFlip E: {result_e}")
    hamiltonian.print_ascii_edges(highlight_subgrid=flipped_e)