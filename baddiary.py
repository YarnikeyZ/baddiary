#Requirments: Python3, Selenium, geckodriver.exe, firefox binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from sys import argv

def find(driver, xpath):
    return driver.find_element(By.XPATH, xpath)

def prepare(firefox_binary: str, geckodriver: str, login: str, password: str) -> None:
    """
    1. Starts up browser window;
    2. Logs in with your credentials;
    3. Navigates to the neded table with marks;
    4. Cleans page up;
    """
    global driver
    options = webdriver.firefox.options.Options()
    options.binary = webdriver.firefox.firefox_binary.FirefoxBinary(firefox_binary)
    driver = webdriver.Firefox(executable_path=geckodriver, options=options)
    driver.get('https://login.dnevnik.ru/login/')
    find(driver, '/html/body/div/div/div/div/div/form/div[2]/div[3]/div[1]/div[1]/label/input').send_keys(login)
    find(driver, '/html/body/div/div/div/div/div/form/div[2]/div[3]/div[2]/div[1]/label/input').send_keys(password)
    find(driver, '/html/body/div/div/div/div/div/form/div[2]/div[3]/div[4]/div[1]/input').click()
    find(driver, '/html/body/div[3]/div/div[2]/ul/li[2]/ul/li[3]/a').click()
    find(driver, '//*[@id="TabPeriod"]').click()
    to_remove = [
        "/html/body/div[2]/div[1]/h2",
        "/html/body/div[1]/div[1]/div/div[2]/div[1]/div",
        "/html/body/div[2]/div[1]/ul[1]/li[1]",
        "/html/body/div[2]/div[1]/div[8]/div"
    ]
    for element in to_remove:
        driver.execute_script("var element = arguments[0];\nelement.parentNode.removeChild(element);", driver.find_element(By.XPATH, element))

def display(frames: str, fps: float) -> None:
    """
    Redacts the html of a page to display frames.
    """
    input("Display?...")
    sleep(10)
    display_start = datetime.now()
    remaining = 0
    overflow = 0
    count = len(frames)
    for frame in range(1, count+1):
        frame_time = datetime.now()
        driver.execute_script(f"var ele=arguments[0]; ele.outerHTML = '{frames[0]}';", driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/table/tbody'))
        manual_frame_time = 1/fps - (datetime.now() - frame_time).microseconds/1000000-remaining
        if manual_frame_time > 0:
            sleep(manual_frame_time)
            remaining = 0
        else:
            overflow += 1
            remaining = manual_frame_time*-1
        frames.pop(0)
        print(f'Time Total/FPS/Preset FT/Manual FT/Used FT/Overflowed: {datetime.now()-display_start}/{fps}/{1/fps}/{manual_frame_time}/{datetime.now()-frame_time}/{overflow}')

def re_render(path: str) -> list:
    """
    Re-renders output of special (deprecated) version of https://github.com/YarnikeyZ/bad_apple_ta output
    """
    five =  '<span class="mark mG analytics-app-popup-mark ">5</span>'
    four =  '<span class="mark mG analytics-app-popup-mark ">4</span>'
    three = '<span class="mark mY analytics-app-popup-mark ">3</span>'
    two =   '<span class="mark mR analytics-app-popup-mark ">2</span>'
    one =   '<span class="mark mR analytics-app-popup-mark ">1</span>'
    mark_frames = []
    with open(path, "r", encoding="utf-8") as txt_frames:
        symb_frames = txt_frames.read().split("\n{~~~~~~~~~~~~~~~}\n")
    for frame in range(1, len(symb_frames)+1):
        rows = []
        web_frame = symb_frames[0]
        web_frame = web_frame.replace("#", five).replace("%", four).replace("+", three).replace("*", two).replace(".", one)
        web_frame = web_frame.split("\n")
        for line in web_frame:
            rows.append(f'<tr><td class="tac">0</td><td class="tac">Row</td><td class="s2"><a href="nah" title="nah"><strong class="u">{line}</strong></a></td><td class="tac" style="text-align:left;">0</td><td>0</td><td>0</td><td>0</td></tr>')
        title = f'<tr><th style="width:3%" rowspan="2">№</th><th style="width:20%" rowspan="2">Предметы</th><th style="width:46%" rowspan="2">Оценки</th><th style="width:5%" rowspan="2">Опоздания</th><th style="width:10%" colspan="2">Пропуски</th><th style="width:5%" rowspan="2"><b>2 четверть</b><p>Итог</p></th></tr><tr><th style="width:5%">Всего</th><th style="width:5%">По болезни</th></tr>'
        mark_frames.append(f'<tbody> {title} {"".join(rows)} </tbody>')
        symb_frames.pop(0)
    return mark_frames

def main():
    """
    main.
    """
    frames = re_render(f"{argv[1]}txt_frames_{argv[2]}")
    prepare(
        firefox_binary=r'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
        geckodriver=r'D:\python_p\\geckodriver.exe',
        login='login',
        password='password'
    )
    display(
        frames=frames,
        fps=float(argv[3])
    )

if __name__ == "__main__":
    main()
