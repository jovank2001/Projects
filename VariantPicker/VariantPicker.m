clear, clc
%Written by Jovan Koledin on 6/10/2022 for Torus BioSystems
%START THIS PROGRAM INSIDE A RUN FOLDER CONTAINING IN_FILE_NAME 
%IN_FILE_NAME: Has the enough of each files name to make it unique
%OUT_FILE_NAME: Where you want the variant name printed out
IN_FILE_NAME = 'runs.txt';
OUT_FILE_NAME = 'SARS- COV-2 Variants.txt';

%What this program is comparing:
    %row 3 columns 2-5 (484s)
    INDEX_484s = [14:17];
    %row 4: columns 1-2 (452s)
    INDEX_452s = [19:20];
    %row 4: columns:3-5 && row5 Column 6 (501s)
    INDEX_501s = [21:23, 30];
    %row 5: columns 1-3 (417s)
    INDEX_417s = [25:27];
    %row 5: Columns 4-5 (614s)
    INDEX_614s = [28:29];

%SARS- COV-2 Variants:
    %Wuhan: 484E, 452L, 501N, 417K, 614D
    Wuhan = [14, 19, 21, 25, 28];
    %Alpha: 484E, 452L, 501Y, 417K, 614G
    Alpha = [14, 19, 22, 25, 29];
    %Beta: 484K, 452L, 501Y, 417N, 614G
    Beta = [16, 19, 22, 26, 29];
    %Gamma: 484K, 452L, 501Y, 417T, 614G
    Gamma = [16, 19, 22, 27, 29];
    %Delta: 484E, 452R, 501N, 417K, 614G
    Delta = [14, 20, 21, 25, 29];
    %Kappa: 484Q, 452R, 501N, 417K, 614G
    Kappa = [17, 20, 21, 25, 29];
    %OmicronBA1: 484A, 452L, 501Y-2, 417N, 614G
    OmicronBA1 = [15, 19, 23, 26, 29];
    %OmicronBA2: 484A, 452L, 501Y-2.2, 417N, 614G
    OmicronBA2 = [15, 19, 23, 26, 29]; 
    
%Load names of panel 
spotfile = '..\..\..\MATLAB\Chip_configs\Respiratory BARDA Panel V2'; %location of directory with array configs
load(spotfile);
global tar_names 
tar_names = tar_names_Optikos;

%Load runs.txt
fid = fopen(IN_FILE_NAME);
runs_to_read = readlines(IN_FILE_NAME);
num_runs = length(runs_to_read);


%Loop through the runs and write out the Variants inside each run folder
for i = 1:num_runs
    %Winner array
    winners = [];
    %Search for run folder and enter it
    cd ..
    list = dir();
    for l = 1:length(list)
        if contains(list(l).name,runs_to_read(i))
            cd(list(l).name)
            break
        end  
    end
   
    %Load DATA
    DATA = load('DATA.mat');
    FIGURE = 4;%1 = raw, 2 = background_sub, 3 = norm, 4 = baseline_sub
    Figure = DATA.DATA{FIGURE};
    
    %Open outfile
    fid = fopen(OUT_FILE_NAME, 'w');
    
    %Add 484s winner
    winners = [winners, compare_mutations(INDEX_484s, fid, Figure, '484')];
    %Add 452s winner
    winners = [winners, compare_mutations(INDEX_452s, fid, Figure, '452')];
    %Add 501s winner
    winners = [winners, compare_mutations(INDEX_501s, fid, Figure, '501')];
    %Add 417s winner
    winners = [winners, compare_mutations(INDEX_417s, fid, Figure, '417')];
    %Add 614s winner
    winners = [winners, compare_mutations(INDEX_614s, fid, Figure, '614')];
    
    %Find final variant and close file
    if isequal(winners, Wuhan)
        fprintf(fid, "This corresponds to the Wuhan variant.\n");
        fprintf("This corresponds to the Wuhan variant.\n");
    elseif isequal(winners, Alpha)
        fprintf(fid, "This corresponds to the Alpha variant.\n");
        fprintf("This corresponds to the Alpha variant.\n");
    elseif isequal(winners, Beta)
        fprintf(fid, "This corresponds to the Beta variant.\n");
        fprintf("This corresponds to the Beta variant.\n");
    elseif isequal(winners, Gamma)
        fprintf(fid, "This corresponds to the Gamma variant.\n");
        fprintf("This corresponds to the Gamma variant.\n");
    elseif isequal(winners, Delta)
        fprintf(fid, "This corresponds to the Delta variant.\n");
        fprintf("This corresponds to the Delta variant.\n");
    elseif isequal(winners, Kappa)
        fprintf(fid, "This corresponds to the Kappa variant.\n");
        fprintf("This corresponds to the Kappa variant.\n");
    elseif isequal(winners, OmicronBA1)
        fprintf(fid, "This corresponds to the Omicron BA.1 variant.\n");
        fprintf("This corresponds to the Omicron BA.1 variant.\n");
    elseif isequal(winners, OmicronBA2)
        fprintf(fid, "This corresponds to the Omicron BA.2 variant.\n");
        fprintf("This corresponds to the Omicron BA.2 variant.\n");
    else
        fprintf(fid, "Couldnt find a variant match.\n");
        fprintf("Couldnt find a variant match.\n");
    end
       
    fclose(fid);
    
end

%Takes in the index range of mutations to be compared and writes out the
%mutation with the steepest max slope to the fid
function index = compare_mutations(mutation_index, fid, Figure, mutation_name)
    %Misc.
    max_slope = 0;
    index = 0;
    [num_rows, num_columns] = size(Figure);
    global tar_names
    
    %Check mutations and add winner to best_mutation
    for c = mutation_index
        max_slope_temp = 0;
        %Find max slope for current mutation
        for r = 10:num_rows
            if r < (num_rows-3)
                curr_slope = (abs(Figure(r, c) - Figure(r + 3,c))/4);
                if curr_slope > max_slope_temp
                    max_slope_temp = curr_slope;
                end
            end
        end
        %Check against current top mutation
        if max_slope_temp > max_slope
            max_slope = max_slope_temp;
            index = c;
        end
    end
    
    %Write out findings
    name = tar_names{index};
    fprintf(fid, "The best mutation for the %s set: %s\n", mutation_name, name);
end
