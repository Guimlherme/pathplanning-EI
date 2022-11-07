map = binaryOccupancyMap(rows,cols,resolution);
setOccupancy(map, [5 5 ; 8 8], 1);
squareInflate(map,2)
show(map)