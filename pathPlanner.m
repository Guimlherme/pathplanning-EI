classdef pathPlanner
    properties
        map
        rows
        cols
        resolution
    end
    methods
        function obj = pathPlanner(rows,cols,resolution)
            obj.rows = rows;
            obj.cols = cols;
            obj.resolution = resolution;
            obj.map = binaryOccupancyMap(rows,cols,resolution);
        end
        
        function obj = fill(obj)
            for i = 1:obj.rows
                for j = 1:obj.cols
                    setOccupancy(obj.map, [i j], 1)
                end
            end
        end
        
        function obj = addroad(obj,roadCenters, laneSpecification)
            side = laneSpecification.Width/2;
            [A,B] = meshgrid(roadCenters(1,1)-side:roadCenters(2,1)+side,roadCenters(1,2)-side:roadCenters(2,2)+side);
            c=cat(2,A',B');
            square = reshape(c,[],2);
            setOccupancy(obj.map, grid2world(obj.map,square), 0);
        end
        
        function obj = addcar(obj)
            
        end
        
        function obj = addobject(obj)
            
        end
        
        
    end
end