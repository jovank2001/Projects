%Program that takes in pictures of arrays on slides in a .tif format and
%Outputs their flourescence ratios on top of the original picture, and tablular representation of ratios
%Input: Array pictures in .tif format in file TestPics
%Output: Array pictures with overlayed spot ratios in AssayValidationOut

close all
clear all

%%Globals
radius_range = [45 50]; %range of acceptable radii for spot finding
rnd = -1; %used for rounding
int_corr = 0.2; %used for re-scaling image for masking
border = 20; %number of pixels from each edge for zoomed-in crop of array
threshold = 2; %Acceptable spot ratio

%Find Files
list=dir('**/*.tif');
num_images = floor(length(list));

%Loops over each input .fig image
for n = 1:num_images
    %% Clean and read images
    %Read File
    input_path = append("TestPics/", list(n).name);
    fid = fopen(input_path, 'r');
    fname = list(n).name;

    fname_out = append("AVO", fname(1:length(fname)-4), ".fig");
    data = fread(fid, [2048,2048], 'int16');
    fclose(fid);
    data = reshape(data, [2048, 2048]);

    % convert to intensity
    data(data < 0) = 0;
    data = rot90(data, 3);
    I = mat2gray(data);
    IMAGE = data;

    %Get user inputs 
    input(1) = 6; input(2) = 6;
    yy = inputdlg('Enter number of rows and columns with space between:',fname, [1 50]);
    input = str2num(yy{:});
    num_rows = input(1);
    num_cols = input(2);
    num_spots = num_cols * num_rows
    
    %Write adjusted images to PNG, [0 0.5], [0 1]
    Im_out = imadjust(I);
    %imwrite(Im_out, fname);
    imshow(Im_out);

    %% Masking 
    %make array's masks
    array_size = [num_rows, num_cols];
    [MASKS(:,1), MASKS_BG(:,1), avg_back_int, cen] = find_masks_current(Im_out, int_corr, radius_range, rnd, array_size, IMAGE);
    [target_number,~] = size(MASKS(:,1));
    save('Masks.mat','MASKS', 'MASKS_BG');
    save('target_number.mat','target_number');
    close all

    fprintf("Wait....\n");

    %calculate each spot's raw intensity
    DATA = cell(1);
    DATABG = cell(1);

    %target intensity
    for ii = 1:target_number
        MASK = MASKS{ii};
        MASKBG = MASKS_BG{ii};
        DATA{1,1}(ii) = sum(sum(double(IMAGE) .* double(MASK))) / sum(double(MASK(:)));
        D = DATA{1,1};
        DATABG{1,1}(ii) = sum(sum(double(IMAGE) .* double(MASKBG))) / sum(double(MASKBG(:)));
        DATA{1,2}(ii) = DATA{1,1}(ii) - DATABG{1,1}(ii);
    end


    save('raw_DATA.mat','DATA','DATABG');

    %% Determine Spot Array ratios
    %Add to this list and to avg_control_int if additional POS control spots
    %Spot intensity of each POS control spot
    top_left_spot = DATA{1,1}(1);
    top_right_spot = DATA{1,1}(num_cols);
    two_three_spot = DATA{1,1}(num_cols + 3);
    bottom_left_spot = DATA{1,1}(((num_rows - 1) * num_cols) + 1);
    bottom_right_spot = DATA{1,1}(num_rows * num_cols);
    num_pos_control_spots = 5;

    %Average intensity of each positive control spot
    avg_control_int = (top_left_spot + top_right_spot + two_three_spot + ...
        bottom_left_spot + bottom_right_spot)/num_pos_control_spots;
    
    inten_ratio = (avg_control_int - avg_back_int) ./ (DATA{1,1} - avg_back_int);
    %Draw array intensity ratios (inten_ratio) on original pictures
    figure(3)
    hold on
    imshow(I)
    for i = 1:num_spots
        text(cen(i,1), cen(i,2) ,num2str(round(inten_ratio(i), 1)), 'color', 'r', 'fontsize', 12); 
    end
    out_path = append('AssayValidationOut/',"AVI", fname(1:length(fname)-4), ".fig");
    savefig(out_path);
    
    
    %Create list containing each intensity ratio and table for excel sheet 
    inten_ratio = inten_ratio';
    spot_num = [1:num_spots]';
    above_thresh = zeros(num_spots, 1);
    for j = 1:num_spots
        if inten_ratio(j) > threshold
            above_thresh(j) = 1;
        else
            above_thresh(j) = 0;
        end
    end
    
    %Set PC values and write to excel
    above_thresh(1) = NaN;
    above_thresh(num_rows) = NaN;
    above_thresh(num_rows + 3) = NaN;
    above_thresh(num_spots - num_rows + 1) = NaN;
    above_thresh(num_spots) = NaN;
    T_out = table(spot_num, inten_ratio, above_thresh); 
    out_path = append('AssayValidationOut/',"AVE", fname(1:length(fname)-4), ".xlsx");
    writetable(T_out,out_path,'Sheet', 1);
    
end

