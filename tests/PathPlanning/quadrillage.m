clear all
close all
% Construct a drivingScenario object.
Ts = 1; %sampling time
scenario = drivingScenario('SampleTime', Ts);

rng(122);

% Add all road segments
L=10;
for i=0:L
    for j=0:L
        if j<L
            roadCenters = [i*L j*L 0 ;i*L (j+1)*L 0];
            laneSpecification = lanespec(1);
            road(scenario, roadCenters, 'Lanes', laneSpecification);
        end
        if i<L
            roadCenters = [i*L j*L 0 ;(i+1)*L j*L 0];
            laneSpecification = lanespec(1);
            road(scenario, roadCenters, 'Lanes', laneSpecification);
        end
    end
end

%ajouter vehicules
Nb_car=1;      %nbre de voiture
for i=1:Nb_car
    car(i) = vehicle(scenario, 'ClassID', 1, 'Position', [0 0 0]);
    speed(i)=randi(2);  %vitesse
    point_livraison(i,:)= [max((randi(6)-1)*L,1*L) (randi(6)-1)*L 0]  %point de livraison du coli
    T0(i)=2*i;  %date de départ de la voiture
    Livraison_OK(i)=0;      %1 = coli livré
    stop(i)=0;     %si stop=1 la voiture est à l'arret
    fin(i)=0;
end

%ajouter obstacles
Nb_Obstacles= 7; % nbre d'obstacles
for i=1:Nb_Obstacles
    obstacle =  [max((randi(6)-1)*L,1*L) (randi(6)-1)*L 0];
    while obstacle == point_livraison
        obstacle =   [max((randi(6)-1)*L,1*L) (randi(6)-1)*L 0] ;
    end
    pos_obstacle(i,:)=obstacle; %position de l'obstacle
    car(i+Nb_car) = vehicle(scenario, 'ClassID', 1, 'Position', [pos_obstacle(i, :)]);
end
plot(scenario) 
hold on;
scatter(point_livraison(1), point_livraison(2), 'rx')


map = ones(10, 10);
while advance(scenario)
    for j=1:Nb_car
        %detection des collisions
        flag_stop=zeros(1,Nb_car);
        for i=1:Nb_car+Nb_Obstacles
            if (i~=j)  
                 [zoneX,zoneY,flag_stop(i)] = distancequadrillage(car(j),car(i));
                if max(flag_stop)==1  
                    stop(j)=1;
                    ix = pos_to_index(car(j).Position);
                    car(j).Yaw
                    car(j).Position
                    if car(j).Yaw == 180
                        map(ix(1)-1, ix(2)) = 0;
                    elseif car(j).Yaw == 90
                        map(ix(1), ix(2)+1) = 0;
                    elseif car(j).Yaw == -90
                        map(ix(1), ix(2)-1) = 0;
                    elseif car(j).Yaw == 0
                        map(ix(1)+1, ix(2)) = 0;
                    end
                else stop(j)=0;end  %la voiture s'arrete
                
            end
        end
        %deplacement des voitures
        if (scenario.SimulationTime>T0(j)) 
            [map, next_position, next_Yaw, final] = motionquadrillage(map, car(j),point_livraison(j,:),speed(j),Ts);
            %if (stop(j)==0)
                car(j).Position=next_position;
                car(j).Yaw=next_Yaw;
           % end
        end
        %verification si point de livraison atteind ; la voiture repart au
        %point de depart
        if car(j).Position==point_livraison(j,:)
            if Livraison_OK(j)==0
                Livraison_OK(j)=1;
                point_livraison(j,:)=0;
                car(j).Yaw=car(j).Yaw+180;
            else
              %  disp('arrivé');
              fin(j)=1;
              scenario.StopTime=scenario.SimulationTime; % Arreter la simulation si le vehicule revient au point de depart

            end
        end
        

    end
	updatePlots(scenario) 
    pause(0.1)
   
end
