#!/usr/bin/env python

# Author: Github - nrkorte
#
# Hi there!
# 
# You are welcome to look through my code to see what is going on underneath the hood and improve it if you'd like
# This program is not the most efficient (time-wise or storage-wise) but it gets the job done much faster than a human can
# The main hub that sends requests for completing questions is in mcbegin()
# From there each question type, prompt, and answer is parsed, completed, and stored through individual function calls
#
# Happy hunting!

import sys
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains


class mcbot:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"./chromedriver.exe")
        self.driver.set_window_position(2000, 0)
        self.driver.maximize_window()
    
    def mcstart(self, user, passw, link):
        time.sleep(3)
        self.driver.get(link)
        WebDriverWait( self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'https://colostate.instructure.com/login/saml')]"))).click()
        WebDriverWait( self.driver, 15).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(user)
        WebDriverWait( self.driver, 15).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(passw)
        WebDriverWait( self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@type, 'submit')]"))).click()
        time.sleep(3)

    def mcbegin(self):
        get_into_questions(self)

        dictionary_for_answers = {}
        self.driver.get(self.driver.current_url)
        while True:
            
            try:
                self.driver.switch_to.alert.dismiss()
                label = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Multiple Choice Question') or contains(text(), 'True or False Question') or contains(text(), 'Multiple Select Question') or contains(text(), 'Fill in the Blank Question') or contains(text(), 'Matching Question') or contains(text(), 'Ordering Question')]"))).text
            except TimeoutException:
                WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),' Next Question')]"))).click()
                label = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Multiple Choice Question') or contains(text(), 'True or False Question') or contains(text(), 'Multiple Select Question') or contains(text(), 'Fill in the Blank Question')  or contains(text(), 'Matching Question') or contains(text(), 'Ordering Question')]"))).text
            except NoAlertPresentException:
                try:
                    label = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Multiple Choice Question') or contains(text(), 'True or False Question') or contains(text(), 'Multiple Select Question') or contains(text(), 'Fill in the Blank Question')  or contains(text(), 'Matching Question') or contains(text(), 'Ordering Question')]"))).text
                except TimeoutException:
                    WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),' Next Question')]"))).click()
                    label = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Multiple Choice Question') or contains(text(), 'True or False Question') or contains(text(), 'Multiple Select Question') or contains(text(), 'Fill in the Blank Question')  or contains(text(), 'Matching Question') or contains(text(), 'Ordering Question')]"))).text

            prompt_in_question = WebDriverWait (self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'prompt')]"))).text

            if label == "Fill in the Blank Question":
                solve_fill_in_question(self, dictionary_for_answers, prompt_in_question)

            elif label == "Multiple Choice Question" or label == "Multiple Select Question" or label == "True or False Question":
                solve_multiple_choice_question(self, dictionary_for_answers, prompt_in_question, label)
            
            elif label == "Matching Question":
                solve_matching_question(self, dictionary_for_answers, prompt_in_question)
            
            elif label == "Ordering Question":
                solve_ordering_question(self, dictionary_for_answers, prompt_in_question)

def solve_fill_in_question(self, dictionary_, prompt_in_question):
    prompt_in_question = parse_prompt(prompt_in_question)
    count = 0
    for prompt in dictionary_:
        count += 1
        if prompt_in_question == prompt:
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
            counter = 0
            for x in dictionary_.get(prompt):
                counter += 1
                number_of_fields = len(dictionary_.get(prompt))
                xpath_string_for_input = "//input[contains(@aria-label, 'Blank "+ str(counter) + " of " + str(number_of_fields) + "')]"
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath_string_for_input))).send_keys(parse_answer(x))
                webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(1)
            try:
                WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'High')]"))).click()
            except TimeoutException:
                print ("Could not find the Low button for: ", prompt_in_question)
            break
    if count == len(dictionary_): # if it was not found in the list
        count = 0
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
        webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
        aria_label = self.driver.find_element(By.XPATH, "//input[contains(@class, 'fitb-input')]").get_attribute('aria-label')
        new_str = int("" + aria_label[len(aria_label) - 1])
        x = 0
        while x < new_str:
            x += 1
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, 'Blank "+ str(x) + " of " + aria_label[len(aria_label) - 1] + "')]"))).send_keys("test")
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
        try:
            WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Low')]"))).click()
        except TimeoutException:
            print ("Could not find the Low button for: ", prompt_in_question)
        tmpstr = WebDriverWait (self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'answer-container')]"))).text
        tmp = tmpstr.split("\n")
        tmp.pop(0)

        dictionary_.update({prompt_in_question: tmp})
        get_around_forced_learning(self, prompt_in_question)
    time.sleep(1)
    try:
        WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),' Next Question')]"))).click()
    except TimeoutException:
        print ("Could not find the Next Question button for: ", prompt_in_question)

def solve_multiple_choice_question(self, dictionary_, prompt_in_question, label):
    prompt_in_question = parse_prompt(prompt_in_question)
    count = 0
    for prompt in dictionary_:
        count += 1
        if prompt_in_question == prompt:
            for x in dictionary_.get(prompt):
                if (label != "True or False Question"):
                    list_store = WebDriverWait (self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'responses-container')]"))).text.split("\n")
                    list_store.pop(0)
                    for v in list_store:
                        v = parse_mc_choice_answer(v)

                    i = 0
                    while i < len(list_store):
                        if str(x) == str(list_store[i]):
                            WebDriverWait( self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '/html/body/awd-root/div[1]/awd-app-root/div/div[2]/div/awd-main-container/div/div/div/div[1]/awd-probe-navigation/div/div[1]/awd-probe/avalon-probe-renderer/div/aa-air-item/div/div/div/div/div/div/div/div/div/div[2]/fieldset/div[' + str(i + 1) + ']'))).click()
                        i += 1


                else:
                    if str(x) == "False": # if it's false
                        WebDriverWait( self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/awd-root/div[1]/awd-app-root/div/div[2]/div/awd-main-container/div/div/div/div[1]/awd-probe-navigation/div/div[1]/awd-probe/avalon-probe-renderer/div/aa-air-item/div/div/div/div/div/div/div/div/div/fieldset/div[2]/div/mhe-radio-button/label/span/span"))).click()
                    else: # if it's true
                        WebDriverWait( self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/awd-root/div[1]/awd-app-root/div/div[2]/div/awd-main-container/div/div/div/div[1]/awd-probe-navigation/div/div[1]/awd-probe/avalon-probe-renderer/div/aa-air-item/div/div/div/div/div/div/div/div/div/fieldset/div[1]/div/mhe-radio-button/label/span/span"))).click()
            time.sleep(1)
            try:
                WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'High')]"))).click()
            except TimeoutException:
                print ("Could not find the High button for: ", prompt_in_question)
            break
    if count == len(dictionary_):
        count = 0
        try:
            WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'choice-row')]"))).click()
            WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Low')]"))).click()
        except TimeoutException:
            print ("Could not find the Low button or any first choice to select after the prompt: ", prompt_in_question)
        tmpstr = WebDriverWait (self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'answer-container')]"))).text
        tmp = tmpstr.split("\n")
        tmp.pop(0)
        for v in tmp:
            v = parse_mc_choice_answer(v)
        dictionary_.update({prompt_in_question: tmp})
        get_around_forced_learning(self, prompt_in_question)
    time.sleep(1)
    try:
        WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),' Next Question')]"))).click()
    except TimeoutException:
        print ("Could not find the Next Question button for: ", prompt_in_question)

def solve_matching_question(self, dictionary_, prompt_in_question):
    
    prompt_in_question = parse_prompt(prompt_in_question)
    count = 0
    for prompt in dictionary_:
        count += 1
        if prompt_in_question == prompt:
            is_it_i = True
            try:
                WebDriverWait (self.driver, 4).until(EC.presence_of_element_located((By.XPATH, "//i[contains(text(), '"+ dictionary_.get(prompt)[1] +"')]")))
            except TimeoutException:
                is_it_i = False
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            action = ActionChains(self.driver)
            remaining = len(dictionary_.get(prompt)) // 2
            xpath_string = "//"
            if is_it_i:
                xpath_string += "i[contains(text(), '"
            else:
                xpath_string += "p[contains(text(), '"
            for test in range(1, len(dictionary_.get(prompt)), 2):
                xpath_string += str(dictionary_.get(prompt)[test])
                if (test != len(dictionary_.get(prompt)) - 1):
                    xpath_string += "') or contains(text(), '"
                else:
                    xpath_string += "')"
            xpath_string += "]"
            
            tmpheader = self.driver.find_element(By.XPATH, "//div[contains(@class, 'choices-container droppableContainer')]")
            all_children_unparsed = tmpheader.find_elements(By.XPATH, xpath_string)
            all_children = []
            for var in all_children_unparsed:
                all_children.append(var.text)
            action.context_click(tmpheader).perform()
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(0.2)
            for ind in range (1, len(dictionary_.get(prompt)), 2):
                for i in range (0, all_children.index(dictionary_.get(prompt)[ind]), 1):
                    webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
                    time.sleep(0.2)
                webdriver.ActionChains(self.driver).send_keys(Keys.SPACE).perform()
                time.sleep(0.5)
                for qwertyui in range (0, remaining + all_children.index(dictionary_.get(prompt)[ind]), 1):
                    webdriver.ActionChains(self.driver).send_keys(Keys.ARROW_UP).perform()
                    time.sleep(0.5)
                webdriver.ActionChains(self.driver).send_keys(Keys.SPACE).perform()
                time.sleep(0.2)
                webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(0.2)
                all_children.remove(dictionary_.get(prompt)[ind])
                remaining -= 1
            
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            try:
                WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'High')]"))).click()
            except TimeoutException:
                print ("Could not find the High button for: ", prompt_in_question)
            time.sleep(1)
            try:
                WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),' Next Question')]"))).click()
            except TimeoutException:
                print ("Could not find the Next Question button for: ", prompt_in_question)
            break

  
    if count == len(dictionary_):
        time.sleep(2)

        header = self.driver.find_element(By.CLASS_NAME, "responses-container")
        all_children = header.find_elements(By.XPATH, ".//*")
        number_of_answers = len(all_children) / 18
        prompt_array = create_prompt_array_for_matching(self, number_of_answers)

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        action = ActionChains(self.driver)
        src = WebDriverWait (self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'choice-item draggableItem')]")))
        action.context_click(src).perform()
        action.click().perform()
        time.sleep(4)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        time.sleep(0.5)

        remaining = number_of_answers
        while remaining > 0:
            i = 0
            while i < remaining:
                i += 1
                webdriver.ActionChains(self.driver).send_keys(Keys.ARROW_UP).perform()
                time.sleep(0.5)
            remaining -= 1
            webdriver.ActionChains(self.driver).send_keys(Keys.SPACE).perform()
            time.sleep(0.5)
            webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
            time.sleep(0.5)
            webdriver.ActionChains(self.driver).send_keys(Keys.SPACE).perform()
            time.sleep(0.5)
        WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Low')]"))).click()

        final_array = make_final_array(self, prompt_array)
        dictionary_.update({prompt_in_question : final_array})
        get_around_forced_learning(self, prompt_in_question)
        try:
            WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),' Next Question')]"))).click()
        except:
            print ("Could not find the Next Question button for: ", prompt_in_question)
        time.sleep(3)
        self.driver.refresh()

# you are getting boned by the right click. revert back to the tab method of getting the right element

def solve_ordering_question(self, dictionary_, prompt_in_question):
    time.sleep(4)
    prompt_in_question = parse_prompt(prompt_in_question)
    count = 0
    tmpheader = WebDriverWait (self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'vertical-list')]")))
    child_elements = tmpheader.find_elements(By.XPATH, "./*")
    child_texts = []
    for var in child_elements:
        child_texts.append(var.text.split("\n"))
    final_array = []
    for i in range (0, len(child_texts), 1):
        final_array.append(child_texts[i][1])
    for prompt in dictionary_:
        count += 1
        # if prompt_in_question == prompt:
        #     webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
        #     webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
        #     webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
        #     for d in range (0, 4, 1):
        #         time.sleep(0.2)
        #         webdriver.ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
        #     time.sleep(5)
        #     finished = 0
        #     print ("Initial array ==> ", final_array)
        #     print ("Correct answer ==> ", dictionary_.get(prompt))
        #     for r in range (0, len(dictionary_.get(prompt)) - 1, 1):
        #         newheader = self.driver.find_element(By.XPATH, "//div[contains(@class, 'responses-container')]")
        #         action = ActionChains(self.driver)
        #         print ("Right clicking: ", dictionary_.get(prompt)[r])
        #         print ("Current scroll height: ", self.driver.execute_script("return document.documentElement.scrollHeight"))
        #         action.context_click(WebDriverWait (newheader, 10).until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), '"+ dictionary_.get(prompt)[r] +"')]")))).perform()
        #         print ("Grabbing")
        #         print ("Current scroll height: ", self.driver.execute_script("return document.documentElement.scrollHeight"))
        #         time.sleep(2)
        #         webdriver.ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        #         time.sleep(2)
        #         final_array, num = swap_back(final_array, dictionary_.get(prompt)[r], r)
        #         for c in range (0, num, 1):
        #             print ("Upping")
        #             webdriver.ActionChains(self.driver).send_keys(Keys.ARROW_UP).perform()
        #             time.sleep(2)
        #         print ("Dropping")
        #         webdriver.ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        #         time.sleep(3)
        #         finished += 1
        #         for d in range (0, 4, 1):
        #             time.sleep(0.2)
        #             webdriver.ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
        #     try:
        #         WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'High')]"))).click()
        #     except TimeoutException:
        #         print ("Could not find the High button for: ", prompt_in_question)
        #     break
    if count == len(dictionary_):
        time.sleep(2)
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        try:
            WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Low')]"))).click()
        except TimeoutException:
            print ("Could not find the Low button for: ", prompt_in_question)

        tmpstr = WebDriverWait (self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'answer-container')]"))).text
        tmp = tmpstr.split("\n")
        tmp.pop(0)
        dictionary_.update({prompt_in_question: tmp})
        get_around_forced_learning(self, prompt_in_question)

    try:
        WebDriverWait( self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),' Next Question')]"))).click()
    except TimeoutException:
        print ("Could not find the Next Question button for: ", prompt_in_question)
    time.sleep(3)

def get_into_questions(self):
    time.sleep(3)
    try:
        self.driver.switch_to.window(self.driver.window_handles[1])
    except:
        print ("You recieved an error because the software attempted to switch to a new window handle without one present. Please restart your program and try again.")
    try:
        WebDriverWait( self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Begin')]"))).click()
    except TimeoutException:
        print(end="1 Failed, ")
    try:
        WebDriverWait( self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Questions')]"))).click()
    except TimeoutException:
        print(end="2 Failed, ")
    try:
        WebDriverWait( self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue Questions')]"))).click()
    except TimeoutException:
        print(end="3 Failed, ")
    try:
        WebDriverWait( self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Start Questions')]"))).click()
    except TimeoutException:
        print(end="4 Failed.")
        
    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

def get_around_forced_learning(self, prompt_in_question):
    try:
        WebDriverWait( self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'review a resource')]"))).click()
        WebDriverWait( self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Read About the Concept')]"))).click()
        WebDriverWait( self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'To Questions')]"))).click()
    except TimeoutException:
        print(end="")

def parse_prompt(prompt_unsplit):
    prompt = prompt_unsplit.split("\n")
    for var in prompt:
        if "Blank" in var or "prompt_array" in var:
            prompt.remove(var)
    ret_str = ""
    for f in prompt:
        ret_str += f
    ret_str = re.sub(r'[\W_]', '', ret_str)
    return ret_str

def parse_answer(answer):
    while answer.find("Blank") != -1:
        start = answer.find("Blank")
        inner = 0
        while inner < 9:
            inner += 1
            answer = answer[:start] + answer[start + 1:]
        if answer.find(",") != -1:
            answer = answer[:answer.find(",")]
        if answer.find(" or") != -1:
            answer = answer[:answer.find(" or")]
    return answer

def parse_mc_choice_answer(ans):
    return re.sub(r'[\W_]', '', ans)

def create_prompt_array_for_matching(self, number_of_answers):
    count = 0
    add = "/following-sibling::div"
    prompt_array = []
    while count < number_of_answers:
        start = "//div[contains(@class, 'match-row')]"
        inner = 0
        while inner < count:
            start += add
            inner += 1
        count += 1
        prompt_array.append(WebDriverWait (self.driver, 30).until(EC.presence_of_element_located((By.XPATH, start))).text) # might also just need to run the following sibling thing multiple times with multiple variables getting created

    prompt_array[0] = prompt_array[0].split("\n", 1)[0]
    prompt_array[1] = prompt_array[1].split("\n", 1)[0]
    prompt_array[2] = prompt_array[2].split("\n", 1)[0]
    return prompt_array

def make_final_array(self, prompt_array):
    tmp = WebDriverWait (self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'correct-list')]"))).text.split("\n")
    answer_array = []
    while len(tmp) > 0:
        tmp.pop(0)
        tmp.pop(0)
        tmp.pop(0)
        answer_array.append(tmp.pop(0))
    final_array = []
    i = 0
    while i < len(prompt_array):
        final_array.append(prompt_array[i])
        final_array.append(answer_array[i])
        i += 1
    return final_array

def swap_back (arr, thing, end):
    num = arr.index(thing)
    counter = 0
    while (num > end):
        arr[num] = arr[num - 1]
        arr[num - 1] = thing
        num -= 1
        counter += 1
    return arr, counter

if __name__ == "__main__":
# arguments in order : username, password, link to hw
    # print("Python version: ", sys.version)
    if (len(sys.argv) != 4):
        raise Exception("Wrong number of program arguments: found ", len(sys.argv) ," needed 3 additional. Exiting now...")
    bot = mcbot()
    bot.mcstart(sys.argv[1], sys.argv[2], sys.argv[3])
    bot.mcbegin()
    