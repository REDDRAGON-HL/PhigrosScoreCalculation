import tkinter as tk
import threading
from tkinter import Toplevel, scrolledtext, END, font
import pandas as pd
import compute
import sys
import os


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def perror():
    window.after(0, lambda: txt.configure(text="参数有误"))
    window.after(0, lambda: par1.delete(0, END))
    window.after(0, lambda: par2.delete(0, END))
    window.after(0, lambda: par3.delete(0, END))


def fScore():
    """固定分数计算引导"""
    def thread_task():
        try:
            target_score = int(par1.get())
            volume = int(par2.get())
            kadai_mode = kadai_var.get()
            
            if volume == 0 or target_score > 1000000 or target_score < 0:
                perror()
                return
            
            algorithm = optvar2.get()
            
            if kadai_mode:
                window.after(0, lambda: txt.configure(text="课题模式 - 固定分数计算\n计算中"))
                if algorithm == '常规算法':
                    results = compute.fscore_kadai_base(volume, target_score)
                elif algorithm == '剪枝算法':
                    results = compute.fscore_kadai_prune(volume, target_score)
                elif algorithm == '范围剪枝':
                    results = compute.fscore_kadai_range_prune(volume, target_score)
                elif algorithm == '二分剪枝':
                    results = compute.fscore_kadai_binary_prune(volume, target_score)
                elif algorithm == '神秘算法':
                    results = compute.fscore_kadai_math_enum(volume, target_score)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            else:
                window.after(0, lambda: txt.configure(text="固定分数计算\n计算中"))
                if algorithm == '常规算法':
                    results = compute.fscore_base(volume, target_score)
                elif algorithm == '剪枝算法':
                    results = compute.fscore_prune(volume, target_score)
                elif algorithm == '范围剪枝':
                    results = compute.fscore_range_prune(volume, target_score)
                elif algorithm == '二分剪枝':
                    results = compute.fscore_binary_prune(volume, target_score)
                elif algorithm == '神秘算法':
                    results = compute.fscore_range_enum(volume, target_score)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            
            mode_text = "课题模式 - " if kadai_mode else ""
            window.after(0, lambda: txt.configure(text=f"{mode_text}固定分数计算,运行结束\n结果请前往运行窗口查看"))
            
            if checkvar.get() == 1:
                export(results)
                
        except ValueError:
            perror()
    
    threading.Thread(target=thread_task, daemon=True).start()


def fAccuracy():
    """固定acc计算引导"""
    def thread_task():
        try:
            target_acc = float(par1.get())
            volume = int(par2.get())
            kadai_mode = kadai_var.get()
            
            if volume == 0 or target_acc > 100 or target_acc < 0:
                perror()
                return
            
            if kadai_mode:
                window.after(0, lambda: txt.configure(text="课题模式 - 固定acc计算\n计算中"))
                if algorithm == '常规算法':
                    results = compute.faccuracy_kadai_base(volume, target_acc)
                elif algorithm == '剪枝算法':
                    results = compute.faccuracy_kadai_prune(volume, target_acc)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            else:
                algorithm = optvar2.get()
                window.after(0, lambda: txt.configure(text="固定acc计算\n计算中"))
                
                if algorithm == '常规算法':
                    results = compute.faccuracy_base(volume, target_acc)
                elif algorithm == '剪枝算法':
                    results = compute.faccuracy_prune(volume, target_acc)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            
            mode_text = "课题模式 - " if kadai_mode else ""
            window.after(0, lambda: txt.configure(text=f"{mode_text}固定acc计算,运行结束\n结果请前往运行窗口查看"))
            
            if checkvar.get() == 1:
                export(results)
                
        except ValueError:
            perror()
    
    threading.Thread(target=thread_task, daemon=True).start()


def Ranking():
    """rks计算"""
    try:
        difficulty = float(par1.get())
        acc = float(par2.get()) / 100
        
        if difficulty <= 0 or acc < 0 or acc > 1:
            perror()
            return
        
        rks = compute.rounding(difficulty * acc, 4)
        window.after(0, lambda: txt.configure(
            text=f"单曲rks计算,运行结束\n定数{difficulty},acc{par2.get()}%的单曲rks为{rks}"))
            
    except ValueError:
        perror()


def iScore():
    """区间分数计算引导"""
    def thread_task():
        try:
            score_lower = int(par1.get())
            score_upper = int(par2.get())
            volume = int(par3.get())
            kadai_mode = kadai_var.get()
            
            if volume == 0 or score_upper > 1000000 or score_lower < 0 or score_lower > score_upper:
                perror()
                return
            
            if kadai_mode:
                window.after(0, lambda: txt.configure(text="课题模式 - 区间分数计算\n计算中"))
                if algorithm == '常规算法':
                    results = compute.iscore_kadai_base(volume, score_lower, score_upper)
                elif algorithm == '剪枝算法':
                    results = compute.iscore_kadai_prune(volume, score_lower, score_upper)
                elif algorithm == '范围剪枝':
                    results = compute.iscore_kadai_range_prune(volume, score_lower, score_upper)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            else:
                algorithm = optvar2.get()
                window.after(0, lambda: txt.configure(text="区间分数计算\n计算中"))
                
                if algorithm == '常规算法':
                    results = compute.iscore_base(volume, score_lower, score_upper)
                elif algorithm == '剪枝算法':
                    results = compute.iscore_prune(volume, score_lower, score_upper)
                elif algorithm == '范围剪枝':
                    results = compute.iscore_range_prune(volume, score_lower, score_upper)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            
            mode_text = "课题模式 - " if kadai_mode else ""
            window.after(0, lambda: txt.configure(text=f"{mode_text}区间分数计算,运行结束\n结果请前往运行窗口查看"))
            
            if checkvar.get() == 1:
                export(results)
                
        except ValueError:
            perror()
    
    threading.Thread(target=thread_task, daemon=True).start()


def iAccuracy():
    """区间acc计算引导"""
    def thread_task():
        try:
            acc_lower = float(par1.get())
            acc_upper = float(par2.get())
            volume = int(par3.get())
            kadai_mode = kadai_var.get()
            
            if volume == 0 or acc_upper > 100 or acc_lower > acc_upper or acc_lower < 0:
                perror()
                return
            
            if kadai_mode:
                window.after(0, lambda: txt.configure(text="课题模式 - 区间acc计算\n计算中"))
                if algorithm == '常规算法':
                    results = compute.iaccuracy_kadai_base(volume, acc_lower, acc_upper)
                elif algorithm == '剪枝算法':
                    results = compute.iaccuracy_kadai_prune(volume, acc_lower, acc_upper)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            else:
                algorithm = optvar2.get()
                window.after(0, lambda: txt.configure(text="区间acc计算\n计算中"))
                
                if algorithm == '常规算法':
                    results = compute.iaccuracy_base(volume, acc_lower, acc_upper)
                elif algorithm == '剪枝算法':
                    results = compute.iaccuracy_prune(volume, acc_lower, acc_upper)
                else:
                    window.after(0, lambda: txt.configure(text="请选择算法"))
                    return
            
            mode_text = "课题模式 - " if kadai_mode else ""
            window.after(0, lambda: txt.configure(text=f"{mode_text}区间acc计算,运行结束\n结果请前往运行窗口查看"))
            
            if checkvar.get() == 1:
                export(results)
                
        except ValueError:
            perror()
    
    threading.Thread(target=thread_task, daemon=True).start()


def export(results):
    """导出结果到Excel"""
    window.after(0, lambda: txt.configure(text="运行结束，正在导出"))
    print("运行结束，正在导出")
    
    try:
        data = []
        for result in results:
            parts = result.split(',')
            row = {}
            for part in parts:
                key, value = part.split(':')
                try:
                    if '.' in value:
                        row[key] = float(value)
                    else:
                        row[key] = int(value)
                except ValueError:
                    row[key] = value
            data.append(row)
        
        df = pd.DataFrame(data)
        output = 'output.xlsx'
        df.to_excel(output, index=False)
        
        window.after(0, lambda: txt.configure(text=f"结果已导出到 {output}"))
        print(f"结果已导出到 {output}")
        
    except Exception as e:
        window.after(0, lambda: txt.configure(text=f"导出失败: {str(e)}"))
        print(f"导出失败: {str(e)}")


def choose():
    """运行计算"""
    opta = optvar.get()
    
    if opta == '固定分数计算':
        fScore()
    elif opta == '固定acc计算':
        fAccuracy()
    elif opta == '单曲rks计算':
        Ranking()
    elif opta == '区间分数计算':
        iScore()
    elif opta == '区间acc计算':
        iAccuracy()
    else:
        window.after(0, lambda: txt.configure(text="请选择计算选项"))


def update_algorithm_menu(n):
    """更新算法选择菜单"""
    opt2['menu'].delete(0, 'end')
    for op in algorithmli[n]:
        opt2['menu'].add_command(label=op, command=lambda x=op: optvar2.set(x))


def update_text(a=None, b=None, c=None):
    """更新提示文本"""
    opta = optvar.get()
    
    if opta == '固定分数计算':
        text.configure(text="参数1输入目标分数，参数2输入物量")
        update_algorithm_menu(0)
    elif opta == '固定acc计算':
        text.configure(text="参数1输入目标acc，参数2输入物量")
        update_algorithm_menu(1)
    elif opta == '单曲rks计算':
        text.configure(text="参数1输入定数，参数2输入acc")
        opt2['menu'].delete(0, 'end')
        opt2['menu'].add_command(label='常规算法', command=lambda: optvar2.set('常规算法'))
        optvar2.set('常规算法')
    elif opta == '区间acc计算':
        text.configure(text="参数1输入acc下限，参数2输入acc上限\n参数3输入物量")
        update_algorithm_menu(2)
    elif opta == '区间分数计算':
        text.configure(text="参数1输入分数下限，参数2输入分数上限\n参数3输入物量")
        update_algorithm_menu(3)


def show():
    """初始化选项显示"""
    optvar.trace("w", update_text)
    update_text()


def menuSupport():
    """菜单栏更新与支持"""
    tip = Toplevel(window)
    tip.title("更新与支持")
    tip.geometry('300x200')
    tip.attributes('-alpha', 0.9)
    tip.config(background="#cccccc")
    tip.resizable(0, 0)
    
    try:
        tip.iconbitmap(get_resource_path("favicon.ico"))
    except:
        pass
    
    text_area = scrolledtext.ScrolledText(
        tip, wrap="char", width=40, height=15, background="#cccccc"
    )
    text_area.grid(row=0, column=0, padx=10, pady=10)
    tip.grid_rowconfigure(0, weight=1)
    tip.grid_columnconfigure(0, weight=1)
    
    placeholders = "<TITLE>"
    style = ("Helvetica", 10, "bold", "blue")
    replacement_titles = ["更新日志", "更新计划","算法说明", "支持"]
    
    text_content = f"""
              {placeholders}
         | 新增算法
26.05.13 | 实现课题模式
         | 完成区间分数计算
         | 算法重构，大幅优化计算速度

24.12.04 | 增加acc计算、区间acc计算

24.11.05 | 添加ico，更新GUI整体框架

         | 优化GUI，增加菜单栏支持选
24.10.27 | 项卡、增加导出结果为Excel
         | 表格

24.10.20 | 重写算法，重写GUI

              {placeholders}
算法：输入红黄数进行更精确计算
GUI：优化参数输入提示
其他：编写网页版

              {placeholders}
1. 常规算法
   暴力穷举，遍历所有可能的组合
   实现简单，效果稳定
   速度最慢

2. 剪枝算法
   通过公式直接计算所需连击数
   结合连击分范围进行剪枝
   速度较快

2. 范围剪枝
   在剪枝算法基础上，提前计算每个P的
   有效分数范围，大幅跳过不可能的组合
   速度很快

3. 二分剪枝
   对G值进行二分查找定位候选点
   在候选点附近搜索验证
   速度很快，结果太多时可能有部分遗漏

3. 神秘算法（范围枚举）
   利用公式反推 P 和 G 的可能范围
   大幅缩小搜索空间后枚举
   速度最快，但可能不太稳定

                {placeholders}
感谢使用！！！

这么屎的代码也要支持吗
欢迎反馈问题！
Github:REDDRAGON-HL

        """
    
    text_area.insert("1.0", text_content)
    
    font_style = tk.font.Font(family=style[0], size=style[1], weight=style[2])
    text_area.tag_config("title_tag", font=font_style, foreground=style[3])
    
    start_index = "1.0"
    for title in replacement_titles:
        start_index = text_area.search(placeholders, start_index, tk.END)
        if not start_index:
            break
        
        end_index = f"{start_index} + {len(placeholders)}c"
        centered_title = f" {title} "
        text_area.delete(start_index, end_index)
        text_area.insert(start_index, centered_title + "\n")
        text_area.tag_add("title_tag", start_index, f"{start_index} + {len(centered_title) - 1}c")
        start_index = f"{end_index} linestart + 1c"


def fixedCalculations():
    """菜单栏固定计算"""
    opt['menu'].delete(0, 'end')
    for op in calculationli[0]:
        opt['menu'].add_command(label=op, command=lambda x=op: optvar.set(x))
    
    optvar.set("选择计算选项")
    par3.place_forget()
    opt.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.1)
    opt2.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.1)


def intervalCalculation():
    """菜单栏区间计算"""
    opt['menu'].delete(0, 'end')
    for op in calculationli[1]:
        opt['menu'].add_command(label=op, command=lambda x=op: optvar.set(x))
    
    optvar.set("选择计算选项")
    par3.place(relx=0.1, rely=0.32, relwidth=0.3, relheight=0.1)
    opt.place(relx=0.1, rely=0.46, relwidth=0.4, relheight=0.1)
    opt2.place(relx=0.6, rely=0.46, relwidth=0.3, relheight=0.1)


window = tk.Tk()
window.title("ScoreCalculation")
window.geometry('300x300')
window.config(background="#cccccc")
window.resizable(0, 0)
window.attributes('-alpha', 0.9)

try:
    window.iconbitmap(get_resource_path("favicon.ico"))
except:
    pass

menu = tk.Menu(window)
menu.add_command(label="更新与支持", command=menuSupport)
menu.add_radiobutton(label="固定计算", command=fixedCalculations)
menu.add_radiobutton(label="区间计算", command=intervalCalculation)

text = tk.Label(window, text="选择计算方式", bg="#cccccc")
text.place(relx=0, rely=0.035, relwidth=1, relheight=0.1)

par1 = tk.Entry(window)
par1.place(relx=0.1, rely=0.17, relwidth=0.3, relheight=0.1)

par2 = tk.Entry(window)
par2.place(relx=0.6, rely=0.17, relwidth=0.3, relheight=0.1)

par3 = tk.Entry(window)
par3.place_forget()

calculationli = [
    ['固定分数计算', '固定acc计算', '单曲rks计算'],
    ['区间分数计算', '区间acc计算']
]

optvar = tk.StringVar()
optvar.set("选择计算选项")
opt = tk.OptionMenu(window, optvar, '请在菜单栏选择选项')
opt.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.1)

algorithmli = [
    ['常规算法', '剪枝算法', '范围剪枝', '二分剪枝', '神秘算法'],
    ['常规算法', '剪枝算法'],
    ['常规算法', '剪枝算法'],
    ['常规算法', '剪枝算法', '范围剪枝']
]

optvar2 = tk.StringVar()
optvar2.set("选择算法")
opt2 = tk.OptionMenu(window, optvar2, '请选择计算选项')
opt2.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.1)

checkvar = tk.IntVar()
check = tk.Checkbutton(
    window, text="导出结果", variable=checkvar, 
    onvalue=1, offvalue=0, bg="#cccccc"
)
check.place(relx=0.15, rely=0.58, relwidth=0.22, relheight=0.08)

kadai_var = tk.IntVar()
kadai_check = tk.Checkbutton(
    window, text="课题模式", variable=kadai_var,
    onvalue=1, offvalue=0, bg="#cccccc"
)
kadai_check.place(relx=0.55, rely=0.58, relwidth=0.22, relheight=0.08)

btn = tk.Button(window, text='运行', command=choose)
btn.place(relx=0.35, rely=0.68, relwidth=0.3, relheight=0.1)

txt = tk.Label(window, text="等待运行", bg="#cccccc")
txt.place(rely=0.83, relwidth=1)

show()
window.config(menu=menu)
window.mainloop()