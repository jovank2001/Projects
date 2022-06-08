%Copy your ThermoFisher Primer Dimer results into "ThermoAnalysis.txt"
%Specify dimensions of matrix(NUM is number of sequences)
clear, clc
NUM = 40;
NUM_COLUMNS = NUM;
NUM_ROWS = NUM_COLUMNS;
G_C_WEIGHT = 1.5;
A_T_WEIGHT = 1;

%Generate empty 2D output matrix
OUT_MATRIX = strings(NUM_ROWS + 1);

%Open file and read from it
fid = fopen("ThermoAnalysisMAT.txt");
input = readlines("ThermoAnalysisMAT.txt");

%Sort input string into cell array
tline = fgetl(fid);
input_cell = cell(0,1);
while ischar(tline)
    input_cell{end+1,1} = tline;
    tline = fgetl(fid);
end

%Iterate through input_cell and divide into 2d array with each set divided
%into its own row
line_lengths = strlength(input);
num_lines = length(input_cell);
sorted_2D = [];
internal_set = [];
for k=1:num_lines
    if line_lengths(k) ~= 0
        internal_set = [internal_set, input_cell(k)];
    else
        %Correct for fact internal_sets will have variable size
        while length(internal_set) ~= 5
            internal_set = [internal_set, " "];
        end
        
        sorted_2D = [sorted_2D; internal_set];
        internal_set = [];
    end
end

%Locate index of self dimers and cross primer dimers
length2D = length(sorted_2D);
index_self_dimers = 0;
index_cross_dimers = 0;
for i=1:length2D
    if contains(sorted_2D(i,1), 'Self-Dimers:')
        index_self_dimers = i;
    end
    if contains(sorted_2D(i,1), 'Cross Primer Dimers:')
        index_cross_dimers = i;
    end
end


%Create self dimer matrix and clean up the labels
self_dimer_matrix = sorted_2D(index_self_dimers + 1:index_cross_dimers - 2, :);
if ~isempty(self_dimer_matrix)
    self_dimer_matrix_names = split(self_dimer_matrix(:,1));
    self_dimer_matrix(:,1) = self_dimer_matrix_names(:,4);
end

%Create cross primer dimers matrix and clean up the labels
cross_dimer_matrix = sorted_2D(index_cross_dimers + 1:length2D, :);
for j=1:length(cross_dimer_matrix)
    if contains(cross_dimer_matrix(j,1), 'with')
        names_temp = split(cross_dimer_matrix(j,1));
        cross_dimer_matrix(j,1) = append(names_temp(1), ' ', names_temp(3));
    end
end


%Add rows and columns labels in OUT_MATRIX according to order they appear
%in cross_dimer_matrix (first pass)
c = 1;
for j=1:length(cross_dimer_matrix)
    if ~contains(cross_dimer_matrix(j,1), '>')
        names_temp = split(cross_dimer_matrix(j,1));
        if names_temp(1) ~= OUT_MATRIX(1,c)
            c = c + 1;
            OUT_MATRIX(1,c) = names_temp(1);
            OUT_MATRIX(c,1) = names_temp(1);
        end
        
    end
end

%Add rows and columns labels in OUT_MATRIX according to order they appear
%in cross_dimer_matrix (second pass)
%Also add in self dimer names if they aren't encountered in
%cross_dimer_matrix
for j=1:length(cross_dimer_matrix)
    if ~contains(cross_dimer_matrix(j,1), '>')
        names_temp = split(cross_dimer_matrix(j,1));
        new_name = names_temp(2);
        f = 1;
        for co=1:length(OUT_MATRIX)
            if OUT_MATRIX(1,co) == new_name
                f = 0;
            end
        end
        if f == 1
            c = c + 1;
            OUT_MATRIX(1,c) = names_temp(2);
            OUT_MATRIX(c,1) = names_temp(2);
        end
    end
        
end
%Add in self dimer names just in case
for j=1:length(self_dimer_matrix)
        name_temp = self_dimer_matrix(1);
        f = 1;
        for co=1:length(OUT_MATRIX)
            if OUT_MATRIX(1,co) == name_temp
                f = 0;
            end
        end
        if f == 1
            c = c + 1;
            OUT_MATRIX(1,c) = name_temp;
            OUT_MATRIX(c,1) = name_temp;
        end
        
    
end

count_cross = 0;
total_weight_cross = 0;
%Add cross dimer weighted interactions to OUT_MATRIX 
for j=1:length(cross_dimer_matrix)
    
    %Iterate through top sequence and interactions strings 
    %Returning the weighted interaction_value
    top_sequence = char(cross_dimer_matrix(j,3));
    interactions_representation = char(cross_dimer_matrix(j,4));
    sequence_length = length(top_sequence);
    interactions_lengths = length(interactions_representation);
    weighted_interactions = 0;
    
    %If, to make sure top_sequence is in format: 5-aacctgtttcaa...
    if top_sequence(1) == '5'
        for t = 1:interactions_lengths
            %weighted_interactions += 1.5
            if top_sequence(t) == 'g' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + G_C_WEIGHT;
            end
            %weighted_interactions += 1.5
            if top_sequence(t) == 'c' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + G_C_WEIGHT;
            end
            %weighted_interactions += 1
            if top_sequence(t) == 'a' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + A_T_WEIGHT;
            end
            %weighted_interactions += 1
            if top_sequence(t) == 't' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + A_T_WEIGHT;
            end
            
        end
        %Now add that weighted value to its correct location on OUT_MATRIX
        names_temp = split(cross_dimer_matrix(j,1));
        name_col = names_temp(1);
        name_row = names_temp(2);
    end
    
    
    
    %Search for location in OUT_MATRIX and throw in weighted_interactions
    for c=2:(NUM_COLUMNS + 1)
        if strcmp(OUT_MATRIX(1, c), name_col)
            for r=2:(NUM_ROWS + 1)
                if strcmp(OUT_MATRIX(r, 1), name_row)
                    OUT_MATRIX(r, c) = string(weighted_interactions);
                    total_weight_cross = total_weight_cross + weighted_interactions;
                    count_cross = count_cross + 1;
                end
            end
        end
    end
end

%Search for empty location in OUT_MATRIX and throw in 0 if empty
for c=2:(NUM_COLUMNS + 1)
      for r=2:(NUM_ROWS + 1)
          if strcmp(OUT_MATRIX(r, c), "")
                    OUT_MATRIX(r, c) = "0";
          end
      end
end





%Add self dimers to OUT_MATRIX (Can be downsized to save on CPU)
count_self = 0;
total_weight_self = 0;
%Add cross dimer weighted interactions to OUT_MATRIX 
if ~isempty(self_dimer_matrix)
    
    for j=1:length(self_dimer_matrix)
    
        %Iterate through top sequence and interactions strings
        %Returning the weighted interaction_value
        top_sequence = char(self_dimer_matrix(j,2));
        interactions_representation = char(self_dimer_matrix(j,3));
        sequence_length = length(top_sequence);
        interactions_lengths = length(interactions_representation);
        weighted_interactions = 0;
        
        
        
        for t = 1:interactions_lengths
            %weighted_interactions += 1.5
            disp(interactions_lengths)
            if top_sequence(t) == 'g' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + G_C_WEIGHT;
            end
            %weighted_interactions += 1.5
            if top_sequence(t) == 'c' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + G_C_WEIGHT;
            end
            %weighted_interactions += 1
            if top_sequence(t) == 'a' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + A_T_WEIGHT;
            end
            %weighted_interactions += 1
            if top_sequence(t) == 't' && interactions_representation(t) == '|'
                weighted_interactions = weighted_interactions + A_T_WEIGHT;
            end

        end
        %Now add that weighted value to its correct location on OUT_MATRIX
        names_col = self_dimer_matrix(j,1);
        
        c = 0;
        r = 0;
        %Search for location in OUT_MATRIX and throw in weighted_interactions
        for c=2:(NUM_COLUMNS + 1)
            if strcmp(OUT_MATRIX(1, c), names_col)
                for r=2:(NUM_ROWS + 1)
                    if strcmp(OUT_MATRIX(r, 1), names_col)
                        
                        OUT_MATRIX(r, c) = string(weighted_interactions);
                        total_weight_self = total_weight_self + weighted_interactions;
                        count_self = count_self + 1;
                    end
                end
            end
        end
    
        
        
        
    end
end

disp(OUT_MATRIX)
fprintf("Total cross dimer interactions: %.0f\n", count_cross)
fprintf("Total cross dimer interactions weight: %.0f\n", total_weight_cross)
fprintf("Total self dimer interactions: %.0f\n", count_self)
fprintf("Total self dimer interactions weight: %.0f\n", total_weight_self)
