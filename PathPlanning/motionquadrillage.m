
function [map next_Position next_Yaw final] = motionquadrillage(map, car, point_livraison,v,Ts)
    persistent arrived;
    if isempty(arrived)
        arrived=1;
    end
    persistent nextPos;
    persistent firstPos;

    start = to_index(car.Position);
    goal = to_index(point_livraison);

    % if it is in the point, stop
    if car.Position(1) == point_livraison(1) && car.Position(2) == point_livraison(2) 
        next_Position = car.Position;
        next_Yaw = car.Yaw;
        return
    end  
   
    % find path
    final = a_star(logical(map), ones(size(map)), start, goal, 10, 10);
    final = flip(final, 2);
    
    if size(final, 2) < 2
         % if there is only one point, keep going to it
        [newX, newY] = ind2sub(10, final(1));
        nextPos = to_pos([newX, newY]);
    else  
         % if there is only one point, keep going to it
        [newX, newY] = ind2sub(10, final(1));
        newFirstPos = to_pos([newX, newY]);
        [newX, newY] = ind2sub(10, final(2));
        newSecondPos = to_pos([newX, newY]);
        
        if isempty(firstPos) || not(firstPos(1) == newFirstPos(1) && firstPos(2) == newFirstPos(2)) 
            firstPos = newFirstPos;
        end
        arrived = (car.Position(1) == firstPos(1) && firstPos(2) == car.Position(2));
        if not(isempty(nextPos)) && not( (nextPos(1) == newSecondPos(1) &&nextPos(2) == newSecondPos(2)) || (nextPos(1) ==newFirstPos(1) && nextPos(2) ==newFirstPos(2)))
            nextPos=newFirstPos;
        elseif arrived 
            nextPos=newSecondPos;
        end
    end
    
    next_Position = nextPos;
    
    
    next_Yaw=car.Yaw;
     if next_Position(1) ~= car.Position(1) 
        if abs(next_Position(1)-car.Position(1))>v*Ts
            next_Position(1)=car.Position(1)+v*Ts*sign(next_Position(1)-car.Position(1));
        end
        if (next_Position(1)-car.Position(1))>0 next_Yaw = 0;else next_Yaw = 180;end
        next_Position(2) = car.Position(2);
     elseif next_Position(2) ~= car.Position(2) 
        if abs(next_Position(2)-car.Position(2))>v*Ts
            next_Position(2)=car.Position(2)+v*Ts*sign(next_Position(2)-car.Position(2));
        end
        if (next_Position(2)-car.Position(2))>0 next_Yaw = 90;else next_Yaw = -90;end
        next_Position(1) = car.Position(1);
     end
end

function pos = to_index(pos)
    pos = [round(pos(1)/10)+1, round(pos(2)/10)+1];
end


function pos = to_pos(ix)
    pos = [(ix(1)-1)*10, (ix(2)-1)*10, 0];
end