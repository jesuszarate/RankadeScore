import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json


class Rankade:

    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.login(username, password)

        self.users = self.load_users('users.json')
        print(self.users)

    def login(self, username, password):
        self.driver.get('https://rankade.com/signin/')

        self.driver.find_element_by_class_name('sign-button')

        _username = self.driver.find_element_by_name('email')
        _username.send_keys(username)

        _password = self.driver.find_element_by_name('password')
        _password.send_keys(password)

        _password.submit()

        self.driver.get('https://rankade.com/#/group/WkMK9GYyb2o/DlLprOnOKM7')

        self.clearPopUps()

    def add_matches(self, players, scores):
        add_match = self.driver.find_element_by_xpath('//*[@id="teamRankWidget"]/div[1]/a[1]')
        time.sleep(2)
        add_match.click()

        for score in scores:
            time.sleep(2)
            self.add_match(players, score)

    def add_match(self, users, score):

        for i in range(0, len(users)):
            user = self.users[users[i]]
            print('adding user: {0}, at position: {1}'.format(user, i + 1))
            self.select_user(user, i + 1)

        self.add_score(score[0], score[1])

    def add_score(self, home_score, away_score):
        self.driver.find_element_by_name('f0_points').send_keys(home_score)
        self.driver.find_element_by_name('f1_points').send_keys(away_score)

        self.save_score()

    def save_score(self):
        self.driver.find_element_by_xpath('//*[@id="matchModal"]/div/div/div[3]/a[1]').click()

    def clearPopUps(self):
        closed = False
        try:
            time.sleep(5)  # Let the user actually see something!
            self.driver.find_element_by_xpath('//*[@id="goProGroupModal"]/div/div/div[1]/button').click()
            closed = True
        except:
            closed = False

        if not closed:
            try:
                time.sleep(5)
                self.driver.find_element_by_xpath('//*[@id="goProGroupModal"]/div/div/div[3]/button').click()
                closed = True
            except:
                closed = False

        if not closed:
            try:
                alert = self.driver.switch_to_alert()
                alert.accept()
            except:
                closed = False

    def click_user(self, dropdown, user_id):
        elements = dropdown.find_elements_by_tag_name('li')
        actions = ActionChains(self.driver)

        for option in elements:
            if option.get_attribute('data-user-id') == user_id:
                option.click()
            else:
                actions.send_keys(Keys.ARROW_DOWN)
                actions.perform()

    def select_user(self, user_id, user_spot):
        time.sleep(3)

        print("Finding dropdown")

        dropdown = None
        if user_spot == 1:
            dropdown = self.driver.find_element_by_xpath(
                '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[1]/div/div[1]/div')

        elif user_spot == 2:
            dropdown = self.driver.find_element_by_xpath(
                '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[1]/div/div[2]/div')

        elif user_spot == 3:
            dropdown = self.driver.find_element_by_xpath(
                '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[2]/div/div[1]/div')

        elif user_spot == 4:
            dropdown = self.driver.find_element_by_xpath(
                '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[2]/div/div[2]/div')

        if dropdown != None:
            print("Clicking dropdown")
            time.sleep(1)
            dropdown.click()

            self.click_user(dropdown, user_id)

    def load_users(self, users_file):
        with open(users_file) as f:
            d = json.load(f)
            return d


def read_match(filename='match.txt'):
    with open(filename, 'r') as f:

        line = f.readline().split('=')

        players = list()
        for player in line[0].split(','):
            players.append(player.replace('@', ''))

        print(players)

        scores = list()
        for score in line[1].split(';'):
            ss = score.split(',')
            scores.append((ss[0], ss[1]))
        print(scores)

    return players, scores


if __name__ == '__main__':
    r = Rankade('fake.emai.@gmail.com', 'notarealpassword')
    players, scores = read_match()

    r.add_matches(players, scores)
    r.driver.quit()
