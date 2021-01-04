import numpy as np

class RangeImageLabeling( object ):
    def __init__(self):
        self.Label = 1
        self.queue = list()
    
    def LabelRangeImage(self, RangeImage, HorizontalTheta, HorizontalAngle, VerticalTheta, VerticalAngle):
        self.RangeImage = RangeImage
        self.Rrow = self.RangeImage.shape[0]
        self.Rcol = self.RangeImage.shape[1]
        self.L = np.zeros( self.RangeImage.shape )
        defect = 1*(self.RangeImage == 0)
        self.L = self.L - defect

        self.Htheta = np.deg2rad(HorizontalTheta)
        self.HorizontalAngle = np.deg2rad(HorizontalAngle)
        self.Vtheta = np.deg2rad(VerticalTheta)
        self.VerticalAngle = np.deg2rad(VerticalAngle)

        for row in range(self.Rrow):
            for col in range(self.Rcol):
                if self.L[row,col] == 0:
                    self.LabelComponentBFS(row, col)
                    self.Label += 1

        return self.L.astype(np.int16)

    def LabelComponentBFS( self, r, c ):
        self.queue.append([r, c])
        while len(self.queue) != 0:
            target = self.queue.pop(0)
            target_r = target[0]
            target_c = target[1]
            if self.L[target_r, target_c] == 0:
                self.L[target_r, target_c] = self.Label
                RangeCenter = self.RangeImage[target_r, target_c]

                if RangeCenter > 0:
                    RowNeighborList, ColNeighborList = self.GetNeighbor( target_r, target_c )

                    if len(RowNeighborList) > 0:

                        for RowNeighbor in RowNeighborList:
                            row_neighbor_r = RowNeighbor[0]
                            row_neighbor_c = RowNeighbor[1]

                            RangeNeighbor = self.RangeImage[row_neighbor_r, row_neighbor_c]
                            
                            d1 = max(RangeCenter, RangeNeighbor)
                            d2 = min(RangeCenter, RangeNeighbor)

                            ValueArcTan = np.arctan(( d2 * np.sin(self.HorizontalAngle * (row_neighbor_r - target_r)) ) / ( d1 - d2 * np.cos(self.HorizontalAngle * (row_neighbor_r - target_r)) ))
                            if ValueArcTan > self.Htheta:
                                if [row_neighbor_r, row_neighbor_c] in self.queue:
                                    pass
                                else:
                                    self.queue.append([row_neighbor_r, row_neighbor_c])

                    if len(ColNeighborList) > 0:

                        for ColNeighbor in ColNeighborList:
                            col_neighbor_r = ColNeighbor[0]
                            col_neighbor_c = ColNeighbor[1]

                            RangeNeighbor = self.RangeImage[col_neighbor_r, col_neighbor_c]
                            
                            d1 = max(RangeCenter, RangeNeighbor)
                            d2 = min(RangeCenter, RangeNeighbor)

                            ValueArcTan = np.arctan(( d2 * np.sin(self.VerticalAngle * (col_neighbor_c - target_c)) ) / ( d1 - d2 * np.cos(self.VerticalAngle * (col_neighbor_c - target_c)) ))
                            if ValueArcTan > self.Vtheta:
                                if [col_neighbor_r, col_neighbor_c] in self.queue:
                                    pass
                                else:
                                    self.queue.append([col_neighbor_r, col_neighbor_c])

    def GetNeighbor(self, r, c):

        RowNeighborList = list()
        ColNeighborList = list()

        DownPointRow = r + 1
        RightPointCol = c + 1

        deterR = 0
        deterC = 0

        while True:
            if DownPointRow < self.Rrow:
                if self.RangeImage[DownPointRow, c] > 0:
                    deterR = 1
                else:
                    DownPointRow += 1
            else:
                deterR = 1
                DownPointRow = -1

            if RightPointCol < self.Rcol:
                if self.RangeImage[r, RightPointCol] > 0:
                    deterC = 1
                else:
                    RightPointCol += 1
            else:
                deterC = 1
                RightPointCol = -1

            if (deterR+deterC) == 2:
                break

        if DownPointRow > 0:
            RowNeighborList.append([DownPointRow, c])
        if RightPointCol > 0:
            ColNeighborList.append([r, RightPointCol])
        return RowNeighborList, ColNeighborList

