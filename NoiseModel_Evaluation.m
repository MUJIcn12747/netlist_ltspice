% 获取当前文件夹下的 Source、Model 和 Original 文件夹路径
main_folder = fullfile(pwd, 'NoiseTran');
source_folder = fullfile(main_folder, 'Source');
model_folder = fullfile(main_folder, 'Model');
original_folder = fullfile(main_folder, 'Original');

% disp(main_folder);
% disp(source_folder);
% disp(model_folder);
% disp(original_folder);

% 获取 Source、Model 和 Original 文件夹中的所有 txt 文件
source_files = dir(fullfile(source_folder, '*.txt'));
model_files = dir(fullfile(model_folder, '*.txt'));
original_files = dir(fullfile(original_folder, '*.txt'));

% 确保三个文件夹中都有相同数量的文件
N = 25;

% 初始化数据存储变量
source_means = zeros(1, N);
model_means = zeros(1, N);
original_means = zeros(1, N);

% disp('Source folder files:');
% disp({source_files.name});
% 
% disp('Model folder files:');
% disp({model_files.name});
% 
% disp('Original folder files:');
% disp({original_files.name});

% 计算每个文件的平均值
for i = 1:N
    % 读取 Source 文件中的数据并计算平均值
    source_data = load(fullfile(source_folder, source_files(i).name));
    source_means(i) = 100 * mean(source_data);
    
    % 读取 Model 文件中的数据并计算平均值
    model_data = load(fullfile(model_folder, model_files(i).name));
    model_means(i) = 100 * mean(model_data);
    
    % 读取 Original 文件中的数据并计算平均值
    original_data = load(fullfile(original_folder, original_files(i).name));
    original_means(i) = 100 * mean(original_data);
end

% 绘制图像
figure;
hold on;

% 绘制 Source、Model 和 Original 的平均值曲线
plot(1:N, source_means, '-o', 'DisplayName', 'Noise Source', 'LineWidth', 2, 'Color', 'r');
plot(1:N, model_means, '-x', 'DisplayName', 'Noise Model', 'LineWidth', 2, 'Color', 'b');
plot(1:N, original_means, '-s', 'DisplayName', 'Without Noise', 'LineWidth', 2, 'Color', 'g');  % 新增 Original 曲线

% 添加标题、标签和图例
title('Noise Model Evaluation');
xlabel('Input cases');
ylabel('Average Relative Error(%)');
grid on;
legend('show', 'Location', 'northeastoutside');
hold off;

% 保存图像到 NoiseTran 文件夹
save_path = fullfile(main_folder, 'Average_Relative_Error.png');  % 设置保存路径和文件名
saveas(gcf, save_path);  % 保存图像为 PNG 文件
