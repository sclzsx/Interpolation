clc, clear, close all

command = 'python main3.py';
status = system(command);

Xin = read_txt_pylist('Xin.txt');
Yin = read_txt_pylist('Yin.txt');
Xgt = read_txt_pylist('Xgt.txt');
Ygt = read_txt_pylist('Ygt.txt');

% Yout = lagrange(Xin, Yin, Xgt);

% Yout = interp1(Xin, Yin, Xgt, 'spline', 'extrap');

% Yout = interp1(Xin, Yin, Xgt, 'cubic');

Yout = interp1(Xin, Yin, Xgt, 'linear');

% c = polyfit(Xin, Yin, 2);
% Yout = polyval(c, Xgt, 1);

% values = spcrv([Xin; Yin],3);
% Yout = values(2,:);

% Yout = spline(Xin,Yin,Xgt);

Ydiff = Yout - Ygt;

plot(Xgt,Ygt)
hold on
plot(Xin, Yin)
hold on
plot(Xgt, Yout)
hold on
plot(Xgt, Ydiff)

function data = read_txt_pylist(filename)
    f = fileread(filename);
    f = f(2:end-1);
    f = split(f, ', ');
    data = zeros(1, length(f));
    for i=1:length(f)
        data(1, i) = str2double(f{i,1});
    end 
end

function yh = lagrange(x,y,xh)
    n = length(x);
    m = length(xh);
    x = x(:);
    y = y(:);
    xh = xh(:);
    yh = zeros(m,1); 
    c1 = ones(1,n-1);
    c2 = ones(m,1);
    for i=1:n
        xp = x([1:i-1 i+1:n]);
        yh = yh + y(i) * prod((xh*c1-c2*xp')./(c2*(x(i)*c1-xp')),2);
    end
    yh = yh';
end









%% 
% data_dir = './data/';
% input_dir = [data_dir 'input/'];
% gt_dir = [data_dir 'gt/'];
% 
% list_folder = dir(input_dir);
% for i = 3: length(list_folder)
%     if ~isempty(strfind(list_folder(i).name,'.sp3')) > 0
%         input_filename = list_folder(i).name;
%         gt_filename = ['GBM0MGXRAP_2021' input_filename(7:10) '000_01D_05M_ORB.SP3'];
%         
%         input_filepath = [input_dir input_filename];
% 
%         input_data = zeros(1798, 40, 3);
%         idx = 1;
%         group = 1;
%         fid = fopen(input_filepath, 'r');
%         while 1
%             line = fgetl(fid);
% 
% %             if strfind(line, 'PC19') > 0
% %                 idx = 1;
% %             end
% 
%             if strfind(line, 'PC') > 0
%                 nums = split(line, ' ');
% %                 num1 = str2double(nums{7,1});
% %                 num2 = str2double(nums{13,1});
% %                 num3 = str2double(nums{19,1});
%                 
% %                 input_data(group, idx, 1) = num1;
% %                 input_data(group, idx, 2) = num2;
% %                 input_data(group, idx, 3) = num3;
%                 
%                 idx = idx + 1;
%             end
% 
%             if idx > 40
%                 idx = 1;
%             end
%             
%             if strfind(line, 'PG32') > 0
%                 group = group + 1;
%             end
% 
%             if group > 0
%                 group = group + 1;
%             end
%             
%             if group > 10
%                 break;
%             end
%             
%         end
%         fclose(fid);
% 
% 
% 
%     end
% end
% 
% % function As, Bs, Cs = extract_data_from_sp3_file(filepath, start, end)
% %     fid = fopen(filepath, 'r');
% %     i = 1;
% %     j = 1;
% %     As = [];
% %     while start_flag && end_flag		
% %        line = fgetl(fid);
% %        
% %        
% %        if strfind(line, 'PC19') > 0
% %            start_flag = 1;
% %            
% %            As[1] = [As[1] 1];
% %            
% %        end
% %        
% %        if start_flag == 1 && strfind(line, 'PG32') > 0
% %            start_flag = 1;
% %        end
% %        
% %        disp(line);
% %     end
% % end