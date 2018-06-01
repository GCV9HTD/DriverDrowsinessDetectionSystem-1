close all;
Data = dufeFINAL; %the imported EAR/MAR/YAWN values,
Ones = 1;         %the list can be changed to any other list of values
Twos = 2;         
fps=18.7; %this is a changable value, depends on the video

%checking the Original Matrix "Data from Linux script"
for log = Data(:,1) == Twos  %if first column is '2', Then copy only
    Only2 = Data(log,:)  %the values related to 2 into a new matrix
end                     

%Checking the Original Matrix "Data from Linux script"
for log = Data(:,1) == Ones %if first column is '1', Then copy only
    Only1 = Data(log,:)  %the values related to 1 into a new matrix
end         

%%% plotting face 1 %%% 
x=Only1(:,2); %Frames column set to x 
y1=Only1(:,3);%EAR column set to y1
y2=Only1(:,4);%MAR column set to y2
y3=Only1(:,5);%Yawn detector column set to y3

face1 = subplot(2,1,1)
plot(x,y1,'Red',x,y2, 'Blue',x,y3,'Black')
title('Face1 (left)')
xlabel('Frames')
ylabel('Eye Aspect Ratio & MAR')
legend('EAR','MAR', 'Yawn Detector')
grid(face1, 'on')
grid minor

%%% plotting face 2 %%%
x=Only2(:,2);
y1=Only2(:,3);
y2=Only2(:,4);
y3=Only2(:,5);
face2 = subplot(2,1,2);

plot(x,y1, 'Red',x,y2, 'Blue',x,y3, 'Black')
title('Face2 (Right)')
xlabel('Frames')
ylabel('Eye Aspect Ratio & MAR')
legend('EAR','MAR', 'Yawn Detector')
grid(face2, 'on')
grid minor

%%% setting axis limits for both face plots (x and y limits in plot) %%%
axis([face1 face2],[101500 104100 -0.1 1.1]) %%these limits are specific to desired location in a long set of data

%%% BELOW CAN BE USED TO CREATE MORE PLOTS ###
% figure;
% 
% %%% plotting face 1 MORE FRAMES %%% 
% x=Only1(:,2);
% y1=Only1(:,3);
% y2=Only1(:,4);
% y3=Only1(:,5);
% face1 = subplot(2,1,1)
% 
% plot(x,y1,x,y2,x,y3)
% title('Face1 (left)')
% xlabel('Frames')
% ylabel('Eye Aspect Ratio & MAR')
% legend('EAR','MAR')
% grid(face1, 'on')
% grid minor
% 
% %%% plotting face 2 %%%
% x=Only2(:,2);
% y1=Only2(:,3);
% y2=Only2(:,4);
% y3=Only2(:,5);
% face2 = subplot(2,1,2)
% 
% plot(x,y1,x,y2,x,y3)
% title('Face2 (Right)')
% xlabel('Frames')
% ylabel('Eye Aspect Ratio & MAR')
% legend('EAR','MAR')
% grid(face2, 'on')
% grid minor
% 
% %%% setting axis limits for both face plots %%%
% axis([face1 face2],[3500 7000 0 1.1])
% 
% figure;
% %%% plotting face 1 MORE FRAMES%%% 
% x=Only1(:,2);
% y1=Only1(:,3);
% y2=Only1(:,4);
% y3=Only1(:,5);
% face1 = subplot(2,1,1)
% 
% plot(x,y1,x,y2,x,y3)
% title('Face1 (left)')
% xlabel('Frames')
% ylabel('Eye Aspect Ratio & MAR')
% legend('EAR','MAR')
% grid(face1, 'on')
% grid minor
% 
% %%% plotting face 2 MORE FRAMES %%%
% x=Only2(:,2);
% y1=Only2(:,3);
% y2=Only2(:,4);
% y3=Only2(:,5);
% face2 = subplot(2,1,2)
% 
% plot(x,y1,x,y2,x,y3)
% title('Face2 (Right)')
% xlabel('Frames')
% ylabel('Eye Aspect Ratio & MAR')
% legend('EAR','MAR')
% grid(face2, 'on')
% grid minor
% %%% setting axis limits for both face plots %%%
% axis([face1 face2],[7000 10500 0 1.1]) %Previously 10500
% 
% figure;
% %%% plotting face 1 MORE FRAMES%%% 
% x=Only1(:,2);
% y1=Only1(:,3);
% y2=Only1(:,4);
% y3=Only1(:,5);
% face1 = subplot(2,1,1)
% 
% plot(x,y1,x,y2,x,y3)
% title('Face1 (left)')
% xlabel('Frames')
% ylabel('Eye Aspect Ratio & MAR')
% legend('EAR','MAR')
% grid(face1, 'on')
% grid minor
% 
% %%% plotting face 2 MORE FRAMES %%%
% x=Only2(:,2);
% y1=Only2(:,3);
% y2=Only2(:,4);
% y3=Only2(:,5);
% y1Mean = mean(y1, 2)
% y2Mean = mean(y2, 2)
% face2 = subplot(2,1,2)
% 
% plot(x,y1Mean,x,y2Mean,x,y3)
% title('Face2 (Right)')
% xlabel('Frames')
% ylabel('Eye Aspect Ratio & MAR')
% legend('EAR','MAR')
% grid(face2, 'on')
% grid minor
% %%% setting axis limits for both face plots %%%
% axis([face1 face2],[10500 14000 0 1.1]) %HEREEEEE was 14000