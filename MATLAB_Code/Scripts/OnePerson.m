d=importdata('DA_YES.txt'); %Importing data

x=d(:,1);%Frames set to x
y1=d(:,2);%EAR set to y1
y2=d(:,3); %MAR set to y2
y3=d(:,4); %Yawn detector set to y3 

plot(x,y1,'Red',x,y2,'Blue',x, y3, 'Black')
grid on
grid minor
xlabel('Frames')
ylabel('Eye Aspect Ratio & MAR')
legend('EAR', 'MAR', 'Yawn Detector' )
xlim([0 inf])
ylim([-0.1 1.2])

%% this command counts the number of yawns (rough estimation)
for ear = d(:,4) == 1
    %yawn = d(ear,:)
    NoOfYawn = sum(ear)/15
end
