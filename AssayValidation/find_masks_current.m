function [masks_temp, masks_bg, avg_back_int, cen] = find_masks_current(rgb1, int_corr, radius_range, rnd, array_size, IMAGE)
% finds masks using a semi-interactive procedure
% parameter inputs:
% rgb1 is the image to segment
% int_corr is used to rescale the input image so the range 0-int_corr is
% used
% radius_range limits the range of possible radii extracted by the circle
% detection algorithm
% rnd is used to round so spots within the same row/column are grouped
disc_radius = 7; %pixels to extend outwards in each direction for background mask
nRow = array_size(1);
nCol = array_size(2);

sat1 = 0;
while sat1 == 0
    figure (1);;
    %K = imadjust(rgb1,[0 int_corr],[]);
    K = imadjust(rgb1);

    % restrict circle detection to only within a certain range of the image
    [hei, wid] = size(K);
    vertthresh = [0.01 0.01];
    horizthresh = [0.01 0.01];

    hthresh = [floor(vertthresh(1)*hei), hei - floor(vertthresh(2)*hei)];
    wthresh = [floor(horizthresh(1)*wid), wid - floor(horizthresh(2)*wid)];

    % initial sensitivity and threshold for circle detection
    se(1) = 0.985; se(2) = 0.01;
    [centers, radii] = imfindcircles(K,radius_range,'ObjectPolarity','bright', 'Sensitivity',se(1), 'EdgeThreshold', se(2));
    line([wthresh(1) wthresh(1)], [hthresh(1), hthresh(2)]);
    line([wthresh(2) wthresh(2)], [hthresh(1), hthresh(2)]);
    line([wthresh(1) wthresh(2)], [hthresh(1), hthresh(1)]);
    line([wthresh(1) wthresh(2)], [hthresh(2), hthresh(2)]);

    % restrict to within specified region and add background ROI
    centers = centers(centers(:,1) > wthresh(1) & centers(:,1) < wthresh(2) & centers(:,2) > hthresh(1) & centers(:,2) < hthresh(2),:);
    radii = radii(centers(:,1) > wthresh(1) & centers(:,1) < wthresh(2) & centers(:,2) > hthresh(1) & centers(:,2) < hthresh(2),:);
    
    % visualize circles, add in radii as separate column and subtract so
    % first two columns represent corner
    imshow(K)
    h = viscircles(centers,radii, 'EdgeColor','b', 'LineWidth', 2);
    centers(:,3) = radii(:,1);
    centers(:,1) = centers(:,1)-radii(:,1);
    centers(:,2) = centers(:,2)-radii(:,1);

    sat1 = menu('Circle detection looking somewhat valid?', 'Yes', 'No' );
    
    % allow user to specify sensitivity and edge threshold
    while sat1 == 2
        yy = inputdlg('If not detecting spots, enter num where: 1>num>0.985, If over detecting spots enter num where: 0.985>num>0.','Sample', [1 50]);
        se(1) = str2double(yy{1,1});
        
        % repeat detection
        [centers, radii] = imfindcircles(K,radius_range,'ObjectPolarity','bright', 'Sensitivity',se(1), 'EdgeThreshold', se(2));
        centers = centers(centers(:,1) > wthresh(1) & centers(:,1) < wthresh(2) & centers(:,2) > hthresh(1) & centers(:,2) < hthresh(2),:);
        radii = radii(centers(:,1) > wthresh(1) & centers(:,1) < wthresh(2) & centers(:,2) > hthresh(1) & centers(:,2) < hthresh(2),:);
        
        imshow(K);

        h = viscircles(centers,radii);
        centers(:,3) = radii(:,1);
        centers(:,1) = centers(:,1)-radii(:,1);
        centers(:,2) = centers(:,2)-radii(:,1);

        sat1 = menu('Good detection now?', 'Yes', 'No' );
    end
end

% add missing targets
mis = menu('Missing any targets?', 'No', 'Yes' );
if mis == 2
    new_targets = menu('how many targets to add?', '1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20',...
                                                    '21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40',...
                                                    '41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60');
    pos = zeros(new_targets,4);
    l = length(centers);
    for i = 1:new_targets
        fprintf('Select target #%d\n',i);
        if length(radii) > 1
            h = imellipse(gca, [50 50 2*mean(radii(1:end-1)) 2*mean(radii(1:end-1))]);
        else
            h = imellipse(gca, [50 50 40 40]);
        end
        position = wait(h);
        pos(i,:) = getPosition(h);
        centers (l+i, 1) = pos(i, 1);
        centers (l+i, 2) = pos(i, 2);
        centers (l+i, 3) = pos(i, 3)/2;
    end
end
% end add missing targets

%sorting spots
[a,~] = size (centers);
c = centers;
n = 0;

% group by row and sort left-to-right
c(:,4) = round((c(:,2)+n)/5,rnd)*5;
cc = sortrows(c, [4 1]);
cen = cc;
tempcen = cen;

figure(1)
imshow(K)
hold on 

% plot current sort
plot(cen(:,1),cen(:,2),'-','color', 'r', 'linewidth', 2.5)
for i =1:a
    text(cen(i,1), cen(i,2) ,num2str(i), 'color', 'b', 'fontsize', 14);   
end

% delete bad targets
xx = inputdlg('Enter space-separated numbers of the targets to be deleted:',...
             'Sample', [1 50]);
data = str2num(xx{:});
cen(data,:) = [];
% end delete bad targets

cen = sortrows(cen, 2);
cen_sort = zeros(size(cen));
for i = 1:nRow
    subset = cen(((i-1)*nCol+1):(i*nCol), :);
    cen_sort(((i-1)*nCol+1):(i*nCol), :) = sortrows(subset, 1);
end

cen = cen_sort;
%end sorting spots

% final check of the spots and making masks
[a,~] = size(cen);
figure(2)
hold on
imshow(K);

for i = 1:a
    % plot detected ROI
    text(cen(i,1), cen(i,2) ,num2str(i), 'color', 'w', 'fontsize', 1); 
    h = imellipse(gca, [cen(i,1),cen(i,2), cen(i,3)*2, cen(i,3)*2]);
    setColor(h,'g');
    % plot background ROI
    h2 = imellipse(gca, [cen(i,1)-disc_radius,cen(i,2)-disc_radius,...
        (cen(i,3)+disc_radius)*2, (cen(i,3)+disc_radius)*2]);
    setColor(h2,'y');
    position = wait(h);
    text(cen(i,1)-20, cen(i,2)-5 ,num2str(i), 'color', 'w', 'fontsize', 12); 
    pos(i,:) = getPosition(h);
    
    % make mask
    masks_temp{i,1} = createMask(h);
    masks_bg{i,1} = analyze_background(cen(i,1:3)+[cen(i,3),cen(i,3),0], size(rgb1), disc_radius);
end

saveas(gcf, ['Chip-1-mask'] , 'pdf');
% end checking

%% Calculate average background intensity 
%Grabs the center x and y values of the top sorted row of spots and
%measures the average intensity of a 100 pixel tall rectangle above the top row
tempradii = tempcen(1:nRow, 3);
tempcenters = tempcen(1:nRow, 1:2);

%rect_buffer says how far above the highest spot center in radii we 
%should start the background rectangle
rect_buffer = 1;
rect_height = 50;
bottom_y_bound = round(max(tempcenters(:,2)) - max(tempradii)*rect_buffer);
top_y_bound = round(bottom_y_bound - rect_height);
left_x_bound = round(tempcenters(1,1));
right_x_bound = round(tempcenters(nCol, 1));

%Grab the average intensity of rectangle defined above
total_intensity = 0;
counter = 0;
total_pixels = rect_height*(right_x_bound-left_x_bound);
for i = top_y_bound:(bottom_y_bound - 1)
    for j = left_x_bound:(right_x_bound - 1)
        total_intensity = total_intensity + IMAGE(i,j);
        counter = counter + 1;
    end
end

avg_back_int = total_intensity/total_pixels;

end