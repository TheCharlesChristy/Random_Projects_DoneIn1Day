from math import floor

class Cell:
    def __init__(self) -> None:
        pass

class HashSpatialGrid:
    def __init__(self, bounds, dimensions, cell_dimensions): # bounds = [[x1,y1], [x2,y2]] dimensions = [w,h]
        self.bounds = bounds
        self.dimensions = dimensions
        self.cell_dimensions = cell_dimensions
        self.Particles = []
        self.Cells = self._GenerateCells() # hashid : obj.Grid_Cell
        self.Pointer_Array = [0]*(len(self.Cells)+1)
        self.DenseArray = [0]*(len(self.Particles))
        self.NumberOfCells = self._SolveNumberOfCells()

    def AddParticles(self, particles):
        for particle in particles:
            self.Particles.append(particle)
        self.DenseArray = [0]*(len(self.Particles))

    def CheckVariables(self):
        #print("Particles:", self.Particles)
        #print("Cells:", self.Cells)
        print("Pointer Array:", self.Pointer_Array)
        arr = []
        for obj in self.DenseArray:
            arr.append(obj.id)
        print("Dense Array:", arr)

    def _GenerateCells(self):
        arr = []
        for i in range(floor((self.dimensions[0]/self.cell_dimensions)*(self.dimensions[1]/self.cell_dimensions))):
            arr.append(Cell())
        return arr
    
    def _SolveNumberOfCells(self):
        return [floor(self.dimensions[0] / self.cell_dimensions), floor(self.dimensions[1] / self.cell_dimensions)]

    def _SolveDenseArray(self):
        self._SolvePointerArray()
        for particle in self.Particles:
            i = self._CalculateGridId(particle.position)
            self.Pointer_Array[i]-=1
            self.DenseArray[self.Pointer_Array[i]] = particle
    
    def _SolvePointerArray(self):
        for particle in self.Particles:
            i = self._CalculateGridId(particle.position)
            self.Pointer_Array[i]+=1
        #for i in range(len(self.Pointer_Array)):
        #    print(i, self.Pointer_Array[i])
        prev = 0
        for i in range(len(self.Pointer_Array)):
            self.Pointer_Array[i]+=prev
            prev = self.Pointer_Array[i]

    def _CalculateGridId(self, position):
        xpos = position[0]-self.bounds[0][0]
        ypos = position[1]-self.bounds[0][1]
        xi = floor(xpos/self.cell_dimensions)
        yi = floor(ypos/self.cell_dimensions)
        i = (xi*(self.NumberOfCells[1])+yi)%(len(self.Pointer_Array)-1)
        return i
    
    def _SolveNearbyCellIds(self, central_id):
        left_cell_id = central_id - self.NumberOfCells[1]
        right_cell_id = central_id + self.NumberOfCells[1]
        arr = [left_cell_id-1,left_cell_id,left_cell_id+1,central_id-1,central_id,central_id+1,right_cell_id-1,right_cell_id,right_cell_id+1]
        ret_arr = []
        for id in arr:
            if id<0 or id>=len(self.Pointer_Array)-1:
                continue
            else:
                ret_arr.append(id)
        return ret_arr
    
    def FindNearby(self, particle_position):
        i = self._CalculateGridId(particle_position)
        cellsToSearch = self._SolveNearbyCellIds(i)
        nearby_particles = []
        for cell_id in cellsToSearch:
            arr = self.GetParticlesInCell(cell_id)
            for particle in arr:
                nearby_particles.append(particle)
        return nearby_particles

    def update(self):
        self.Pointer_Array = [0]*(len(self.Cells)+1)
        self.DenseArray = [0]*(len(self.Particles))
        self._SolveDenseArray()

    def GetParticlesInCell(self, cellid):
        densei = self.Pointer_Array[cellid]
        amount_of_particles = self.Pointer_Array[cellid+1] - densei
        ret_arr = []
        for i in range(amount_of_particles):
            ret_arr.append(self.DenseArray[densei])
            densei += 1
        return ret_arr