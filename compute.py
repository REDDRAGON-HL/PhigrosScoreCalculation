"""
打击获得perfect判定时获得100 % 的分数，
获得good判定时获得65 % 的分数，
获得miss时无分数，

上述判定分数满分为900000，计算方式为：
（perfect数 + good数0.65） / 谱面物量 * 900000（谱面物量是指该谱面获得全连时的连击数）；

另外有100000为连击得分，计算方式为：
最大连击数 / 谱面物量 * 100000；

总分为判定分数 + 连击得分，四舍五入取整。

课题模式：不计连击分，满分1000000
判定分数 = （perfect数 + good数0.65） / 谱面物量 * 1000000
"""
from typing import List


def rounding(num: float, n: int = 0) -> float:
    """
    优化Python内置的round()
    解决Python四舍六入的问题，实现真正的四舍五入
    
    参数:
        num: 需要四舍五入的数字
        n: 保留的小数位数，默认取整
    """
    if n == 0:
        return round(num + 1e-10)
    return round(num + 1e-10, n)


def btf(p: int, g: int, wl: int) -> float:
    """基础分数"""
    return (p + g * 0.65) / wl * 900000


def cp(ljs: int, wl: int) -> float:
    """连击分数"""
    return ljs / wl * 100000



def fscore_base(volume: int, target: int) -> List[str]:
    """
    暴力穷举
    遍历所有可能的P、G、LJS组合
    
    参数:
        volume: 谱面物量
        target: 目标分数
    """
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"P:{volume},G:0,M:0,最大连击:{volume},acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    for p in range(volume + 1):
        max_g = volume - p

        for g in range(max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)

            min_ljs = volume // (m + 1) if m > 0 else volume
            max_ljs = p + g

            for ljs in range(min_ljs, max_ljs + 1):
                total_score = rounding(btf_score + cp(ljs, volume))
                if total_score == target:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    print(f"P:{p},G:{g},M:{m},最大连击:{ljs},acc:{acc}")
                    results.append(f"P:{p},G:{g},M:{m},最大连击:{ljs},acc:{acc}")

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_prune(volume: int, target: int) -> List[str]:
    """
    剪枝算法
    通过数学公式直接计算所需连击数，避免不必要的枚举
    
    参数:
        volume: 谱面物量
        target: 目标分数
    """
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"P:{volume},G:0,M:0,最大连击:{volume},acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    # 连击分的可能范围
    cp_min = 0
    cp_max = 100000

    # 遍历所有可能的Perfect数
    for p in range(volume + 1):
        max_g = volume - p  # 该P下的最大Good数

        # 遍历所有可能的Good数
        for g in range(max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)

            # 计算所需连击分
            cp_needed = target - btf_score

            # 剪枝：所需连击分不在有效范围，跳过
            if cp_needed < cp_min or cp_needed > cp_max:
                continue

            # 反向计算所需的最大连击数
            ljs_float = cp_needed / 100000 * volume
            ljs_target = int(round(ljs_float))

            # 计算该P、G、M组合下可能的最大连击数范围
            min_ljs = volume // (m + 1) if m > 0 else volume
            max_ljs = p + g

            # 验证所需连击数在可行范围内
            if min_ljs <= ljs_target <= max_ljs:
                total_score = rounding(btf_score + cp(ljs_target, volume))
                if total_score == target:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    result = f"P:{p},G:{g},M:{m},最大连击:{ljs_target},acc:{acc}"
                    print(result)
                    results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_range_prune(volume: int, target: int) -> List[str]:
    """
    范围剪枝算法
    在剪枝算法基础上，提前计算每个P的有效分数范围
    大幅跳过不可能的组合
    
    参数:
        volume: 谱面物量
        target: 目标分数
    """
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"P:{volume},G:0,M:0,最大连击:{volume},acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    for p in range(volume + 1):
        max_g = volume - p

        min_btf = btf(p, 0, volume)
        max_btf = btf(p, max_g, volume)

        if target - 100000 > max_btf or target < min_btf:
            continue

        for g in range(max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)

            cp_needed = target - btf_score

            if 0 <= cp_needed <= 100000:
                ljs_float = cp_needed / 100000 * volume
                ljs_target = int(round(ljs_float))

                min_ljs = volume // (m + 1) if m > 0 else volume
                max_ljs = p + g

                if min_ljs <= ljs_target <= max_ljs:
                    total_score = rounding(btf_score + cp(ljs_target, volume))
                    if total_score == target:
                        acc = rounding((p + g * 0.65) / volume, 4)
                        result = f"P:{p},G:{g},M:{m},最大连击:{ljs_target},acc:{acc}"
                        print(result)
                        results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_range_enum(volume: int, target: int) -> List[str]:
    """
    神秘算法，范围枚举

    利用数学公式反推可能的P和G值范围，大幅缩小搜索空间
    
    参数:
        volume: 谱面物量
        target: 目标分数
    """
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"P:{volume},G:0,M:0,最大连击:{volume},acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    # 先用数学公式缩小P的范围
    for p in range(volume + 1):
        max_g = volume - p

        # 计算G的可能范围
        min_g_calc = ((target - 100000) * volume / 900000 - p) / 0.65
        max_g_calc = (target * volume / 900000 - p) / 0.65

        # 添加缓冲防止边界情况遗漏
        search_min_g = max(0, int(min_g_calc) - 5)
        search_max_g = min(max_g, int(max_g_calc) + 5)

        # 只在计算出的小范围内枚举G
        for g in range(search_min_g, search_max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)

            # 计算需要的连击分
            cp_needed = target - btf_score

            # 剪枝，连击分不在有效范围则跳过
            if cp_needed < 0 or cp_needed > 100000:
                continue

            # 计算所需的最大连击数
            ljs_float = cp_needed / 100000 * volume
            ljs_target = int(round(ljs_float))

            # 验证连击数是否在物理可能范围内
            min_ljs = volume // (m + 1) if m > 0 else volume
            max_ljs = p + g

            if min_ljs <= ljs_target <= max_ljs:
                total_score = rounding(btf_score + cp(ljs_target, volume))
                if total_score == target:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    result = f"P:{p},G:{g},M:{m},最大连击:{ljs_target},acc:{acc}"
                    print(result)
                    results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_binary_prune(volume: int, target: int) -> List[str]:
    """
    二分剪枝算法

    对每个P，在G上进行二分查找定位候选点，再在附近搜索验证
    
    参数:
        volume: 谱面物量
        target: 目标分数
    """
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"P:{volume},G:0,M:0,最大连击:{volume},acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    min_p = max(0, int((target - 100000) * volume / 900000 - 0.65 * volume) - 2)
    max_p = min(volume, int(target * volume / 900000) + 2)

    for p in range(min_p, max_p + 1):
        max_g = volume - p
        low, high = 0, max_g

        # 先计算该P下可能的分数范围，快速跳过
        min_score = btf(p, 0, volume)
        max_score = btf(p, max_g, volume) + 100000

        if target < min_score - 0.5 or target > max_score + 0.5:
            continue

        # 二分查找一个候选点
        found_g = None
        while low <= high:
            mid_g = (low + high) // 2
            m = volume - p - mid_g

            # 计算判定分
            btf_score = btf(p, mid_g, volume)

            # 找到可能让分数达到target的连击分
            cp_needed = target - btf_score

            if cp_needed < 0:
                high = mid_g - 1
            elif cp_needed > 100000:
                low = mid_g + 1
            else:
                # 验证这个G值
                ljs_float = cp_needed / 100000 * volume
                ljs_target = int(round(ljs_float))
                min_ljs = volume // (m + 1) if m > 0 else volume
                max_ljs = p + mid_g

                if min_ljs <= ljs_target <= max_ljs:
                    total_score = rounding(btf_score + cp(ljs_target, volume))
                    if total_score == target:
                        found_g = mid_g
                        break
                # 即使不是精确解，也继续搜索
                if btf_score + 100000 < target:
                    low = mid_g + 1
                else:
                    high = mid_g - 1

        # 如果找到了候选点，在附近搜索（因为函数不单调）
        if found_g is not None:
            search_radius = 3
            for g in range(max(0, found_g - search_radius), min(max_g, found_g + search_radius) + 1):
                m = volume - p - g
                btf_score = btf(p, g, volume)
                cp_needed = target - btf_score

                if 0 <= cp_needed <= 100000:
                    ljs_float = cp_needed / 100000 * volume
                    ljs_target = int(round(ljs_float))
                    min_ljs = volume // (m + 1) if m > 0 else volume
                    max_ljs = p + g

                    if min_ljs <= ljs_target <= max_ljs:
                        total_score = rounding(btf_score + cp(ljs_target, volume))
                        if total_score == target:
                            acc = rounding((p + g * 0.65) / volume, 4)
                            result = f"P:{p},G:{g},M:{m},最大连击:{ljs_target},acc:{acc}"
                            if result not in results:
                                print(result)
                                results.append(result)
        else:
            # 如果没找到，用数学公式计算范围后枚举
            min_g_calc = ((target - 100000) * volume / 900000 - p) / 0.65
            max_g_calc = (target * volume / 900000 - p) / 0.65
            search_min_g = max(0, int(min_g_calc) - 3)
            search_max_g = min(max_g, int(max_g_calc) + 3)

            for g in range(search_min_g, search_max_g + 1):
                m = volume - p - g
                btf_score = btf(p, g, volume)
                cp_needed = target - btf_score

                if 0 <= cp_needed <= 100000:
                    ljs_float = cp_needed / 100000 * volume
                    ljs_target = int(round(ljs_float))
                    min_ljs = volume // (m + 1) if m > 0 else volume
                    max_ljs = p + g

                    if min_ljs <= ljs_target <= max_ljs:
                        total_score = rounding(btf_score + cp(ljs_target, volume))
                        if total_score == target:
                            acc = rounding((p + g * 0.65) / volume, 4)
                            result = f"P:{p},G:{g},M:{m},最大连击:{ljs_target},acc:{acc}"
                            if result not in results:
                                print(result)
                                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results



def faccuracy_base(volume: int, acc: float) -> List[str]:
    """
    暴力穷举
    
    参数:
        volume: 谱面物量
        acc: 目标acc
    """
    results = []
    target_acc = acc / 100

    for p in range(volume + 1):
        for g in range(volume - p + 1):
            m = volume - p - g
            now_acc = rounding((p + g * 0.65) / volume, 4)
            if now_acc == target_acc:
                print(f"P:{p},G:{g},M:{m}")
                results.append(f"P:{p},G:{g},M:{m}")

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def faccuracy_prune(volume: int, acc: float) -> List[str]:
    """
    剪枝算法
    通过数学公式直接计算可能的P、G组合
    
    参数:
        volume: 谱面物量
        acc: 目标ACC（百分比）
    """
    results = []
    target_acc = acc / 100

    def process_p(p_val, noc, result_list):
        for g in range(volume - p_val + 1):
            m = volume - p_val - g
            now_acc = rounding((p_val + g * 0.65) / volume, 4)
            if now_acc == target_acc:
                noc += 1
                print(f"P:{p_val},G:{g},M:{m}")
                result_list.append(f"P:{p_val},G:{g},M:{m}")
        return noc, result_list

    count = 0
    try:
        if target_acc < 0.5:
            for p in range(volume + 1):
                count, results = process_p(p, count, results)
        else:
            for i in range(volume + 1):
                p = volume - i
                count, results = process_p(p, count, results)
    except KeyboardInterrupt:
        print("\n运行终止，返回现有结果")

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results



def iaccuracy_base(volume: int, acc1: float, acc2: float) -> List[str]:
    """
    暴力穷举
    
    参数:
        volume: 谱面物量
        acc1: ACC下限
        acc2: ACC上限
    """
    results = []
    acc10 = acc1 / 100
    acc20 = acc2 / 100

    for p in range(volume + 1):
        for g in range(volume - p + 1):
            m = volume - p - g
            now_acc = rounding((p + g * 0.65) / volume, 4)

            if acc10 <= now_acc <= acc20:
                show_acc = rounding(now_acc * 100, 4)
                result = f"P:{p},G:{g},M:{m},acc:{show_acc}%"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def iaccuracy_prune(volume: int, acc1: float, acc2: float) -> List[str]:
    """
    剪枝算法
    通过数学公式缩小P的遍历范围
    
    参数:
        volume: 谱面物量
        acc1: ACC下限
        acc2: ACC上限
    """
    results = []
    acc10 = acc1 / 100
    acc20 = acc2 / 100

    min_p = max(0, int(acc10 * volume - 0.65 * volume) - 2)
    max_p = min(volume, int(acc20 * volume + 1) + 2)

    for p in range(min_p, max_p + 1):
        for g in range(volume - p + 1):
            m = volume - p - g
            now_acc = rounding((p + g * 0.65) / volume, 4)

            if acc10 <= now_acc <= acc20:
                show_acc = rounding(now_acc * 100, 4)
                result = f"P:{p},G:{g},M:{m},acc:{show_acc}%"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results



def iscore_base(volume: int, score1: int, score2: int) -> List[str]:
    """
    暴力穷举
    
    参数:
        volume: 谱面物量
        score1: 分数下限
        score2: 分数上限
    """
    results = []

    if score1 > score2:
        score1, score2 = score2, score1

    for p in range(volume + 1):
        max_g = volume - p

        for g in range(max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)

            min_ljs = volume // (m + 1) if m > 0 else volume
            max_ljs = p + g

            for ljs in range(min_ljs, max_ljs + 1):
                total_score = rounding(btf_score + cp(ljs, volume))

                if score1 <= total_score <= score2:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    result = f"P:{p},G:{g},M:{m},最大连击:{ljs},acc:{acc},分数:{total_score}"
                    print(result)
                    results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def iscore_prune(volume: int, score1: int, score2: int) -> List[str]:
    """
    剪枝算法
    通过数学公式缩小遍历范围
    
    参数:
        volume: 谱面物量
        score1: 分数下限
        score2: 分数上限
    """
    results = []

    if score1 > score2:
        score1, score2 = score2, score1

    for p in range(volume + 1):
        max_g = volume - p

        for g in range(max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)

            min_cp_needed = score1 - btf_score
            max_cp_needed = score2 - btf_score

            if max_cp_needed < 0 or min_cp_needed > 100000:
                continue

            actual_min_cp = max(0, min_cp_needed)
            actual_max_cp = min(100000, max_cp_needed)

            min_ljs_float = actual_min_cp / 100000 * volume
            max_ljs_float = actual_max_cp / 100000 * volume

            min_ljs = max(volume // (m + 1) if m > 0 else volume, int(round(min_ljs_float - 1)))
            max_ljs = min(p + g, int(round(max_ljs_float + 1)))

            min_ljs = max(min_ljs, 0)
            max_ljs = min(max_ljs, volume)

            for ljs in range(min_ljs, max_ljs + 1):
                total_score = rounding(btf_score + cp(ljs, volume))

                if score1 <= total_score <= score2:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    result = f"P:{p},G:{g},M:{m},最大连击:{ljs},acc:{acc},分数:{total_score}"
                    print(result)
                    results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def iscore_range_prune(volume: int, score1: int, score2: int) -> List[str]:
    """
    范围剪枝算法
    在剪枝算法基础上，提前计算每个P的有效分数范围
    
    参数:
        volume: 谱面物量
        score1: 分数下限
        score2: 分数上限
    """
    results = []

    if score1 > score2:
        score1, score2 = score2, score1

    for p in range(volume + 1):
        max_g = volume - p

        min_btf = btf(p, 0, volume)
        max_btf = btf(p, max_g, volume)

        if max_btf + 100000 < score1 or min_btf > score2:
            continue

        for g in range(max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)

            min_cp_needed = score1 - btf_score
            max_cp_needed = score2 - btf_score

            if max_cp_needed < 0 or min_cp_needed > 100000:
                continue

            actual_min_cp = max(0, min_cp_needed)
            actual_max_cp = min(100000, max_cp_needed)

            min_ljs_float = actual_min_cp / 100000 * volume
            max_ljs_float = actual_max_cp / 100000 * volume

            min_ljs = max(volume // (m + 1) if m > 0 else volume, int(round(min_ljs_float - 1)))
            max_ljs = min(p + g, int(round(max_ljs_float + 1)))

            min_ljs = max(min_ljs, 0)
            max_ljs = min(max_ljs, volume)

            for ljs in range(min_ljs, max_ljs + 1):
                total_score = rounding(btf_score + cp(ljs, volume))

                if score1 <= total_score <= score2:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    result = f"P:{p},G:{g},M:{m},最大连击:{ljs},acc:{acc},分数:{total_score}"
                    print(result)
                    results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results



def btf_kadai(p: int, g: int, wl: int) -> float:
    """课题判定分"""
    return (p + g * 0.65) / wl * 1000000


def fscore_kadai_base(volume: int, target: int) -> List[str]:
    """课题固定分数计算
    暴力穷举"""
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"课题模式 - P:{volume},G:0,M:0,acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    for p in range(volume + 1):
        for g in range(volume - p + 1):
            m = volume - p - g
            total_score = rounding(btf_kadai(p, g, volume))

            if total_score == target:
                acc = rounding((p + g * 0.65) / volume, 4)
                result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc}"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_kadai_prune(volume: int, target: int) -> List[str]:
    """课题固定分数计算
    剪枝算法"""
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"课题模式 - P:{volume},G:0,M:0,acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    for p in range(volume + 1):
        max_g = volume - p

        # 计算该P下的分数范围
        min_score = btf_kadai(p, 0, volume)
        max_score = btf_kadai(p, max_g, volume)

        # 剪枝
        if target < min_score - 0.5 or target > max_score + 0.5:
            continue

        for g in range(max_g + 1):
            m = volume - p - g
            total_score = rounding(btf_kadai(p, g, volume))

            if total_score == target:
                acc = rounding((p + g * 0.65) / volume, 4)
                result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc}"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_kadai_range_prune(volume: int, target: int) -> List[str]:
    """课题固定分数计算
    范围剪枝算法"""
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"课题模式 - P:{volume},G:0,M:0,acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    min_p = max(0, int(target * volume / 1000000 - 0.65 * volume) - 2)
    max_p = min(volume, int(target * volume / 1000000) + 2)

    for p in range(min_p, max_p + 1):
        max_g = volume - p

        min_score = btf_kadai(p, 0, volume)
        max_score = btf_kadai(p, max_g, volume)

        if target < min_score - 0.5 or target > max_score + 0.5:
            continue

        for g in range(max_g + 1):
            m = volume - p - g
            total_score = rounding(btf_kadai(p, g, volume))

            if total_score == target:
                acc = rounding((p + g * 0.65) / volume, 4)
                result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc}"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_kadai_math_enum(volume: int, target: int) -> List[str]:
    """课题固定分数计算
    范围枚举
    
    参数:
        volume: 谱面物量
        target: 目标分数
    """
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"课题模式 - P:{volume},G:0,M:0,acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    min_p = max(0, int(target * volume / 1000000 - 0.65 * volume) - 2)
    max_p = min(volume, int(target * volume / 1000000) + 2)

    for p in range(min_p, max_p + 1):
        max_g = volume - p

        g_calc = (target * volume / 1000000 - p) / 0.65
        search_min_g = max(0, int(g_calc) - 2)
        search_max_g = min(max_g, int(g_calc) + 2)

        for g in range(search_min_g, search_max_g + 1):
            m = volume - p - g
            total_score = rounding(btf_kadai(p, g, volume))

            if total_score == target:
                acc = rounding((p + g * 0.65) / volume, 4)
                result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc}"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def fscore_kadai_binary_prune(volume: int, target: int) -> List[str]:
    """课题固定分数计算 - 二分剪枝算法

    参数:
        volume: 谱面物量
        target: 目标分数
    """
    results = []

    if target == 1000000:
        acc = 1.0
        result = f"课题模式 - P:{volume},G:0,M:0,acc:{acc}"
        print(result)
        results.append(result)
        print("-" * 50)
        print(f"{len(results)}种情况")
        print(results)
        return results

    min_p = max(0, int(target * volume / 1000000 - 0.65 * volume) - 2)
    max_p = min(volume, int(target * volume / 1000000) + 2)

    for p in range(min_p, max_p + 1):
        max_g = volume - p

        min_score = btf_kadai(p, 0, volume)
        max_score = btf_kadai(p, max_g, volume)

        if target < min_score - 0.5 or target > max_score + 0.5:
            continue

        found_g = None
        low, high = 0, max_g
        while low <= high:
            mid_g = (low + high) // 2
            m = volume - p - mid_g
            btf_score = btf_kadai(p, mid_g, volume)

            if abs(btf_score - target) < 0.5:
                found_g = mid_g
                break
            elif btf_score < target:
                low = mid_g + 1
            else:
                high = mid_g - 1

        if found_g is not None:
            search_radius = 3
            for g in range(max(0, found_g - search_radius), min(max_g, found_g + search_radius) + 1):
                m = volume - p - g
                total_score = rounding(btf_kadai(p, g, volume))
                if abs(total_score - target) < 0.5:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc}"
                    if result not in results:
                        print(result)
                        results.append(result)
        else:
            min_g_calc = (target * volume / 1000000 - p) / 0.65
            search_min_g = max(0, int(min_g_calc) - 3)
            search_max_g = min(max_g, int(min_g_calc) + 3)

            for g in range(search_min_g, search_max_g + 1):
                m = volume - p - g
                total_score = rounding(btf_kadai(p, g, volume))
                if abs(total_score - target) < 0.5:
                    acc = rounding((p + g * 0.65) / volume, 4)
                    result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc}"
                    if result not in results:
                        print(result)
                        results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results



def iscore_kadai_base(volume: int, score1: int, score2: int) -> List[str]:
    """课题区间分数计算
    暴力穷举"""
    results = []

    if score1 > score2:
        score1, score2 = score2, score1

    for p in range(volume + 1):
        for g in range(volume - p + 1):
            m = volume - p - g
            total_score = rounding(btf_kadai(p, g, volume))

            if score1 <= total_score <= score2:
                acc = rounding((p + g * 0.65) / volume, 4)
                result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc},分数:{total_score}"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def iscore_kadai_prune(volume: int, score1: int, score2: int) -> List[str]:
    """课题区间分数计算
    剪枝算法"""
    results = []

    if score1 > score2:
        score1, score2 = score2, score1

    for p in range(volume + 1):
        max_g = volume - p

        # 计算该P下的分数范围
        min_score = btf_kadai(p, 0, volume)
        max_score = btf_kadai(p, max_g, volume)

        # 剪枝
        if max_score < score1 - 0.5 or min_score > score2 + 0.5:
            continue

        for g in range(max_g + 1):
            m = volume - p - g
            total_score = rounding(btf_kadai(p, g, volume))

            if score1 <= total_score <= score2:
                acc = rounding((p + g * 0.65) / volume, 4)
                result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc},分数:{total_score}"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results


def iscore_kadai_range_prune(volume: int, score1: int, score2: int) -> List[str]:
    """课题区间分数计算
    范围剪枝算法"""
    results = []

    if score1 > score2:
        score1, score2 = score2, score1

    min_p = max(0, int(score1 * volume / 1000000 - 0.65 * volume) - 2)
    max_p = min(volume, int(score2 * volume / 1000000) + 2)

    for p in range(min_p, max_p + 1):
        max_g = volume - p

        min_score = btf_kadai(p, 0, volume)
        max_score = btf_kadai(p, max_g, volume)

        if max_score < score1 - 0.5 or min_score > score2 + 0.5:
            continue

        for g in range(max_g + 1):
            m = volume - p - g
            total_score = rounding(btf_kadai(p, g, volume))

            if score1 <= total_score <= score2:
                acc = rounding((p + g * 0.65) / volume, 4)
                result = f"课题模式 - P:{p},G:{g},M:{m},acc:{acc},分数:{total_score}"
                print(result)
                results.append(result)

    print("-" * 50)
    print(f"{len(results)}种情况")
    print(results)
    return results



def faccuracy_kadai_base(volume: int, acc: float) -> List[str]:
    return faccuracy_base(volume, acc)


def faccuracy_kadai_prune(volume: int, acc: float) -> List[str]:
    return faccuracy_prune(volume, acc)


def iaccuracy_kadai_base(volume: int, acc1: float, acc2: float) -> List[str]:
    return iaccuracy_base(volume, acc1, acc2)


def iaccuracy_kadai_prune(volume: int, acc1: float, acc2: float) -> List[str]:
    return iaccuracy_prune(volume, acc1, acc2)
