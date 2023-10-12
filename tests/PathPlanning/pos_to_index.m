function pos = pos_to_index(pos)
    pos = [round(pos(1)/10)+1, round(pos(2)/10)+1];
end