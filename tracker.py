import csv
import os
import matplotlib.pyplot as plt


def calculate_bmi(weight, height):
  """Calculates BMI and returns BMI value and category."""
  if height <= 0 or weight <= 0:
    raise ValueError("Weight and height must be positive numbers.")
  bmi = weight / (height**2)
  if bmi < 18.5:
    category = "Underweight"
  elif 18.5 <= bmi <= 24.9:
    category = "Normal"
  elif 25.0 <= bmi <= 29.9:
    category = "Overweight"
  else:
    category = "Obese"
  return round(bmi, 2), category


def calculate_average_steps(steps_list):
  if not steps_list:
    return 0.0
  return sum(steps_list) / len(steps_list)


def calculate_total_calories(calories_list):
  return sum(calories_list)


def find_best_day(steps_list):
  if not steps_list:
    return None, 0
  max_steps = max(steps_list)
  best_day_idx = steps_list.index(max_steps) + 1
  return best_day_idx, max_steps


def count_goal_days(steps_list, goal=10000):
  return sum(1 for s in steps_list if s >= goal)


def save_to_csv(steps_list, calories_list, filename="fitness_data.csv"):
  """Saves daily records to a CSV file."""
  with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Day", "Steps", "Calories"])
    for i, (steps, calories) in enumerate(
        zip(steps_list, calories_list), start=1
    ):
      writer.writerow([f"Day {i}", steps, calories])
  print(f"Data successfully saved to {filename}")


def load_from_csv(filename="fitness_data.csv"):
  """Loads daily records from a CSV file."""
  steps_list = []
  calories_list = []
  if not os.path.exists(filename):
    return steps_list, calories_list
  with open(filename, mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
      try:
        steps_list.append(int(row["Steps"]))
        calories_list.append(float(row["Calories"]))
      except ValueError:
        continue
  return steps_list, calories_list


def plot_chart(steps_list, goal=10000):
  """Plots a Matplotlib bar chart of daily steps with goal line."""
  if not steps_list:
    print("No data available to plot.")
    return

  days = [f"Day {i}" for i in range(1, len(steps_list) + 1)]

  plt.figure(figsize=(8, 5))
  bars = plt.bar(days, steps_list, color="#4CAF50", edgecolor="black", alpha=0.85)

  for bar, steps in zip(bars, steps_list):
    if steps >= goal:
      bar.set_color("#2E7D32")

  plt.axhline(
      y=goal,
      color="red",
      linestyle="--",
      linewidth=2,
      label=f"Goal ({goal} steps)",
  )

  plt.title("Daily Steps Tracker", fontsize=14, fontweight="bold", pad=15)
  plt.xlabel("Days", fontsize=12, fontweight="bold")
  plt.ylabel("Steps", fontsize=12, fontweight="bold")
  plt.grid(axis="y", linestyle=":", alpha=0.7)
  plt.legend(loc="upper right")
  plt.tight_layout()
  plt.show()


def main():
  steps_list = []
  calories_list = []


  if os.path.exists("fitness_data.csv"):
    steps_list, calories_list = load_from_csv("fitness_data.csv")
    if steps_list:
      print(f"Loaded {len(steps_list)} record(s) from fitness_data.csv.")

  while True:
    print("\n=== FITNESS DATA TRACKER ===")
    print("1. Add record")
    print("2. Summary")
    print("3. Calculate BMI")
    print("4. Chart")
    print("5. Save to CSV")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ").strip()

    if choice == "1":
      try:
        steps_input = input("Enter steps: ").strip()
        steps = int(steps_input)
        if steps < 0:
          print(
              "Invalid steps. Enter a non-negative whole number. Record not"
              " saved."
          )
          continue

        calories_input = input("Enter calories: ").strip()
        calories = float(calories_input)
        if calories < 0:
          print("Invalid calories. Enter a non-negative number. Record not saved.")
          continue

        steps_list.append(steps)
        calories_list.append(calories)
        day_num = len(steps_list)

        goal = 10000
        achieved = "Yes" if steps >= goal else "No"
        percentage = (steps / goal) * 100
        print(
            f"Record saved for Day {day_num}. Goal achieved: {achieved}"
            f" ({percentage:.2f}% of goal)"
        )

        save_to_csv(steps_list, calories_list)

      except ValueError:
        print(
            "Invalid input. Please enter valid numeric values for steps and"
            " calories."
        )

    elif choice == "2":
      if not steps_list:
        print("No records available yet.")
        continue

      avg_steps = calculate_average_steps(steps_list)
      tot_calories = calculate_total_calories(calories_list)
      best_day_idx, best_steps = find_best_day(steps_list)
      goal_days_count = count_goal_days(steps_list)
      total_days = len(steps_list)

      print(
          f"Average steps: {avg_steps:.2f} | Total calories:"
          f" {tot_calories:.0f} | Best day: Day {best_day_idx} ({best_steps}"
          f" steps) | Goal days: {goal_days_count}/{total_days}"
      )

    elif choice == "3":
      try:
        weight = float(input("Enter weight (kg): ").strip())
        height = float(input("Enter height (m): ").strip())
        bmi, category = calculate_bmi(weight, height)
        print(f"BMI: {bmi:.2f} | Category: {category}")
      except ValueError as e:
        print(f"Invalid input: {e}")

    elif choice == "4":
      plot_chart(steps_list)

    elif choice == "5":
      save_to_csv(steps_list, calories_list)

    elif choice == "6":
      print("Exiting Fitness Data Tracker. Keep moving and stay healthy!")
      break
    else:
      print("Invalid choice. Please select between 1 and 6.")

if __name__ == "__main__":
  main()