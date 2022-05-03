function line_plot(robot,points,workspace,tilesize)
    T = transl(points);
    q = robot.ikine(T,'mask',[1 1 1 0 0 0]);
    robot.plot(q,'workspace',workspace,'tilesize',tilesize);
end