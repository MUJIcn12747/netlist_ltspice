% 设置主目录路径（当前文件夹下的 outputFile 文件夹）
main_folder = fullfile(pwd, 'outputFile');

% 弹出文件夹选择对话框，限制用户只能选择 mvm 或 inv 文件夹
selected_folder = uigetdir(main_folder, 'Choose mvm or inv or pinv or eig');

% 如果用户没有选择文件夹，返回的路径为空
if selected_folder == 0
    disp('No choosen folder');
else
    disp(['choosen folder: ', selected_folder]);
end

% 假设 cmp1, cmp2, ..., cmpN 是子文件夹
cmp_folders = dir(fullfile(selected_folder, 'cmp*'));  % 找到所有以 "cmp" 开头的文件夹

% 遍历每个 cmp 文件夹
for i = 1:length(cmp_folders)
    cmp_folder_path = fullfile(selected_folder, cmp_folders(i).name);  % 当前 cmp 文件夹路径
    txt_files = dir(fullfile(cmp_folder_path, '*.txt'));  % 找到所有 .txt 文件
    
    % 遍历每个 txt 文件
    for j = 1:length(txt_files)
        file_path = fullfile(cmp_folder_path, txt_files(j).name);  % 当前 .txt 文件路径
        
        % 打开文件并读取数据
        fid = fopen(file_path, 'rt');
        if fid == -1
            warning('无法打开文件: %s', file_path);
            continue;
        end
        
        header = fgetl(fid);  % 读取第一行标题（例如 I 和 V）
        data = fscanf(fid, '%f %f', [2, Inf])';  % 按列存储数据
        fclose(fid);
        
        % 确保数据读取成功
        if isempty(data)
            warning('文件 %s 中没有有效数据。', file_path);
            continue;
        end
        
        % 分割标题为列标题
        header_titles = strsplit(header);
        
        % 提取 I 和 V 数据
        ideal = data(:, 1);  % 第一列为 ideal
        test = data(:, 2);  % 第二列为 test
       
         % 创建图像但不显示
        fig = figure('Visible', 'off');
        scatter(ideal, test, 'filled');  % 绘制填充散点图
        hold on;  % 保持图像
        
        % 添加对称参考线
        min_val = 0;  % 原点 (0, 0)
        max_val_x = max(ideal);  % ideal 的最大值
        max_val_y = max(test);  % test 的最大值
        plot([min_val, max_val_x], [min_val, max_val_y], 'r--', 'LineWidth', 1.5);  % 绘制对角线
        
        %设置图像属性
        xlabel(header_titles{1});  % 横坐标标签
        ylabel(header_titles{2});  % 纵坐标标签
        title(sprintf('Scatter Plot: %s', txt_files(j).name));  % 设置标题为文件名
        grid on;  % 显示网格
        hold off;  % 结束叠加模式
        
        % 保存图像到文件
        output_dir = fullfile(selected_folder, 'output_plots');  % 保存图像的输出目录
        if ~exist(output_dir, 'dir')
            mkdir(output_dir);  % 创建目录
        end
        saveas(fig, fullfile(output_dir, sprintf('%s_%s.png', cmp_folders(i).name, txt_files(j).name)));
        close(fig);  % 关闭图像以释放资源
    end
end
