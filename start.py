import tkinter as tk
import random
from PIL import Image, ImageTk

# 从文件加载参与者编号的函数
def load_participants_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            participants = file.read().splitlines()  # 逐行读取并去除换行符
        return participants
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# 保存抽奖结果到文件
def save_winners_to_file(pool_name, winners):
    file_name = f"winners_{pool_name}.txt"
    try:
        with open(file_name, "a", encoding="utf-8") as file:
            for winner in winners:
                file.write(winner + "\n")  # 逐行追加写入
        print(f"保存结果到 {file_name} 完成！")
    except Exception as e:
        print(f"Error writing to {file_name}: {e}")

# 加载两个奖池
pool_1 = load_participants_from_file("pool_1.txt")
pool_2 = load_participants_from_file("pool_2.txt")

# 已经抽中的参与者列表
winners_1 = []
winners_2 = []

rolling_bg_path = "rolling_background.jpg"  # 背景图路径

# 创建主窗口
root = tk.Tk()
root.title("抽奖软件")

# 设置全屏模式
root.attributes("-fullscreen", True)

# 用于显示背景的标签
bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)  # 使背景填满整个窗口

# 选择卡池的变量
pool_var = tk.StringVar(value="pool_1")

# 滚动状态
scrolling = False  # 是否正在滚动数字
rolling_labels = []

# 更新背景图像
def update_background(bg_path):
    try:
        # 获取窗口大小
        width = root.winfo_width()
        height = root.winfo_height()
        image = Image.open(bg_path)
        image = image.resize((width, height), Image.Resampling.LANCZOS)  # 使用 LANCZOS
        bg_image = ImageTk.PhotoImage(image)
        bg_label.config(image=bg_image)
        bg_label.image = bg_image  # 保留图像引用，防止被垃圾回收
    except Exception as e:
        print(f"Error loading background image: {e}")

# 延迟更新背景图像，确保窗口大小已确定
def delayed_update_background():
    update_background(rolling_bg_path)

# 显示抽奖环节文字
def show_lottery_stage():
    stage_label = tk.Label(root, text="抽奖环节", font=("YEFONTMengChangAnXinKai", 100), fg="#ffde00", bg="#b51112")
    stage_label.place(relx=0.5, rely=0.5, anchor="center")

    def hide_label():
        stage_label.destroy()

    return hide_label

hide_stage_label = show_lottery_stage()

# 抽奖结果显示窗口
def show_result_window(single_draw=True):
    global scrolling, rolling_labels

    # 隐藏抽奖环节文字
    if hide_stage_label:
        hide_stage_label()

    # 创建新窗口显示结果
    result_window = tk.Toplevel(root)
    result_window.title("抽奖结果")
    result_window.attributes("-fullscreen", True)  # 设置全屏

    # 加载并设置背景
    try:
        width = result_window.winfo_screenwidth()
        height = result_window.winfo_screenheight()
        image = Image.open(rolling_bg_path)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(result_window, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_image  # 防止被垃圾回收
    except Exception as e:
        print(f"Error loading rolling background: {e}")

    # 显示滚动数字的标签
    rolling_labels = []
    winners = []

    def update_rolling_number():
        for label in rolling_labels:
            if scrolling:
                # 从奖池中随机抽选一个参与者并显示
                participant = random.choice(pool_1 if pool_var.get() == "pool_1" else pool_2)
                label.config(text=participant)  # 设置标签为选中的参与者
        if scrolling:
            result_window.after(50, update_rolling_number)  # 每 50ms 更新显示

    def stop_and_display(event):
        global scrolling
        scrolling = False

        if single_draw:
            final_result = draw_lottery()
            winners.append(final_result)
            rolling_labels[0].config(text=str(final_result))
        else:
            for label in rolling_labels:
                final_result = draw_lottery()
                winners.append(final_result)
                label.config(text=str(final_result))

        save_winners_to_file(pool_var.get(), winners)
        result_window.unbind('<Key>')  # 解除键盘绑定
        result_window.bind('5', lambda e: result_window.destroy())  # 按键 '5' 关闭窗口

    # 启动滚动数字
    scrolling = True

    if single_draw:
        label = tk.Label(result_window, text="000", font=("YEFONTMengChangAnXinKai", 100), fg="#ffde00", bg="#b51112")
        label.place(relx=0.5, rely=0.5, anchor="center")
        rolling_labels.append(label)
    else:
        for i in range(10):
            label = tk.Label(result_window, text="000", font=("YEFONTMengChangAnXinKai", 60), fg="#ffde00", bg="#b51112")
            x = 0.25 + (i % 2) * 0.5
            y = 0.2 + (i // 2) * 0.15
            label.place(relx=x, rely=y, anchor="center")
            rolling_labels.append(label)

    update_rolling_number()
    result_window.bind('<Key>', stop_and_display)
    result_window.focus_set()  # 聚焦到新窗口

# 抽奖函数
def draw_lottery():
    if pool_var.get() == "pool_1":
        available_participants = [p for p in pool_1 if p not in winners_1]
        if available_participants:
            winner = random.choice(available_participants)
            winners_1.append(winner)
            return winner
        else:
            return "无剩余参与者"
    else:
        available_participants = [p for p in pool_2 if p not in winners_2]
        if available_participants:
            winner = random.choice(available_participants)
            winners_2.append(winner)
            return winner
        else:
            return "无剩余参与者"

# 键盘事件处理函数
def switch_pool(event):
    if event.char == '1':  # 按下 '1' 键切换到卡池1
        pool_var.set("pool_1")
        update_background(rolling_bg_path)
    elif event.char == '2':  # 按下 '2' 键切换到卡池2
        pool_var.set("pool_2")
        update_background(rolling_bg_path)
    elif event.char == '9':  # 按下 '9' 键开始单抽
        show_result_window(single_draw=True)
    elif event.char == '0':  # 按下 '0' 键开始十连抽
        show_result_window(single_draw=False)
    elif event.char == ' ':  # 按下空格键退出程序
        exit_program()

# 退出程序
def exit_program():
    root.quit()  # 退出程序

# 默认延迟加载背景
root.after(10, delayed_update_background)  # 延迟100毫秒加载背景图

# 绑定键盘事件：按 '1' 或 '2' 切换卡池
root.bind('<Key>', switch_pool)

# 运行主循环
root.mainloop()
