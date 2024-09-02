"""
Module Name:
    main.py

Author:
    Bryce Graffin

Date:
    September 1, 2024
"""


# import io
# import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from PIL import Image
import time


def get_meal_plan(calories, num_meals):
    """
    This function takes in user input variables that define the type of meal plan they are looking for. Then uses
    Eat This Much to generate a meal plan for an entire month.
    :param calories: the total number of daily calories that will be used to generate the plan.
    :param num_meals: the total number of meals the user wishes to have per day in their plan.
    :return: String - formatted to output the meal plan in a readable fashion.
    """

    # first, we need to make a form submission so the website knows what to generate for us before we grab the results
    url = 'https://www.eatthismuch.com'

    # specific arguments for making requests
    options = Options()
    options.add_argument('--headless')
    options.add_argument('chromedriver --log-level=OFF')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-logging')
    options.add_argument('log-level=3')

    # init the webdriver
    service = Service("/Users/Bryce/Downloads/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    # print('Driver initialized...')

    # get the information from the page
    driver.get(url)
    # print('Locating "https://eatthismuch.com"...')
    time.sleep(3)

    # tell the website how many calories and meals we want to use
    driver.find_element(By.ID, 'cal_input').send_keys(calories)
    meal_selector = Select(driver.find_element(By.XPATH, '//select[@id="num_meals_selector"]'))
    meal_selector.select_by_visible_text(f'{num_meals} meals')
    driver.find_element(By.XPATH, '//button[@class="btn btn-lg btn-block btn-orange gen_button"]').click()

    # wait for the page to load
    # print('Generating meal plan based on user input...')
    time.sleep(5)

    # find all the meals generated for the set calories and meal count
    meals = driver.find_elements(By.XPATH, './/div[@class="meal_box meal_container row"]')
    # print('Meals generated.\n')
    # print(f'Meals: {meals}')

    meal_list = []  # all meals
    food_list = []  # all foods (in each meal)

    # TODO: make this work for an entire month, add checks for repeat recipes
    # get each meal for the day
    for index, meal in enumerate(meals):
        # add the meal information for the meal list
        meal_name = meal.find_element(By.XPATH, './/div[@class="col-auto text-dark-gray text-large text-strong '
                                                'print_meal_title wrap_or_truncate pr-0"]')
        meal_calories = meal.find_element(By.XPATH, './/span[@class="cal_amount text-small text-light-gray"]')

        meal_list.append(f'\n{meal_name.text}')
        meal_list.append(meal_calories.text)

        # get each of the foods in the corresponding meal
        meal_foods = meal.find_elements(By.XPATH, './/div[@class="food_name col-12"]/div[@class="print_name"]')
        for food in range(len(meal_foods)):
            meal_list.append(f'{meal_foods[food].text}')

    # get each food in the meal
    foods = driver.find_elements(By.XPATH, './/div[@class="food_name col-12"]/div[@class="print_name"]')

    # TODO: this will be where we check for repeat foods in the plan (within the same week) so we can swap
    for food in range(len(foods)):
        food_list.append(foods[food].text)
        # print(f'Foods:\n{foods[food].text}\n')

    # quit the driver and return the meal plan
    driver.quit()
    food_list.insert(0, '\nFoods for the day:')
    return '\n'.join(meal_list + food_list)


if __name__ == '__main__':
    # user inputs
    while True:
        try:
            days = int(input('Enter how many days you would like to plan for: '))
            break  # exit the loop if the user enters a valid integer value
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            cals = int(input('Enter desired daily calories (0-20k): '))
            break  # exit the loop if the user enters a valid integer value
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            num_of_meals = int(input('Enter meal count per day (1-9): '))
            break  # exit the loop if the user enters a valid integer value
        except ValueError:
            print("Please enter a valid integer.")

    i = 0  # current day iteration

    # get plan for a month
    while i < days:
        meal_plan = get_meal_plan(cals, num_of_meals)
        print(f'\nDay {i + 1}:\n{meal_plan}')
        i += 1
