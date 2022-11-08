function squareInflate(map,side)

% expands (side) squares in each direction

[a,b] = find(map.occupancyMatrix);

for i = 1:length(a)
    [A,B] = meshgrid(a(i)-side:a(i)+side,b(i)-side:b(i)+side);
    c=cat(2,A',B');
    square = reshape(c,[],2);
    setOccupancy(map, grid2world(map,square), 1);
end

end