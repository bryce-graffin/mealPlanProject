"""
This method is where the project will be run from.
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


def get_meal_plan(calories, meals):
    """
    This function takes in user input variables that define the type of meal plan they are looking for. Then uses
    Eat This Much to generate a meal plan for an entire month.
    :param calories: the total number of daily calories that will be used to generate the plan.
    :param meals: the total number of meals the user wishes to have per day in their plan.
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
    print('Driver initialized...')

    # get the information from the page
    driver.get(url)
    print('Locating "https://eatthismuch.com"...')
    time.sleep(5)

    # tell the website how many calories and meals we want to use
    driver.find_element(By.ID, 'cal_input').send_keys(calories)
    meal_selector = Select(driver.find_element(By.XPATH, '//select[@id="num_meals_selector"]'))
    meal_selector.select_by_visible_text(f'{meals} meals')
    driver.find_element(By.XPATH, '//button[@class="btn btn-lg btn-block btn-orange gen_button"]').click()

    # wait for the page to load
    print('Generating meal plan based on user input...')
    time.sleep(5)

    # find all the meals generated for the set calories and meal count
    meals = driver.find_elements(By.XPATH, '//div[@class="meal_box meal_container row"]')
    print('Meals generated.')

    meal_list = []  # all meals

    # TODO: make this work for an entire month, add checks for repeat recipes
    # get each meal for the day
    for meal in range(len(meals)):
        meal_type = driver.find_element(By.XPATH, './/div[@class="col-auto text-dark-gray text-large text-strong '
                                                  'print_meal_title wrap_or_truncate pr-0"]')
        meal_name = driver.find_element(By.XPATH, './/div[@class="print_name"]')
        meal_calories = driver.find_element(By.XPATH, './/span[@class="cal_amount text-small text-light-gray"]')
        print(f'\n{meal_type.text}')
        print(f'Total Calories: {meal_calories.text}\n')
        print(f'Meal Name: {meal_name}')
        # get each food in each meal
        foods = driver.find_elements(By.XPATH, './/li[@class="diet_draggable ui-sortable-handle"]')

        for food in foods:
            food_name = food.find_element(By.XPATH, './/div[@class="print_name"]')
            print(f'Food: {food_name}')
            # TODO: fix this part for images
            # food_image = food.find_element(By.XPATH,'.//div[@class="food_image"]')
            # food_image_url = food_image.get_attribute('style')
            # food_image_url = food_image_url[food_image_url.index('url(') + 4:]
            # food_image_url = food_image_url[:food_image_url.index(')')]
            #
            # # Print food details
            # print(f'{food_name.text}')
            # print(food_image_url)
            #
            # # try to display the food image
            # try:
            #     response = requests.get(food_image_url)
            #     img = Image.open(io.BytesIO(response.content))
            #     img.show()
            # except Exception as e:
            #     print(f'Error fetching/displaying image: {e}')
            # TODO: add something here to look for ingredients

        # add the meal for the list
        meal_list.append(meals[meal].text)

    # quit the driver and return the meal plan
    driver.quit()
    return '\n'.join(meal_list)


if __name__ == '__main__':
    # user inputs
    cals = input('Enter desired daily calories (0-20k): ')
    num_meals = input('Enter meal count per day (1-9): ')

    # get plan
    meal_plan = get_meal_plan(cals, num_meals)
    print(meal_plan)
