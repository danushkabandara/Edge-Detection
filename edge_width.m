I = imread('3.jpg');
I = rgb2gray(I);
[~,threshold] = edge(I,'sobel');
fudgeFactor = 0.5;
BWs = edge(I,'sobel',threshold * .5);
se90 = strel('line',10,90);
se0 = strel('line',3,0);
BWsdil = imdilate(BWs,[se90 se0]);
BWdfill = imfill(BWsdil,'holes');
BWdfill = bwareafilt(BWdfill,1);

seD = strel('diamond',1);
BWfinal = imerode(BWdfill,seD);
BWfinal = imerode(BWfinal,seD);
imshow(I)
hold on;
top_line = [];
bottom_line = [];
for K = 1 : size(BWfinal,2)
  thiscolumn = BWfinal(:,K,:);
  first_non_zero_row_pos = find(thiscolumn,1,'first');% first non zero element
  last_non_zero_row_pos = find(thiscolumn,1,'last');% last non zero element
  top_line = [top_line; first_non_zero_row_pos];
  bottom_line = [bottom_line; last_non_zero_row_pos];
 % plot(K, last_non_zero_row_pos, 'y*', 'LineWidth', 1, 'MarkerSize', 1);
  %plot(K, row_median, 'b*', 'LineWidth', 1, 'MarkerSize', 1);
end
top_line = transpose(top_line)
bottom_line = transpose(bottom_line)
x_coords = [1:1:size(BWfinal,2)];
p1 = polyfit(x_coords, top_line,1);
f1 = polyval(p1,x_coords);
p2 = polyfit(x_coords, bottom_line,1);
f2 = polyval(p2,x_coords);
plot(x_coords, f1,'r*', 'LineWidth', 1, 'MarkerSize', 2);
plot(x_coords, f2,'b*', 'LineWidth', 1, 'MarkerSize', 2);