import json


class UserProfile:

  def __init__(self, weight, body_fat_pct, muscle_mass, tdee):
    self.weight = weight  # 體重 (kg)
    self.body_fat_pct = body_fat_pct  # 體脂率 (%)
    self.muscle_mass = muscle_mass  # 肌肉量 (kg)
    self.tdee = tdee  # 每日總熱量消耗 (kcal)

    # 衍生計算
    self.fat_mass = self.weight * (self.body_fat_pct / 100)
    self.other_mass = (
        self.weight - self.muscle_mass - self.fat_mass
    )  # 骨骼以外其他組織


class FitnessSimulator:

  def __init__(self, user: UserProfile, daily_calorie_intake=2000):
    self.user = user
    self.calorie_intake = daily_calorie_intake  # 假設每日攝取熱量

  def run_simulation(self, menu_schedule, days=30):
    """模擬執行菜單達指定的日數"""
    print(f"--- 開始模擬 ({days} 天計畫) ---")
    print(
        f"初始狀態 -> 體重: {self.user.weight:.2f} kg | 體脂率:"
        f" {self.user.body_fat_pct:.1f}% | 肌肉量:"
        f" {self.user.muscle_mass:.2f} kg\n"
    )

    # 記錄每日變化軌跡
    history = []

    for day in range(1, days + 1):
      # 取得當天菜單（若菜單天數小於總天數則循環使用）
      day_menu = menu_schedule[(day - 1) % len(menu_schedule)]

      # 1. 計算當日運動消耗的熱量
      workout_calories = day_menu.get("calories_burned", 0)

      # 2. 計算總消耗與熱量赤字/盈餘
      total_expenditure = self.user.tdee + workout_calories
      calorie_balance = self.calorie_intake - total_expenditure  # 負值代表赤字

      # 3. 身體組成變化邏輯 (簡化版科學模型)
      # 7700 kcal 約等於 1kg 的脂肪熱量
      fat_change = calorie_balance / 7700.0

      # 肌肉合成邏輯：若當天有力量訓練且熱量充足或輕微赤字，肌肉微幅成長
      muscle_change = 0.0
      if day_menu.get("type") == "strength":
        if calorie_balance >= -300:  # 熱量沒有極端匱乏
          muscle_change = 0.03  # 假設每日穩定微幅增肌

      # 總體重變化 = 脂肪變化 + 肌肉變化 (其餘水分雜質隨之調整)
      weight_change = fat_change + muscle_change

      # 更新用戶當前身體數據
      self.user.weight += weight_change
      self.user.fat_mass = max(
          1.0, self.user.fat_mass + fat_change * 0.75
      )  # 假設75%減脂來自脂肪
      self.user.muscle_mass += muscle_change
      self.user.body_fat_pct = (self.user.fat_mass / self.user.weight) * 100

      # 隨體重微調 TDEE (體重變輕，基礎代謝微幅下降)
      self.user.tdee = 2000 + (self.user.weight - 70) * 15

    print(f"--- 模擬結束 ({days} 天後) ---")
    print(
        f"最終狀態 -> 體重: {self.user.weight:.2f} kg (變動:"
        f" {self.user.weight - user_initial_weight:+.2f} kg)"
    )
    print(
        f"體脂率: {self.user.body_fat_pct:.1f}% (變動:"
        f" {self.user.body_fat_pct - user_initial_fat_pct:+.1f}%)"
    )
    print(
        f"肌肉量: {self.user.muscle_mass:.2f} kg (變動:"
        f" {self.user.muscle_mass - user_initial_muscle:+.2f} kg)"
    )

    return {
        "final_weight": round(self.user.weight, 2),
        "final_body_fat": round(self.user.body_fat_pct, 1),
        "final_muscle": round(self.user.muscle_mass, 2),
    }


# ==================== 範例執行 ====================
if __name__ == "__main__":
  # 1. 設定測試者初始數據 (例如：身高175cm, 體重75kg, 體脂20%)
  user_initial_weight = 75.0
  user_initial_fat_pct = 20.0
  user_initial_muscle = 33.0
  initial_tdee = 2200

  test_user = UserProfile(
      weight=user_initial_weight,
      body_fat_pct=user_initial_fat_pct,
      muscle_mass=user_initial_muscle,
      tdee=initial_tdee,
  )

  # 2. 定義運動菜單 (可循環的週菜單)
  # 包含力量訓練 (strength) 與 有氧訓練 (cardio)
  sample_menu_schedule = [
      {
          "day": 1,
          "name": "全身重量訓練",
          "type": "strength",
          "calories_burned": 350,
      },
      {"day": 2, "name": "高強度有氧", "type": "cardio", "calories_burned": 500},
      {"day": 3, "name": "休息日", "type": "rest", "calories_burned": 0},
      {
          "day": 4,
          "name": "核心與上肢訓練",
          "type": "strength",
          "calories_burned": 300,
      },
      {"day": 5, "name": "慢跑有氧", "type": "cardio", "calories_burned": 450},
      {"day": 6, "name": "下肢肌力訓練", "type": "strength", "calories_burned": 400},
      {"day": 7, "name": "完全休息", "type": "rest", "calories_burned": 0},
  ]

  # 3. 建立模擬器並執行 30 天
  # 假設每日攝取熱量固定為 2300 kcal
  simulator = FitnessSimulator(user=test_user, daily_calorie_intake=2300)
  result = simulator.run_simulation(sample_menu_schedule, days=30)
