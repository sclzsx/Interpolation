clc, clear, close all

data_dir = './data/';
input_dir = [data_dir 'input/'];
gt_dir = [data_dir 'gt/'];

list_folder = dir(input_dir);
for i = 3: length(list_folder)
    if ~isempty(strfind(list_folder(i).name,'.sp3')) > 0
        input_filename = list_folder(i).name;
        gt_filename = ['GBM0MGXRAP_2021' input_filename(7:10) '000_01D_05M_ORB.SP3'];
        
        input_filepath = [input_dir input_filename];

        input_data = zeros(1798, 40, 3);
        idx = 1;
        group = 1;
        fid = fopen(input_filepath, 'r');
        while 1
            line = fgetl(fid);

%             if strfind(line, 'PC19') > 0
%                 idx = 1;
%             end

            if strfind(line, 'PC') > 0
                nums = split(line, ' ');
%                 num1 = str2double(nums{7,1});
%                 num2 = str2double(nums{13,1});
%                 num3 = str2double(nums{19,1});
                
%                 input_data(group, idx, 1) = num1;
%                 input_data(group, idx, 2) = num2;
%                 input_data(group, idx, 3) = num3;
                
                idx = idx + 1;
            end

            if idx > 40
                idx = 1;
            end
            
            if strfind(line, 'PG32') > 0
                group = group + 1;
            end

            if group > 0
                group = group + 1;
            end
            
            if group > 10
                break;
            end
            
        end
        fclose(fid);



    end
end

% function As, Bs, Cs = extract_data_from_sp3_file(filepath, start, end)
%     fid = fopen(filepath, 'r');
%     i = 1;
%     j = 1;
%     As = [];
%     while start_flag && end_flag		
%        line = fgetl(fid);
%        
%        
%        if strfind(line, 'PC19') > 0
%            start_flag = 1;
%            
%            As[1] = [As[1] 1];
%            
%        end
%        
%        if start_flag == 1 && strfind(line, 'PG32') > 0
%            start_flag = 1;
%        end
%        
%        disp(line);
%     end
% end